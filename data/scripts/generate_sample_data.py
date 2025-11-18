"""
Generate sample data for Evently
Creates realistic data for major cities and events
"""
import sys
import os
from datetime import date, timedelta
import random
import numpy as np

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, Base
from app.models import (
    City, Event, EventType,
    TourismMetric, HotelMetric, EconomicMetric, MobilityMetric
)


def create_database():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def create_cities(db: Session):
    """Create sample cities"""
    cities_data = [
        {
            "name": "London",
            "country": "United Kingdom",
            "country_code": "GBR",
            "continent": "Europe",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "timezone": "Europe/London",
            "population": 9000000,
            "area_km2": 1572,
            "gdp_usd": 635000000000,
            "annual_tourists": 19600000,
            "hotel_rooms": 150000,
            "avg_hotel_price_usd": 180,
        },
        {
            "name": "Tokyo",
            "country": "Japan",
            "country_code": "JPN",
            "continent": "Asia",
            "latitude": 35.6762,
            "longitude": 139.6503,
            "timezone": "Asia/Tokyo",
            "population": 14000000,
            "area_km2": 2194,
            "gdp_usd": 1617000000000,
            "annual_tourists": 15200000,
            "hotel_rooms": 180000,
            "avg_hotel_price_usd": 160,
        },
        {
            "name": "Paris",
            "country": "France",
            "country_code": "FRA",
            "continent": "Europe",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "timezone": "Europe/Paris",
            "population": 2200000,
            "area_km2": 105,
            "gdp_usd": 739000000000,
            "annual_tourists": 19100000,
            "hotel_rooms": 78000,
            "avg_hotel_price_usd": 200,
        },
        {
            "name": "New York",
            "country": "United States",
            "country_code": "USA",
            "continent": "North America",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
            "population": 8400000,
            "area_km2": 783,
            "gdp_usd": 1700000000000,
            "annual_tourists": 66600000,
            "hotel_rooms": 120000,
            "avg_hotel_price_usd": 250,
        },
        {
            "name": "Madrid",
            "country": "Spain",
            "country_code": "ESP",
            "continent": "Europe",
            "latitude": 40.4168,
            "longitude": -3.7038,
            "timezone": "Europe/Madrid",
            "population": 3200000,
            "area_km2": 604,
            "gdp_usd": 230000000000,
            "annual_tourists": 10400000,
            "hotel_rooms": 85000,
            "avg_hotel_price_usd": 140,
        },
        {
            "name": "Berlin",
            "country": "Germany",
            "country_code": "DEU",
            "continent": "Europe",
            "latitude": 52.5200,
            "longitude": 13.4050,
            "timezone": "Europe/Berlin",
            "population": 3700000,
            "area_km2": 891,
            "gdp_usd": 192000000000,
            "annual_tourists": 13500000,
            "hotel_rooms": 95000,
            "avg_hotel_price_usd": 130,
        },
    ]

    cities = []
    for city_data in cities_data:
        city = City(**city_data)
        db.add(city)
        cities.append(city)

    db.commit()
    print(f"✓ Created {len(cities)} cities")
    return cities


