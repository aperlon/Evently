"""
Generate historical CSV files with realistic random data
These CSVs will be used instead of generating data dynamically
"""
import sys
import os
from pathlib import Path
from datetime import date, timedelta
import random
import numpy as np
import pandas as pd

# Add backend to path
backend_path = os.environ.get('BACKEND_PATH', os.path.join(os.path.dirname(__file__), '../../backend'))
if os.path.exists('/app'):  # Inside Docker container
    backend_path = '/app'
sys.path.insert(0, backend_path)

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "examples"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Year to generate data for
YEAR = 2024
START_DATE = date(YEAR, 1, 1)
END_DATE = date(YEAR, 12, 31)

# Cities data (same as in generate_sample_data.py)
CITIES_DATA = [
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
    {
        "name": "Rio de Janeiro",
        "country": "Brazil",
        "country_code": "BRA",
        "continent": "South America",
        "latitude": -22.9068,
        "longitude": -43.1729,
        "timezone": "America/Sao_Paulo",
        "population": 6748000,
        "area_km2": 1200,
        "gdp_usd": 205000000000,
        "annual_tourists": 2820000,
        "hotel_rooms": 45000,
        "avg_hotel_price_usd": 120,
    },
    {
        "name": "São Paulo",
        "country": "Brazil",
        "country_code": "BRA",
        "continent": "South America",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "timezone": "America/Sao_Paulo",
        "population": 12300000,
        "area_km2": 1521,
        "gdp_usd": 430000000000,
        "annual_tourists": 15400000,
        "hotel_rooms": 98000,
        "avg_hotel_price_usd": 135,
    },
    {
        "name": "Dubai",
        "country": "United Arab Emirates",
        "country_code": "ARE",
        "continent": "Asia",
        "latitude": 25.2048,
        "longitude": 55.2708,
        "timezone": "Asia/Dubai",
        "population": 3400000,
        "area_km2": 4114,
        "gdp_usd": 108000000000,
        "annual_tourists": 16700000,
        "hotel_rooms": 120000,
        "avg_hotel_price_usd": 200,
    },
    {
        "name": "Singapore",
        "country": "Singapore",
        "country_code": "SGP",
        "continent": "Asia",
        "latitude": 1.3521,
        "longitude": 103.8198,
        "timezone": "Asia/Singapore",
        "population": 5700000,
        "area_km2": 728,
        "gdp_usd": 397000000000,
        "annual_tourists": 19100000,
        "hotel_rooms": 65000,
        "avg_hotel_price_usd": 220,
    },
    {
        "name": "Sydney",
        "country": "Australia",
        "country_code": "AUS",
        "continent": "Oceania",
        "latitude": -33.8688,
        "longitude": 151.2093,
        "timezone": "Australia/Sydney",
        "population": 5300000,
        "area_km2": 12368,
        "gdp_usd": 337000000000,
        "annual_tourists": 16200000,
        "hotel_rooms": 55000,
        "avg_hotel_price_usd": 190,
    },
    {
        "name": "Los Angeles",
        "country": "United States",
        "country_code": "USA",
        "continent": "North America",
        "latitude": 34.0522,
        "longitude": -118.2437,
        "timezone": "America/Los_Angeles",
        "population": 3900000,
        "area_km2": 1302,
        "gdp_usd": 1000000000000,
        "annual_tourists": 50000000,
        "hotel_rooms": 115000,
        "avg_hotel_price_usd": 220,
    },
    {
        "name": "Chicago",
        "country": "United States",
        "country_code": "USA",
        "continent": "North America",
        "latitude": 41.8781,
        "longitude": -87.6298,
        "timezone": "America/Chicago",
        "population": 2700000,
        "area_km2": 606,
        "gdp_usd": 689000000000,
        "annual_tourists": 57000000,
        "hotel_rooms": 45000,
        "avg_hotel_price_usd": 180,
    },
    {
        "name": "Miami",
        "country": "United States",
        "country_code": "USA",
        "continent": "North America",
        "latitude": 25.7617,
        "longitude": -80.1918,
        "timezone": "America/New_York",
        "population": 470000,
        "area_km2": 143,
        "gdp_usd": 345000000000,
        "annual_tourists": 24200000,
        "hotel_rooms": 95000,
        "avg_hotel_price_usd": 195,
    },
    {
        "name": "Barcelona",
        "country": "Spain",
        "country_code": "ESP",
        "continent": "Europe",
        "latitude": 41.3874,
        "longitude": 2.1686,
        "timezone": "Europe/Madrid",
        "population": 1620000,
        "area_km2": 101,
        "gdp_usd": 156000000000,
        "annual_tourists": 9000000,
        "hotel_rooms": 70000,
        "avg_hotel_price_usd": 150,
    },
    {
        "name": "Amsterdam",
        "country": "Netherlands",
        "country_code": "NLD",
        "continent": "Europe",
        "latitude": 52.3676,
        "longitude": 4.9041,
        "timezone": "Europe/Amsterdam",
        "population": 872680,
        "area_km2": 219,
        "gdp_usd": 96000000000,
        "annual_tourists": 8700000,
        "hotel_rooms": 35000,
        "avg_hotel_price_usd": 180,
    },
]

