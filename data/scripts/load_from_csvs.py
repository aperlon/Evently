"""
Load data from historical CSV files into database
This replaces the dynamic data generation
"""
import sys
import os
from pathlib import Path
from datetime import datetime, date
import pandas as pd

# Add backend to path
backend_path = os.environ.get('BACKEND_PATH', os.path.join(os.path.dirname(__file__), '../../backend'))
if os.path.exists('/app'):  # Inside Docker container
    backend_path = '/app'
sys.path.insert(0, backend_path)

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, Base
from app.models import (
    City, Event, EventType,
    TourismMetric, HotelMetric, EconomicMetric, MobilityMetric
)

# CSV directory
CSV_DIR = Path(__file__).parent.parent / "examples"


def create_database():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def load_cities(db: Session):
    """Load cities from CSV"""
    csv_path = CSV_DIR / "cities.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Cities CSV not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    cities = []
    
    for _, row in df.iterrows():
        city = City(
            name=row['name'],
            country=row['country'],
            country_code=row['country_code'],
            continent=row['continent'],
            latitude=float(row['latitude']),
            longitude=float(row['longitude']),
            timezone=row['timezone'],
            population=int(row['population']),
            area_km2=float(row['area_km2']),
            gdp_usd=float(row['gdp_usd']),
            annual_tourists=int(row['annual_tourists']),
            hotel_rooms=int(row['hotel_rooms']),
            avg_hotel_price_usd=float(row['avg_hotel_price_usd']),
        )
        db.add(city)
        cities.append(city)
    
    db.commit()
    print(f"✓ Loaded {len(cities)} cities from CSV")
    return cities


def load_events(db: Session, cities: list):
    """Load events from CSV"""
    csv_path = CSV_DIR / "events.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Events CSV not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    city_map = {city.name: city for city in cities}
    events = []
    
    for _, row in df.iterrows():
        city_name = row['city']
        city = city_map.get(city_name)
        if not city:
            print(f"⚠️  City '{city_name}' not found, skipping event {row['event_name']}")
            continue
        
        # Map event type
        event_type_str = str(row['event_type']).lower()
        event_type_map = {
            'sports': EventType.SPORTS,
            'music': EventType.MUSIC,
            'culture': EventType.CULTURE,
            'festival': EventType.FESTIVAL,
            'business': EventType.BUSINESS,
        }
        event_type = event_type_map.get(event_type_str, EventType.SPORTS)
        
        event = Event(
            city_id=city.id,
            name=row['event_name'],
            event_type=event_type,
            description=row.get('description', ''),
            start_date=pd.to_datetime(row['start_date']).date(),
            end_date=pd.to_datetime(row['end_date']).date(),
            year=int(row['year']),
            expected_attendance=int(row['expected_attendance']) if pd.notna(row['expected_attendance']) else None,
            actual_attendance=int(row['actual_attendance']) if pd.notna(row['actual_attendance']) else None,
            venue_name=row.get('venue_name', ''),
            venue_capacity=int(row['venue_capacity']) if pd.notna(row.get('venue_capacity')) else None,
            is_recurring=bool(row.get('is_recurring', False)),
            recurrence_pattern=row.get('recurrence_pattern', ''),
            edition_number=int(row['edition_number']) if pd.notna(row.get('edition_number')) else None,
        )
        db.add(event)
        events.append(event)
    
    db.commit()
    print(f"✓ Loaded {len(events)} events from CSV")
    return events


def load_tourism_metrics(db: Session, cities: list):
    """Load tourism metrics from CSV"""
    csv_path = CSV_DIR / "tourism_metrics.csv"
    if not csv_path.exists():
        print("⚠️  Tourism metrics CSV not found, skipping...")
        return 0
    
    df = pd.read_csv(csv_path)
    city_map = {city.name: city for city in cities}
    count = 0
    
    for _, row in df.iterrows():
        city_name = row['city']
        city = city_map.get(city_name)
        if not city:
            continue
        
        metric = TourismMetric(
            city_id=city.id,
            date=pd.to_datetime(row['date']).date(),
            domestic_visitors=int(row['domestic_visitors']),
            international_visitors=int(row['international_visitors']),
            total_visitors=int(row['total_visitors']),
            avg_stay_duration_days=float(row.get('avg_stay_duration_days', 3.5)),
            avg_spending_per_visitor_usd=float(row.get('avg_spending_per_visitor_usd', 280)),
            event_visitors_pct=float(row.get('event_visitors_pct', 0.0)),
        )
        db.add(metric)
        count += 1
        
        # Batch commit every 1000 records
        if count % 1000 == 0:
            db.commit()
    
    db.commit()
    print(f"✓ Loaded {count} tourism metrics from CSV")
    return count