def create_events(db: Session, cities: list):
    """Create sample events"""
    events_data = [
        # London events
        {
            "city": "London",
            "name": "London Marathon 2024",
            "event_type": EventType.SPORTS,
            "description": "One of the world's largest marathons",
            "start_date": date(2024, 4, 21),
            "end_date": date(2024, 4, 21),
            "expected_attendance": 50000,
            "actual_attendance": 48000,
            "venue_name": "Central London",
            "is_recurring": True,
            "recurrence_pattern": "annual",
            "edition_number": 44,
        },
        {
            "city": "London",
            "name": "Wimbledon 2024",
            "event_type": EventType.SPORTS,
            "description": "Tennis Grand Slam Championship",
            "start_date": date(2024, 7, 1),
            "end_date": date(2024, 7, 14),
            "expected_attendance": 500000,
            "actual_attendance": 512000,
            "venue_name": "All England Club",
            "venue_capacity": 42000,
            "is_recurring": True,
            "recurrence_pattern": "annual",
        },
        # Tokyo events
        {
            "city": "Tokyo",
            "name": "Tokyo Marathon 2024",
            "event_type": EventType.SPORTS,
            "description": "Major international marathon",
            "start_date": date(2024, 3, 3),
            "end_date": date(2024, 3, 3),
            "expected_attendance": 38000,
            "actual_attendance": 37500,
            "is_recurring": True,
            "recurrence_pattern": "annual",
        },
        {
            "city": "Tokyo",
            "name": "Tokyo Design Week 2024",
            "event_type": EventType.CULTURE,
            "description": "International design exhibition",
            "start_date": date(2024, 10, 25),
            "end_date": date(2024, 11, 3),
            "expected_attendance": 150000,
            "venue_name": "Tokyo Big Sight",
            "is_recurring": True,
            "recurrence_pattern": "annual",
        },
        # Paris events
        {
            "city": "Paris",
            "name": "Roland Garros 2024",
            "event_type": EventType.SPORTS,
            "description": "French Open Tennis Championship",
            "start_date": date(2024, 5, 26),
            "end_date": date(2024, 6, 9),
            "expected_attendance": 600000,
            "actual_attendance": 620000,
            "venue_name": "Stade Roland Garros",
            "venue_capacity": 15000,
            "is_recurring": True,
            "recurrence_pattern": "annual",
        },
        {
            "city": "Paris",
            "name": "Paris Fashion Week 2024",
            "event_type": EventType.CULTURE,
            "description": "International fashion event",
            "start_date": date(2024, 9, 23),
            "end_date": date(2024, 10, 1),
            "expected_attendance": 100000,
            "is_recurring": True,
            "recurrence_pattern": "biannual",
        },
        # New York events
        {
            "city": "New York",
            "name": "NYC Marathon 2024",
            "event_type": EventType.SPORTS,
            "description": "World's largest marathon",
            "start_date": date(2024, 11, 3),
            "end_date": date(2024, 11, 3),
            "expected_attendance": 55000,
            "actual_attendance": 53000,
            "venue_name": "New York City",
            "is_recurring": True,
            "recurrence_pattern": "annual",
        },
        {
            "city": "New York",
            "name": "US Open 2024",
            "event_type": EventType.SPORTS,
            "description": "Tennis Grand Slam Championship",
            "start_date": date(2024, 8, 26),
            "end_date": date(2024, 9, 8),
            "expected_attendance": 850000,
            "actual_attendance": 890000,
            "venue_name": "USTA Billie Jean King National Tennis Center",
            "venue_capacity": 23000,
            "is_recurring": True,
            "recurrence_pattern": "annual",
        },
        # Madrid events
        {
            "city": "Madrid",
            "name": "Champions League Final 2024",
            "event_type": EventType.SPORTS,
            "description": "UEFA Champions League Final",
            "start_date": date(2024, 6, 1),
            "end_date": date(2024, 6, 1),
            "expected_attendance": 70000,
            "actual_attendance": 71000,
            "venue_name": "Santiago Bernabéu Stadium",
            "venue_capacity": 81000,
            "is_recurring": False,
        },
        {
            "city": "Madrid",
            "name": "Mad Cool Festival 2024",
            "event_type": EventType.MUSIC,
            "description": "International music festival",
            "start_date": date(2024, 7, 10),
            "end_date": date(2024, 7, 13),
            "expected_attendance": 240000,
            "actual_attendance": 252000,
            "is_recurring": True,
            "recurrence_pattern": "annual",
        },
        # Berlin events
        {
            "city": "Berlin",
            "name": "Berlin Marathon 2024",
            "event_type": EventType.SPORTS,
            "description": "World record marathon course",
            "start_date": date(2024, 9, 29),
            "end_date": date(2024, 9, 29),
            "expected_attendance": 50000,
            "actual_attendance": 49500,
            "is_recurring": True,
            "recurrence_pattern": "annual",
        },
        {
            "city": "Berlin",
            "name": "Berlin Festival of Lights 2024",
            "event_type": EventType.FESTIVAL,
            "description": "Light art festival",
            "start_date": date(2024, 10, 4),
            "end_date": date(2024, 10, 13),
            "expected_attendance": 2000000,
            "is_recurring": True,
            "recurrence_pattern": "annual",
        },
    ]

    city_map = {city.name: city for city in cities}
    events = []

    for event_data in events_data:
        city_name = event_data.pop("city")
        city = city_map.get(city_name)
        if not city:
            continue

        event_data["city_id"] = city.id
        event_data["year"] = event_data["start_date"].year

        event = Event(**event_data)
        db.add(event)
        events.append(event)

    db.commit()
    print(f"✓ Created {len(events)} events")
    return events