# Events data
EVENTS_DATA = [
    {"city": "London", "name": "London Marathon 2024", "event_type": "sports",
     "start_date": date(2024, 4, 21), "end_date": date(2024, 4, 21),
     "expected_attendance": 50000, "actual_attendance": 48000},
    {"city": "London", "name": "Wimbledon 2024", "event_type": "sports",
     "start_date": date(2024, 7, 1), "end_date": date(2024, 7, 14),
     "expected_attendance": 500000, "actual_attendance": 512000},
    {"city": "Tokyo", "name": "Tokyo Marathon 2024", "event_type": "sports",
     "start_date": date(2024, 3, 3), "end_date": date(2024, 3, 3),
     "expected_attendance": 38000, "actual_attendance": 37500},
    {"city": "Tokyo", "name": "Tokyo Game Show 2024", "event_type": "culture",
     "start_date": date(2024, 9, 26), "end_date": date(2024, 9, 29),
     "expected_attendance": 200000, "actual_attendance": 185000},
    {"city": "Paris", "name": "Roland Garros 2024", "event_type": "sports",
     "start_date": date(2024, 5, 26), "end_date": date(2024, 6, 9),
     "expected_attendance": 600000, "actual_attendance": 620000},
    {"city": "Paris", "name": "Paris Fashion Week 2024", "event_type": "culture",
     "start_date": date(2024, 9, 23), "end_date": date(2024, 10, 1),
     "expected_attendance": 100000, "actual_attendance": 105000},
    {"city": "New York", "name": "NYC Marathon 2024", "event_type": "sports",
     "start_date": date(2024, 11, 3), "end_date": date(2024, 11, 3),
     "expected_attendance": 55000, "actual_attendance": 53000},
    {"city": "New York", "name": "US Open 2024", "event_type": "sports",
     "start_date": date(2024, 8, 26), "end_date": date(2024, 9, 8),
     "expected_attendance": 850000, "actual_attendance": 890000},
    {"city": "Madrid", "name": "Champions League Final 2024", "event_type": "sports",
     "start_date": date(2024, 6, 1), "end_date": date(2024, 6, 1),
     "expected_attendance": 70000, "actual_attendance": 71000},
    {"city": "Madrid", "name": "Mad Cool Festival 2024", "event_type": "music",
     "start_date": date(2024, 7, 10), "end_date": date(2024, 7, 13),
     "expected_attendance": 240000, "actual_attendance": 252000},
    {"city": "Berlin", "name": "Berlin Marathon 2024", "event_type": "sports",
     "start_date": date(2024, 9, 29), "end_date": date(2024, 9, 29),
     "expected_attendance": 50000, "actual_attendance": 49500},
    {"city": "Berlin", "name": "Berlin Festival of Lights 2024", "event_type": "festival",
     "start_date": date(2024, 10, 4), "end_date": date(2024, 10, 13),
     "expected_attendance": 2000000, "actual_attendance": 2100000},
]


