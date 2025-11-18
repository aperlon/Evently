"""
File upload endpoints for importing data from CSV/XLSX
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import io
from datetime import datetime
from typing import List

from app.core.database import get_db
from app.models import City, Event, HotelMetric, TourismMetric, EconomicMetric
from app.models.event import EventType

router = APIRouter()


@router.post("/upload/cities")
async def upload_cities_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload cities from CSV/XLSX file

    Expected columns:
    - name (required)
    - country (required)
    - country_code (required)
    - continent (required)
    - latitude (required)
    - longitude (required)
    - timezone (required)
    - population (optional)
    - annual_tourists (optional)
    - hotel_rooms (optional)
    - avg_hotel_price_usd (optional)
    """

    # Validate file type
    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        raise HTTPException(
            status_code=400,
            detail="File must be CSV or XLSX format"
        )

    try:
        # Read file
        contents = await file.read()

        # Parse based on file type
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:  # xlsx
            df = pd.read_excel(io.BytesIO(contents))

        # Validate required columns
        required_columns = [
            'name', 'country', 'country_code', 'continent',
            'latitude', 'longitude', 'timezone'
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )

        # Insert cities
        cities_created = 0
        cities_skipped = 0

        for _, row in df.iterrows():
            # Check if city already exists
            existing = db.query(City).filter(City.name == row['name']).first()
            if existing:
                cities_skipped += 1
                continue

            # Create city
            city = City(
                name=row['name'],
                country=row['country'],
                country_code=row['country_code'],
                continent=row['continent'],
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                timezone=row['timezone'],
                population=int(row['population']) if pd.notna(row.get('population')) else None,
                area_km2=float(row['area_km2']) if pd.notna(row.get('area_km2')) else None,
                gdp_usd=float(row['gdp_usd']) if pd.notna(row.get('gdp_usd')) else None,
                annual_tourists=int(row['annual_tourists']) if pd.notna(row.get('annual_tourists')) else None,
                hotel_rooms=int(row['hotel_rooms']) if pd.notna(row.get('hotel_rooms')) else None,
                avg_hotel_price_usd=float(row['avg_hotel_price_usd']) if pd.notna(row.get('avg_hotel_price_usd')) else None,
            )
            db.add(city)
            cities_created += 1

        db.commit()

        return {
            "message": "Cities imported successfully",
            "cities_created": cities_created,
            "cities_skipped": cities_skipped,
            "total_rows": len(df)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


@router.post("/upload/events")
async def upload_events_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload events from CSV/XLSX file

    Expected columns:
    - name (required)
    - city_name (required) - must match existing city
    - event_type (required) - sports, music, culture, etc.
    - start_date (required) - YYYY-MM-DD format
    - end_date (required) - YYYY-MM-DD format
    - expected_attendance (optional)
    - actual_attendance (optional)
    - venue_name (optional)
    - description (optional)
    """

    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        raise HTTPException(status_code=400, detail="File must be CSV or XLSX")

    try:
        contents = await file.read()

        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        # Validate required columns
        required = ['name', 'city_name', 'event_type', 'start_date', 'end_date']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing columns: {', '.join(missing)}"
            )

        events_created = 0
        events_skipped = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                # Get city
                city = db.query(City).filter(City.name == row['city_name']).first()
                if not city:
                    errors.append(f"Row {idx+1}: City '{row['city_name']}' not found")
                    continue

                # Parse dates
                start_date = pd.to_datetime(row['start_date']).date()
                end_date = pd.to_datetime(row['end_date']).date()

                # Validate event type
                try:
                    event_type = EventType(row['event_type'].lower())
                except ValueError:
                    errors.append(f"Row {idx+1}: Invalid event_type '{row['event_type']}'")
                    continue

                # Create event
                event = Event(
                    city_id=city.id,
                    name=row['name'],
                    event_type=event_type,
                    description=row.get('description', ''),
                    start_date=start_date,
                    end_date=end_date,
                    year=start_date.year,
                    expected_attendance=int(row['expected_attendance']) if pd.notna(row.get('expected_attendance')) else None,
                    actual_attendance=int(row['actual_attendance']) if pd.notna(row.get('actual_attendance')) else None,
                    venue_name=row.get('venue_name'),
                    is_recurring=bool(row.get('is_recurring', False)),
                )
                db.add(event)
                events_created += 1

            except Exception as e:
                errors.append(f"Row {idx+1}: {str(e)}")
                continue

        db.commit()

        return {
            "message": "Events imported",
            "events_created": events_created,
            "total_rows": len(df),
            "errors": errors if errors else None
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@router.post("/upload/hotel-metrics")
async def upload_hotel_metrics_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload hotel metrics from CSV/XLSX

    Expected columns:
    - city_name (required)
    - date (required) - YYYY-MM-DD
    - occupancy_rate_pct (optional)
    - avg_price_usd (optional)
    - available_rooms (optional)
    - occupied_rooms (optional)
    """

    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        raise HTTPException(status_code=400, detail="File must be CSV or XLSX")

    try:
        contents = await file.read()

        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        # Validate
        required = ['city_name', 'date']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing: {', '.join(missing)}")

        metrics_created = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                # Get city
                city = db.query(City).filter(City.name == row['city_name']).first()
                if not city:
                    errors.append(f"Row {idx+1}: City not found")
                    continue

                # Parse date
                metric_date = pd.to_datetime(row['date']).date()

                # Check if metric already exists
                existing = db.query(HotelMetric).filter(
                    HotelMetric.city_id == city.id,
                    HotelMetric.date == metric_date
                ).first()

                if existing:
                    # Update existing
                    if pd.notna(row.get('occupancy_rate_pct')):
                        existing.occupancy_rate_pct = float(row['occupancy_rate_pct'])
                    if pd.notna(row.get('avg_price_usd')):
                        existing.avg_price_usd = float(row['avg_price_usd'])
                    if pd.notna(row.get('available_rooms')):
                        existing.available_rooms = int(row['available_rooms'])
                    if pd.notna(row.get('occupied_rooms')):
                        existing.occupied_rooms = int(row['occupied_rooms'])
                else:
                    # Create new
                    metric = HotelMetric(
                        city_id=city.id,
                        date=metric_date,
                        occupancy_rate_pct=float(row['occupancy_rate_pct']) if pd.notna(row.get('occupancy_rate_pct')) else None,
                        avg_price_usd=float(row['avg_price_usd']) if pd.notna(row.get('avg_price_usd')) else None,
                        available_rooms=int(row['available_rooms']) if pd.notna(row.get('available_rooms')) else None,
                        occupied_rooms=int(row['occupied_rooms']) if pd.notna(row.get('occupied_rooms')) else None,
                        median_price_usd=float(row['median_price_usd']) if pd.notna(row.get('median_price_usd')) else None,
                    )
                    db.add(metric)

                metrics_created += 1

            except Exception as e:
                errors.append(f"Row {idx+1}: {str(e)}")
                continue

        db.commit()

        return {
            "message": "Hotel metrics imported",
            "metrics_created": metrics_created,
            "total_rows": len(df),
            "errors": errors if errors else None
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload/tourism-metrics")
async def upload_tourism_metrics_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload tourism metrics from CSV/XLSX

    Expected columns:
    - city_name (required)
    - date (required)
    - total_visitors (optional)
    - international_visitors (optional)
    - domestic_visitors (optional)
    - avg_spending_per_visitor_usd (optional)
    """

    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        raise HTTPException(status_code=400, detail="File must be CSV or XLSX")

    try:
        contents = await file.read()

        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        required = ['city_name', 'date']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing: {', '.join(missing)}")

        metrics_created = 0

        for idx, row in df.iterrows():
            city = db.query(City).filter(City.name == row['city_name']).first()
            if not city:
                continue

            metric_date = pd.to_datetime(row['date']).date()

            metric = TourismMetric(
                city_id=city.id,
                date=metric_date,
                total_visitors=int(row['total_visitors']) if pd.notna(row.get('total_visitors')) else None,
                international_visitors=int(row['international_visitors']) if pd.notna(row.get('international_visitors')) else None,
                domestic_visitors=int(row['domestic_visitors']) if pd.notna(row.get('domestic_visitors')) else None,
                avg_spending_per_visitor_usd=float(row['avg_spending_per_visitor_usd']) if pd.notna(row.get('avg_spending_per_visitor_usd')) else None,
            )
            db.add(metric)
            metrics_created += 1

        db.commit()

        return {
            "message": "Tourism metrics imported",
            "metrics_created": metrics_created,
            "total_rows": len(df)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/templates/cities")
def download_cities_template():
    """Download CSV template for cities upload"""
    csv_data = """name,country,country_code,continent,latitude,longitude,timezone,population,annual_tourists,hotel_rooms,avg_hotel_price_usd
Barcelona,Spain,ESP,Europe,41.3874,2.1686,Europe/Madrid,1620000,9000000,70000,150
Amsterdam,Netherlands,NLD,Europe,52.3676,4.9041,Europe/Amsterdam,872680,8700000,35000,180
"""

    return {
        "filename": "cities_template.csv",
        "content": csv_data,
        "content_type": "text/csv"
    }


@router.get("/templates/events")
def download_events_template():
    """Download CSV template for events upload"""
    csv_data = """name,city_name,event_type,start_date,end_date,expected_attendance,actual_attendance,venue_name,description
Formula 1 Barcelona,Barcelona,sports,2024-06-21,2024-06-23,200000,195000,Circuit de Barcelona-Catalunya,F1 Grand Prix
ADE Amsterdam,Amsterdam,music,2024-10-16,2024-10-20,400000,450000,Various venues,Amsterdam Dance Event
"""

    return {
        "filename": "events_template.csv",
        "content": csv_data,
        "content_type": "text/csv"
    }


@router.get("/templates/hotel-metrics")
def download_hotel_metrics_template():
    """Download CSV template for hotel metrics"""
    csv_data = """city_name,date,occupancy_rate_pct,avg_price_usd,available_rooms,occupied_rooms
Barcelona,2024-01-15,75.5,120.50,70000,52850
Barcelona,2024-01-16,78.2,125.00,70000,54740
"""

    return {
        "filename": "hotel_metrics_template.csv",
        "content": csv_data,
        "content_type": "text/csv"
    }
