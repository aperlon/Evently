"""
API endpoints for Evently
"""
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import City, Event, EventImpact
from app.api import schemas
from app.analytics.impact_analyzer import ImpactAnalyzer
from app.analytics.scenario_simulator import ScenarioSimulator

router = APIRouter()


# ============================================================================
# City Endpoints
# ============================================================================

@router.get("/cities", response_model=List[schemas.CityResponse])
def get_cities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all cities"""
    cities = db.query(City).offset(skip).limit(limit).all()
    return cities


@router.get("/cities/{city_id}", response_model=schemas.CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    """Get a specific city"""
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/cities", response_model=schemas.CityResponse, status_code=201)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    """Create a new city"""
    # Check if city already exists
    existing = db.query(City).filter(City.name == city.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="City already exists")

    db_city = City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


# ============================================================================
# Event Endpoints
# ============================================================================

@router.get("/events", response_model=List[schemas.EventResponse])
def get_events(
    city_id: Optional[int] = None,
    event_type: Optional[str] = None,
    year: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all events with optional filters"""
    query = db.query(Event)

    if city_id:
        query = query.filter(Event.city_id == city_id)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if year:
        query = query.filter(Event.year == year)

    events = query.offset(skip).limit(limit).all()
    return events


@router.get("/events/{event_id}", response_model=schemas.EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/events", response_model=schemas.EventResponse, status_code=201)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    # Verify city exists
    city = db.query(City).filter(City.id == event.city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    # Extract year from start_date
    event_data = event.model_dump()
    event_data['year'] = event.start_date.year

    db_event = Event(**event_data)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


# ============================================================================
# Impact Analysis Endpoints
# ============================================================================

@router.get("/events/{event_id}/impact", response_model=schemas.EventImpactResponse)
def get_event_impact(
    event_id: int,
    recalculate: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get impact analysis for an event

    Args:
        event_id: Event ID
        recalculate: Force recalculation of impact metrics
    """
    # Check if event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Get existing impact or calculate new one
    impact = db.query(EventImpact).filter(EventImpact.event_id == event_id).first()

    if not impact or recalculate:
        analyzer = ImpactAnalyzer(db)
        impact = analyzer.calculate_event_impact(event_id)

        if not impact:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data to calculate impact"
            )

        # Save to database
        if recalculate and db.query(EventImpact).filter(EventImpact.event_id == event_id).first():
            # Update existing
            db.query(EventImpact).filter(EventImpact.event_id == event_id).update(
                {k: v for k, v in impact.__dict__.items() if not k.startswith('_')}
            )
        else:
            # Create new
            db.add(impact)

        db.commit()
        db.refresh(impact)

    return impact


@router.post("/events/batch-analyze", response_model=List[schemas.EventImpactResponse])
def batch_analyze_events(
    event_ids: List[int],
    db: Session = Depends(get_db)
):
    """Batch analyze multiple events"""
    analyzer = ImpactAnalyzer(db)
    results = []

    for event_id in event_ids:
        try:
            impact = analyzer.calculate_event_impact(event_id)
            if impact:
                # Check if exists
                existing = db.query(EventImpact).filter(EventImpact.event_id == event_id).first()
                if existing:
                    # Update
                    for key, value in impact.__dict__.items():
                        if not key.startswith('_'):
                            setattr(existing, key, value)
                    db.commit()
                    db.refresh(existing)
                    results.append(existing)
                else:
                    # Create new
                    db.add(impact)
                    db.commit()
                    db.refresh(impact)
                    results.append(impact)
        except Exception as e:
            # Log error but continue with other events
            print(f"Error analyzing event {event_id}: {str(e)}")
            continue

    return results


# ============================================================================
# Time Series Endpoints
# ============================================================================

@router.get("/analytics/timeseries/{city_id}")
def get_time_series(
    city_id: int,
    metric_type: str = Query(..., regex="^(tourism|hotel|economic|mobility)$"),
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    """Get time series data for a city"""
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    analyzer = ImpactAnalyzer(db)
    df = analyzer.get_time_series(city_id, metric_type, start_date, end_date)

    if df.empty:
        return {
            "metric_name": metric_type,
            "city_name": city.name,
            "data_points": [],
            "events": []
        }

    # Get events in this period
    events = db.query(Event).filter(
        Event.city_id == city_id,
        Event.start_date >= start_date,
        Event.start_date <= end_date
    ).all()

    # Format data points
    data_points = df.to_dict('records')

    return {
        "metric_name": metric_type,
        "city_name": city.name,
        "data_points": data_points,
        "events": [
            {
                "id": e.id,
                "name": e.name,
                "start_date": e.start_date,
                "end_date": e.end_date,
                "event_type": e.event_type
            }
            for e in events
        ]
    }


# ============================================================================
# Comparison Endpoints
# ============================================================================

@router.post("/analytics/compare/events")
def compare_events(
    event_ids: List[int],
    db: Session = Depends(get_db)
):
    """Compare multiple events"""
    if len(event_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 events required")

    analyzer = ImpactAnalyzer(db)
    comparison_df = analyzer.compare_events(event_ids)

    if comparison_df.empty:
        raise HTTPException(
            status_code=404,
            detail="No impact data found for these events"
        )

    return {
        "comparison_type": "events",
        "items": comparison_df.to_dict('records')
    }


@router.post("/analytics/compare/cities")
def compare_cities(
    city_ids: List[int],
    db: Session = Depends(get_db)
):
    """Compare multiple cities"""
    if len(city_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 cities required")

    analyzer = ImpactAnalyzer(db)
    comparison_df = analyzer.compare_cities(city_ids)

    if comparison_df.empty:
        raise HTTPException(
            status_code=404,
            detail="No impact data found for these cities"
        )

    return {
        "comparison_type": "cities",
        "items": comparison_df.to_dict('records')
    }


# ============================================================================
# What-If Scenario Endpoints
# ============================================================================

@router.post("/analytics/whatif/attendance")
def simulate_attendance_change(
    scenario: schemas.WhatIfScenarioInput,
    db: Session = Depends(get_db)
):
    """Simulate what-if scenario for attendance change"""
    event = db.query(Event).filter(Event.id == scenario.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    simulator = ScenarioSimulator(db)
    result = simulator.simulate_attendance_change(
        event_id=scenario.event_id,
        attendance_change_pct=scenario.attendance_change_pct,
        price_elasticity=scenario.price_elasticity,
        spending_multiplier=scenario.spending_multiplier,
    )

    if not result:
        raise HTTPException(
            status_code=400,
            detail="Insufficient data to simulate scenario"
        )

    return result


@router.get("/analytics/whatif/growth/{event_id}")
def simulate_event_growth(
    event_id: int,
    years: int = Query(5, ge=1, le=10),
    annual_growth_pct: float = Query(10, ge=-50, le=100),
    db: Session = Depends(get_db)
):
    """Simulate multi-year event growth"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    simulator = ScenarioSimulator(db)
    result = simulator.simulate_event_growth(
        event_id=event_id,
        years=years,
        annual_growth_pct=annual_growth_pct
    )

    return result


# ============================================================================
# Dashboard KPI Endpoints
# ============================================================================

@router.get("/analytics/dashboard/kpis", response_model=schemas.DashboardKPIs)
def get_dashboard_kpis(db: Session = Depends(get_db)):
    """Get key performance indicators for dashboard"""
    # Total events analyzed
    total_events = db.query(Event).count()

    # Total cities
    total_cities = db.query(City).count()

    # Get all impacts
    impacts = db.query(EventImpact).all()

    if not impacts:
        raise HTTPException(
            status_code=404,
            detail="No impact data available yet"
        )

    # Calculate averages
    avg_economic_impact = sum(
        i.total_economic_impact_usd for i in impacts if i.total_economic_impact_usd
    ) / len(impacts)

    avg_visitor_increase = sum(
        i.visitor_increase_pct for i in impacts if i.visitor_increase_pct
    ) / len(impacts)

    avg_price_increase = sum(
        i.price_increase_pct for i in impacts if i.price_increase_pct
    ) / len(impacts)

    total_jobs = sum(i.jobs_created for i in impacts if i.jobs_created)

    # Find highest impact event
    highest_impact = max(
        impacts,
        key=lambda i: i.total_economic_impact_usd or 0
    )
    highest_impact_event = db.query(Event).filter(
        Event.id == highest_impact.event_id
    ).first()

    # Find city with most impact
    from sqlalchemy import func
    city_impacts = db.query(
        Event.city_id,
        func.sum(EventImpact.total_economic_impact_usd).label('total_impact')
    ).join(EventImpact, Event.id == EventImpact.event_id).group_by(
        Event.city_id
    ).order_by(func.sum(EventImpact.total_economic_impact_usd).desc()).first()

    highest_impact_city = db.query(City).filter(
        City.id == city_impacts[0]
    ).first()

    return {
        "total_events_analyzed": total_events,
        "total_cities": total_cities,
        "avg_economic_impact_per_event_usd": round(avg_economic_impact, 2),
        "avg_visitor_increase_pct": round(avg_visitor_increase, 2),
        "avg_hotel_price_increase_pct": round(avg_price_increase, 2),
        "total_jobs_created": int(total_jobs),
        "highest_impact_event": highest_impact_event,
        "highest_impact_city": highest_impact_city,
    }