def generate_baseline_metrics(city_data, start_date, end_date):
    """Generate baseline metrics for a city (no events)"""
    metrics = {
        'tourism': [],
        'hotel': [],
        'economic': [],
        'mobility': []
    }
    
    current_date = start_date
    while current_date <= end_date:
        day_of_week = current_date.weekday()
        is_weekend = day_of_week >= 5
        day_of_year = current_date.timetuple().tm_yday
        
        # Seasonal variation
        seasonal_variation = 1 + 0.2 * np.sin(2 * np.pi * day_of_year / 365)
        
        # Base visitors
        base_visitors = int(city_data['annual_tourists'] / 365)
        weekend_multiplier = 1.3 if is_weekend else 1.0
        total_visitors = int(base_visitors * weekend_multiplier * seasonal_variation * (0.9 + random.random() * 0.2))
        
        # Tourism metrics
        metrics['tourism'].append({
            'city': city_data['name'],
            'date': current_date.isoformat(),
            'domestic_visitors': int(total_visitors * 0.6),
            'international_visitors': int(total_visitors * 0.4),
            'total_visitors': total_visitors,
            'avg_stay_duration_days': round(3.5 + random.random() * 0.5, 1),
            'avg_spending_per_visitor_usd': int(280 * (0.9 + random.random() * 0.2)),
            'event_visitors_pct': 0.0,
        })
        
        # Hotel metrics
        base_occupancy = 65 + (10 if is_weekend else 0)
        occupancy_rate = min(95, base_occupancy * seasonal_variation * (0.95 + random.random() * 0.1))
        avg_price = city_data['avg_hotel_price_usd'] * (1.1 if is_weekend else 1.0) * (0.95 + random.random() * 0.1)
        
        metrics['hotel'].append({
            'city': city_data['name'],
            'date': current_date.isoformat(),
            'occupancy_rate_pct': round(occupancy_rate, 1),
            'available_rooms': city_data['hotel_rooms'],
            'occupied_rooms': int(city_data['hotel_rooms'] * occupancy_rate / 100),
            'avg_price_usd': round(avg_price, 2),
            'median_price_usd': round(avg_price * 0.9, 2),
            'min_price_usd': round(avg_price * 0.5, 2),
            'max_price_usd': round(avg_price * 2.5, 2),
        })
        
        # Economic metrics
        daily_spending = total_visitors * 280
        
        metrics['economic'].append({
            'city': city_data['name'],
            'date': current_date.isoformat(),
            'total_spending_usd': int(daily_spending * (0.9 + random.random() * 0.2)),
            'accommodation_spending_usd': int(daily_spending * 0.35 * (0.9 + random.random() * 0.2)),
            'food_beverage_spending_usd': int(daily_spending * 0.25 * (0.9 + random.random() * 0.2)),
            'retail_spending_usd': int(daily_spending * 0.20 * (0.9 + random.random() * 0.2)),
            'entertainment_spending_usd': int(daily_spending * 0.12 * (0.9 + random.random() * 0.2)),
            'transport_spending_usd': int(daily_spending * 0.08 * (0.9 + random.random() * 0.2)),
        })
        
        # Mobility metrics
        metrics['mobility'].append({
            'city': city_data['name'],
            'date': current_date.isoformat(),
            'airport_arrivals': int(total_visitors * 0.7 * (0.9 + random.random() * 0.2)),
            'airport_departures': int(total_visitors * 0.7 * (0.9 + random.random() * 0.2)),
            'international_flights': int(total_visitors * 0.4 / 150 * (0.9 + random.random() * 0.2)),
            'domestic_flights': int(total_visitors * 0.3 / 120 * (0.9 + random.random() * 0.2)),
            'public_transport_usage': int(city_data['population'] * 0.4 * (0.9 + random.random() * 0.2)),
            'traffic_congestion_index': round(5.5 + (1.5 if is_weekend else 0) + random.random() * 0.5, 1),
        })
        
        current_date += timedelta(days=1)
    
    return metrics