def generate_baseline_metrics(
    city: City,
    start_date: date,
    end_date: date,
    db: Session
):
    """Generate baseline metrics for a city (no events)"""
    current_date = start_date

    while current_date <= end_date:
        # Tourism metrics with realistic patterns
        day_of_week = current_date.weekday()
        is_weekend = day_of_week >= 5

        # Base visitors with weekend boost
        base_visitors = int(city.annual_tourists / 365)
        weekend_multiplier = 1.3 if is_weekend else 1.0
        seasonal_variation = 1 + 0.2 * np.sin(2 * np.pi * current_date.timetuple().tm_yday / 365)

        total_visitors = int(base_visitors * weekend_multiplier * seasonal_variation)

        tourism = TourismMetric(
            city_id=city.id,
            date=current_date,
            domestic_visitors=int(total_visitors * 0.6),
            international_visitors=int(total_visitors * 0.4),
            total_visitors=total_visitors,
            avg_stay_duration_days=3.5,
            avg_spending_per_visitor_usd=280,
        )
        db.add(tourism)

        # Hotel metrics
        base_occupancy = 65 + (10 if is_weekend else 0)
        occupancy_rate = min(95, base_occupancy * seasonal_variation)

        hotel = HotelMetric(
            city_id=city.id,
            date=current_date,
            occupancy_rate_pct=occupancy_rate,
            available_rooms=city.hotel_rooms,
            occupied_rooms=int(city.hotel_rooms * occupancy_rate / 100),
            avg_price_usd=city.avg_hotel_price_usd * (1.1 if is_weekend else 1.0),
            median_price_usd=city.avg_hotel_price_usd * 0.9,
            min_price_usd=city.avg_hotel_price_usd * 0.5,
            max_price_usd=city.avg_hotel_price_usd * 2.5,
        )
        db.add(hotel)

        # Economic metrics
        daily_spending = total_visitors * 280

        economic = EconomicMetric(
            city_id=city.id,
            date=current_date,
            total_spending_usd=daily_spending,
            accommodation_spending_usd=daily_spending * 0.35,
            food_beverage_spending_usd=daily_spending * 0.25,
            retail_spending_usd=daily_spending * 0.20,
            entertainment_spending_usd=daily_spending * 0.12,
            transport_spending_usd=daily_spending * 0.08,
        )
        db.add(economic)

        # Mobility metrics
        mobility = MobilityMetric(
            city_id=city.id,
            date=current_date,
            airport_arrivals=int(total_visitors * 0.7),
            airport_departures=int(total_visitors * 0.7),
            international_flights=int(total_visitors * 0.4 / 150),
            domestic_flights=int(total_visitors * 0.3 / 120),
            public_transport_usage=int(city.population * 0.4),
            traffic_congestion_index=5.5 + (1.5 if is_weekend else 0),
        )
        db.add(mobility)

        current_date += timedelta(days=1)