def load_hotel_metrics(db: Session, cities: list):
    """Load hotel metrics from CSV"""
    csv_path = CSV_DIR / "hotel_metrics.csv"
    if not csv_path.exists():
        print("⚠️  Hotel metrics CSV not found, skipping...")
        return 0
    
    df = pd.read_csv(csv_path)
    city_map = {city.name: city for city in cities}
    count = 0
    
    for _, row in df.iterrows():
        city_name = row['city']
        city = city_map.get(city_name)
        if not city:
            continue
        
        metric = HotelMetric(
            city_id=city.id,
            date=pd.to_datetime(row['date']).date(),
            occupancy_rate_pct=float(row['occupancy_rate_pct']),
            available_rooms=int(row.get('available_rooms', city.hotel_rooms)),
            occupied_rooms=int(row.get('occupied_rooms', city.hotel_rooms * float(row['occupancy_rate_pct']) / 100)),
            avg_price_usd=float(row['avg_price_usd']),
            median_price_usd=float(row.get('median_price_usd', row['avg_price_usd'] * 0.9)),
            min_price_usd=float(row.get('min_price_usd', row['avg_price_usd'] * 0.5)),
            max_price_usd=float(row.get('max_price_usd', row['avg_price_usd'] * 2.5)),
        )
        db.add(metric)
        count += 1
        
        if count % 1000 == 0:
            db.commit()
    
    db.commit()
    print(f"✓ Loaded {count} hotel metrics from CSV")
    return count


def load_economic_metrics(db: Session, cities: list):
    """Load economic metrics from CSV"""
    csv_path = CSV_DIR / "economic_metrics.csv"
    if not csv_path.exists():
        print("⚠️  Economic metrics CSV not found, skipping...")
        return 0
    
    df = pd.read_csv(csv_path)
    city_map = {city.name: city for city in cities}
    count = 0
    
    for _, row in df.iterrows():
        city_name = row['city']
        city = city_map.get(city_name)
        if not city:
            continue
        
        metric = EconomicMetric(
            city_id=city.id,
            date=pd.to_datetime(row['date']).date(),
            total_spending_usd=float(row['total_spending_usd']),
            accommodation_spending_usd=float(row.get('accommodation_spending_usd', row['total_spending_usd'] * 0.35)),
            food_beverage_spending_usd=float(row.get('food_beverage_spending_usd', row['total_spending_usd'] * 0.25)),
            retail_spending_usd=float(row.get('retail_spending_usd', row['total_spending_usd'] * 0.20)),
            entertainment_spending_usd=float(row.get('entertainment_spending_usd', row['total_spending_usd'] * 0.12)),
            transport_spending_usd=float(row.get('transport_spending_usd', row['total_spending_usd'] * 0.08)),
        )
        db.add(metric)
        count += 1
        
        if count % 1000 == 0:
            db.commit()
    
    db.commit()
    print(f"✓ Loaded {count} economic metrics from CSV")
    return count


def load_mobility_metrics(db: Session, cities: list):
    """Load mobility metrics from CSV"""
    csv_path = CSV_DIR / "mobility_metrics.csv"
    if not csv_path.exists():
        print("⚠️  Mobility metrics CSV not found, skipping...")
        return 0
    
    df = pd.read_csv(csv_path)
    city_map = {city.name: city for city in cities}
    count = 0
    
    for _, row in df.iterrows():
        city_name = row['city']
        city = city_map.get(city_name)
        if not city:
            continue
        
        metric = MobilityMetric(
            city_id=city.id,
            date=pd.to_datetime(row['date']).date(),
            airport_arrivals=int(row.get('airport_arrivals', 0)),
            airport_departures=int(row.get('airport_departures', 0)),
            international_flights=int(row.get('international_flights', 0)),
            domestic_flights=int(row.get('domestic_flights', 0)),
            public_transport_usage=int(row.get('public_transport_usage', 0)),
            traffic_congestion_index=float(row.get('traffic_congestion_index', 5.5)),
        )
        db.add(metric)
        count += 1
        
        if count % 1000 == 0:
            db.commit()
    
    db.commit()
    print(f"✓ Loaded {count} mobility metrics from CSV")
    return count


def main():
    """Main function to load all data from CSVs"""
    print("\n🚀 Evently CSV Data Loader")
    print("=" * 60)
    print(f"📁 CSV directory: {CSV_DIR}")
    
    if not CSV_DIR.exists():
        print(f"❌ CSV directory not found: {CSV_DIR}")
        print("   Run generate_historical_csvs.py first to create CSV files")
        return
    
    # Create database
    create_database()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Load cities
        cities = load_cities(db)
        
        # Load events
        events = load_events(db, cities)
        
        # Load metrics
        print("\n📊 Loading metrics...")
        tourism_count = load_tourism_metrics(db, cities)
        hotel_count = load_hotel_metrics(db, cities)
        economic_count = load_economic_metrics(db, cities)
        mobility_count = load_mobility_metrics(db, cities)
        
        print("\n" + "=" * 60)
        print("✅ Data loading completed!")
        print(f"   - Cities: {len(cities)}")
        print(f"   - Events: {len(events)}")
        print(f"   - Tourism metrics: {tourism_count:,}")
        print(f"   - Hotel metrics: {hotel_count:,}")
        print(f"   - Economic metrics: {economic_count:,}")
        print(f"   - Mobility metrics: {mobility_count:,}")
        print("=" * 60)
        
        # Train regression model automatically
        print("\n🤖 Training regression model from CSV data...")
        try:
            from app.ml.economic_impact_model import EconomicImpactModel
            model = EconomicImpactModel()
            model.load_data()
            model.train()
            model.save()
            print("   ✅ Regression model trained and saved")
        except Exception as e:
            print(f"   ⚠️  Could not train model: {e}")
            print("   You can train it manually later: python data/scripts/train_models.py")
        
        print("\n💡 Next steps:")
        print("   1. Start API: uvicorn app.main:app --reload")
        print("   2. Access docs: http://localhost:8000/api/v1/docs")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