def generate_event_metrics(city_data, event_data, metrics_dict):
    """Generate elevated metrics during event period"""
    current_date = event_data['start_date']
    event_duration = (event_data['end_date'] - event_data['start_date']).days + 1
    attendance = event_data.get('actual_attendance') or event_data.get('expected_attendance') or 10000
    
    attendance_ratio = attendance / 10000
    visitor_multiplier = 1 + (0.3 * min(attendance_ratio, 5))
    price_multiplier = 1 + (0.2 * min(attendance_ratio, 3))
    
    while current_date <= event_data['end_date']:
        base_visitors = int(city_data['annual_tourists'] / 365)
        total_visitors = int(base_visitors * visitor_multiplier * (0.95 + random.random() * 0.1))
        
        # Overwrite tourism metrics
        for i, tm in enumerate(metrics_dict['tourism']):
            if tm['city'] == city_data['name'] and tm['date'] == current_date.isoformat():
                metrics_dict['tourism'][i] = {
                    'city': city_data['name'],
                    'date': current_date.isoformat(),
                    'domestic_visitors': int(total_visitors * 0.5),
                    'international_visitors': int(total_visitors * 0.5),
                    'total_visitors': total_visitors,
                    'avg_stay_duration_days': round(4.5 + random.random() * 0.5, 1),
                    'avg_spending_per_visitor_usd': int(350 * (0.95 + random.random() * 0.1)),
                    'event_visitors_pct': round(40.0 + random.random() * 10, 1),
                }
                break
        
        # Overwrite hotel metrics
        occupancy_rate = min(95, 85 + random.uniform(-5, 5))
        avg_price = city_data['avg_hotel_price_usd'] * price_multiplier * (0.95 + random.random() * 0.1)
        
        for i, hm in enumerate(metrics_dict['hotel']):
            if hm['city'] == city_data['name'] and hm['date'] == current_date.isoformat():
                metrics_dict['hotel'][i] = {
                    'city': city_data['name'],
                    'date': current_date.isoformat(),
                    'occupancy_rate_pct': round(occupancy_rate, 1),
                    'available_rooms': city_data['hotel_rooms'],
                    'occupied_rooms': int(city_data['hotel_rooms'] * occupancy_rate / 100),
                    'avg_price_usd': round(avg_price, 2),
                    'median_price_usd': round(avg_price * 0.9, 2),
                    'min_price_usd': round(avg_price * 0.6, 2),
                    'max_price_usd': round(avg_price * 3.5, 2),
                }
                break
        
        # Overwrite economic metrics
        daily_spending = total_visitors * 350
        
        for i, em in enumerate(metrics_dict['economic']):
            if em['city'] == city_data['name'] and em['date'] == current_date.isoformat():
                metrics_dict['economic'][i] = {
                    'city': city_data['name'],
                    'date': current_date.isoformat(),
                    'total_spending_usd': int(daily_spending * (0.95 + random.random() * 0.1)),
                    'accommodation_spending_usd': int(daily_spending * 0.40 * (0.95 + random.random() * 0.1)),
                    'food_beverage_spending_usd': int(daily_spending * 0.22 * (0.95 + random.random() * 0.1)),
                    'retail_spending_usd': int(daily_spending * 0.18 * (0.95 + random.random() * 0.1)),
                    'entertainment_spending_usd': int(daily_spending * 0.15 * (0.95 + random.random() * 0.1)),
                    'transport_spending_usd': int(daily_spending * 0.05 * (0.95 + random.random() * 0.1)),
                }
                break
        
        # Overwrite mobility metrics
        for i, mm in enumerate(metrics_dict['mobility']):
            if mm['city'] == city_data['name'] and mm['date'] == current_date.isoformat():
                metrics_dict['mobility'][i] = {
                    'city': city_data['name'],
                    'date': current_date.isoformat(),
                    'airport_arrivals': int(total_visitors * 0.8 * (0.95 + random.random() * 0.1)),
                    'airport_departures': int(total_visitors * 0.6 * (0.95 + random.random() * 0.1)),
                    'international_flights': int(total_visitors * 0.5 / 150 * (0.95 + random.random() * 0.1)),
                    'domestic_flights': int(total_visitors * 0.3 / 120 * (0.95 + random.random() * 0.1)),
                    'public_transport_usage': int(city_data['population'] * 0.6 * (0.95 + random.random() * 0.1)),
                    'traffic_congestion_index': round(8.5 + random.random() * 0.5, 1),
                }
                break
        
        current_date += timedelta(days=1)