def generate_event_period_metrics(
    event: Event,
    city: City,
    db: Session
):
    """Generate elevated metrics during event period"""
    current_date = event.start_date
    event_duration = (event.end_date - event.start_date).days + 1

    # Calculate impact multipliers based on event size
    attendance_ratio = (event.actual_attendance or event.expected_attendance or 10000) / 10000
    visitor_multiplier = 1 + (0.3 * min(attendance_ratio, 5))
    price_multiplier = 1 + (0.2 * min(attendance_ratio, 3))

    while current_date <= event.end_date:
        # Tourism metrics - elevated
        base_visitors = int(city.annual_tourists / 365)
        total_visitors = int(base_visitors * visitor_multiplier)

        tourism = TourismMetric(
            city_id=city.id,
            date=current_date,
            domestic_visitors=int(total_visitors * 0.5),
            international_visitors=int(total_visitors * 0.5),
            total_visitors=total_visitors,
            avg_stay_duration_days=4.5,
            avg_spending_per_visitor_usd=350,
            event_visitors_pct=40.0,
        )
        db.add(tourism)

        # Hotel metrics - elevated prices and occupancy
        occupancy_rate = min(95, 85 + random.uniform(-5, 5))

        hotel = HotelMetric(
            city_id=city.id,
            date=current_date,
            occupancy_rate_pct=occupancy_rate,
            available_rooms=city.hotel_rooms,
            occupied_rooms=int(city.hotel_rooms * occupancy_rate / 100),
            avg_price_usd=city.avg_hotel_price_usd * price_multiplier,
            median_price_usd=city.avg_hotel_price_usd * price_multiplier * 0.9,
            min_price_usd=city.avg_hotel_price_usd * 0.6,
            max_price_usd=city.avg_hotel_price_usd * 3.5,
        )
        db.add(hotel)

        # Economic metrics - elevated spending
        daily_spending = total_visitors * 350

        economic = EconomicMetric(
            city_id=city.id,
            date=current_date,
            total_spending_usd=daily_spending,
            accommodation_spending_usd=daily_spending * 0.40,
            food_beverage_spending_usd=daily_spending * 0.22,
            retail_spending_usd=daily_spending * 0.18,
            entertainment_spending_usd=daily_spending * 0.15,
            transport_spending_usd=daily_spending * 0.05,
            temporary_jobs_created=int((event.actual_attendance or event.expected_attendance) / 100),
        )
        db.add(economic)

        # Mobility metrics - elevated
        mobility = MobilityMetric(
            city_id=city.id,
            date=current_date,
            airport_arrivals=int(total_visitors * 0.8),
            airport_departures=int(total_visitors * 0.6),
            international_flights=int(total_visitors * 0.5 / 150),
            domestic_flights=int(total_visitors * 0.3 / 120),
            public_transport_usage=int(city.population * 0.6),
            traffic_congestion_index=8.5,
        )
        db.add(mobility)

        current_date += timedelta(days=1)


def generate_all_metrics(db: Session, cities: list, events: list):
    """Generate metrics for all cities and events"""
    for city in cities:
        print(f"Generating metrics for {city.name}...")

        # Generate baseline for 2024
        generate_baseline_metrics(
            city,
            date(2024, 1, 1),
            date(2024, 12, 31),
            db
        )

    # Overwrite event periods with elevated metrics
    for event in events:
        print(f"Generating event metrics for {event.name}...")
        city = db.query(City).filter(City.id == event.city_id).first()

        # Delete baseline metrics for event period
        db.query(TourismMetric).filter(
            TourismMetric.city_id == city.id,
            TourismMetric.date >= event.start_date,
            TourismMetric.date <= event.end_date
        ).delete()

        db.query(HotelMetric).filter(
            HotelMetric.city_id == city.id,
            HotelMetric.date >= event.start_date,
            HotelMetric.date <= event.end_date
        ).delete()

        db.query(EconomicMetric).filter(
            EconomicMetric.city_id == city.id,
            EconomicMetric.date >= event.start_date,
            EconomicMetric.date <= event.end_date
        ).delete()

        db.query(MobilityMetric).filter(
            MobilityMetric.city_id == city.id,
            MobilityMetric.date >= event.start_date,
            MobilityMetric.date <= event.end_date
        ).delete()

        # Generate event period metrics
        generate_event_period_metrics(event, city, db)

    db.commit()
    print("✓ Generated all metrics")


def main():
    """Main function to generate all sample data"""
    print("\n🚀 Evently Sample Data Generator\n")
    print("=" * 50)

    # Create database
    create_database()

    # Create session
    db = SessionLocal()

    try:
        # Create cities
        cities = create_cities(db)

        # Create events
        events = create_events(db, cities)

        # Generate metrics
        generate_all_metrics(db, cities, events)

        print("\n" + "=" * 50)
        print("✅ Sample data generation completed!")
        print(f"   - Cities: {len(cities)}")
        print(f"   - Events: {len(events)}")
        print(f"   - Metrics: Generated for full year 2024")
        print("\n💡 Next steps:")
        print("   1. Start the API: cd backend && uvicorn app.main:app --reload")
        print("   2. Access docs: http://localhost:8000/api/v1/docs")
        print("   3. Analyze events using the /events/{id}/impact endpoint")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