def main():
    """Generate all historical CSV files"""
    print("\n🚀 Generating Historical CSV Files")
    print("=" * 60)
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"📅 Year: {YEAR}")
    print(f"🏙️  Cities: {len(CITIES_DATA)}")
    print(f"🎪 Events: {len(EVENTS_DATA)}")
    print("=" * 60)
    
    # 1. Generate cities CSV
    print("\n1️⃣ Generating cities.csv...")
    cities_df = pd.DataFrame(CITIES_DATA)
    cities_df.to_csv(OUTPUT_DIR / "cities.csv", index=False)
    print(f"   ✅ Created cities.csv with {len(cities_df)} cities")
    
    # 2. Generate events CSV
    print("\n2️⃣ Generating events.csv...")
    events_list = []
    for event in EVENTS_DATA:
        city_name = event['city']
        city_data = next(c for c in CITIES_DATA if c['name'] == city_name)
        
        events_list.append({
            'event_name': event['name'],
            'city': city_name,
            'event_type': event['event_type'],
            'description': f"Major {event['event_type']} event in {city_name}",
            'start_date': event['start_date'].isoformat(),
            'end_date': event['end_date'].isoformat(),
            'year': YEAR,
            'expected_attendance': event['expected_attendance'],
            'actual_attendance': event.get('actual_attendance', event['expected_attendance']),
            'venue_name': f"{city_name} City Center",
            'venue_capacity': None,
            'is_recurring': 1,
            'recurrence_pattern': 'annual',
            'edition_number': None,
        })
    
    events_df = pd.DataFrame(events_list)
    events_df.to_csv(OUTPUT_DIR / "events.csv", index=False)
    print(f"   ✅ Created events.csv with {len(events_df)} events")
    
    # 3. Generate metrics for all cities
    print("\n3️⃣ Generating metrics for all cities...")
    all_metrics = {
        'tourism': [],
        'hotel': [],
        'economic': [],
        'mobility': []
    }
    
    for city_data in CITIES_DATA:
        print(f"   📊 Generating metrics for {city_data['name']}...")
        city_metrics = generate_baseline_metrics(city_data, START_DATE, END_DATE)
        
        for metric_type in ['tourism', 'hotel', 'economic', 'mobility']:
            all_metrics[metric_type].extend(city_metrics[metric_type])
    
    # 4. Apply event impacts
    print("\n4️⃣ Applying event impacts...")
    for event_data in EVENTS_DATA:
        city_name = event_data['city']
        city_data = next(c for c in CITIES_DATA if c['name'] == city_name)
        print(f"   🎪 Applying impact for {event_data['name']} in {city_name}...")
        generate_event_metrics(city_data, event_data, all_metrics)
    
    # 5. Save metrics CSVs
    print("\n5️⃣ Saving metrics CSVs...")
    
    tourism_df = pd.DataFrame(all_metrics['tourism'])
    tourism_df.to_csv(OUTPUT_DIR / "tourism_metrics.csv", index=False)
    print(f"   ✅ Created tourism_metrics.csv with {len(tourism_df)} records")
    
    hotel_df = pd.DataFrame(all_metrics['hotel'])
    hotel_df.to_csv(OUTPUT_DIR / "hotel_metrics.csv", index=False)
    print(f"   ✅ Created hotel_metrics.csv with {len(hotel_df)} records")
    
    economic_df = pd.DataFrame(all_metrics['economic'])
    economic_df.to_csv(OUTPUT_DIR / "economic_metrics.csv", index=False)
    print(f"   ✅ Created economic_metrics.csv with {len(economic_df)} records")
    
    mobility_df = pd.DataFrame(all_metrics['mobility'])
    mobility_df.to_csv(OUTPUT_DIR / "mobility_metrics.csv", index=False)
    print(f"   ✅ Created mobility_metrics.csv with {len(mobility_df)} records")
    
    # 6. Generate event_impacts.csv (for regression model)
    print("\n6️⃣ Generating event_impacts.csv...")
    impacts_list = []
    for event in EVENTS_DATA:
        city_name = event['city']
        city_data = next(c for c in CITIES_DATA if c['name'] == city_name)
        attendance = event.get('actual_attendance') or event.get('expected_attendance')
        duration = (event['end_date'] - event['start_date']).days + 1
        
        # Calculate estimated impact (will be refined by regression model)
        base_impact = attendance * 200 * duration  # Rough estimate
        impacts_list.append({
            'event_name': event['name'],
            'city': city_name,
            'event_type': event['event_type'],
            'year': YEAR,
            'attendance': attendance,
            'duration_days': duration,
            'total_economic_impact_usd': int(base_impact * (0.9 + random.random() * 0.2)),
            'jobs_created': int(attendance / 100),
            'roi_ratio': round(3.5 + random.random() * 1.5, 2),
        })
    
    impacts_df = pd.DataFrame(impacts_list)
    impacts_df.to_csv(OUTPUT_DIR / "event_impacts.csv", index=False)
    print(f"   ✅ Created event_impacts.csv with {len(impacts_df)} records")
    
    print("\n" + "=" * 60)
    print("✅ All CSV files generated successfully!")
    print("=" * 60)
    print(f"\n📁 Files created in: {OUTPUT_DIR}")
    print("   - cities.csv")
    print("   - events.csv")
    print("   - tourism_metrics.csv")
    print("   - hotel_metrics.csv")
    print("   - economic_metrics.csv")
    print("   - mobility_metrics.csv")
    print("   - event_impacts.csv")
    print("\n💡 Next step: Run import script to load into database")


if __name__ == "__main__":
    main()

