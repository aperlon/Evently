"""
Import real CSV data into PostgreSQL database
Handles data from multiple sources and normalizes to Evently schema
"""
import sys
import os
from pathlib import Path
from datetime import datetime, date
import pandas as pd
import numpy as np

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from app.core.database import SessionLocal, engine, Base
from app.models import (
    City, Event, EventType,
    TourismMetric, HotelMetric, EconomicMetric, MobilityMetric
)

SOURCES_DIR = Path(__file__).parent.parent / "sources"


class DataImporter:
    """Import and normalize data from various sources"""

    def __init__(self, db):
        self.db = db
        self.city_map = {}
        self.stats = {
            "cities_created": 0,
            "events_created": 0,
            "tourism_metrics": 0,
            "hotel_metrics": 0,
            "economic_metrics": 0,
            "mobility_metrics": 0,
            "errors": 0
        }

    def get_or_create_city(self, name: str, **kwargs) -> City:
        """Get existing city or create new one"""
        if name in self.city_map:
            return self.city_map[name]

        city = self.db.query(City).filter(City.name == name).first()
        if not city:
            city = City(name=name, **kwargs)
            self.db.add(city)
            self.db.commit()
            self.stats["cities_created"] += 1
            print(f"  ✅ Created city: {name}")

        self.city_map[name] = city
        return city

    def import_worldbank_tourism(self):
        """Import World Bank tourism arrivals data"""
        print("\n🌍 Importing World Bank Tourism Data...")

        wb_dir = SOURCES_DIR / "worldbank"
        if not wb_dir.exists():
            print("  ⚠️  Directory not found")
            return

        # Look for CSV files in extracted ZIP
        csv_files = list(wb_dir.glob("**/API_ST.INT.ARVL*.csv"))

        if not csv_files:
            print("  ⚠️  No arrivals CSV found")
            return

        # World Bank CSVs have metadata in first few rows
        df = pd.read_csv(csv_files[0], skiprows=4)

        # Country mapping to our cities
        country_to_cities = {
            "United Kingdom": "London",
            "France": "Paris",
            "Spain": "Madrid",
            "United States": "New York",
            "Japan": "Tokyo",
            "Brazil": "Rio de Janeiro",
            "Germany": "Berlin",
            "United Arab Emirates": "Dubai",
            "Singapore": "Singapore",
            "Australia": "Sydney",
            "Netherlands": "Amsterdam",
        }

        for _, row in df.iterrows():
            country_name = row["Country Name"]
            if country_name not in country_to_cities:
                continue

            city_name = country_to_cities[country_name]

            # Get city (create if needed with defaults)
            city = self.get_or_create_city(
                city_name,
                country=country_name,
                country_code=row["Country Code"],
                continent="Unknown",  # Will be updated later
                latitude=0.0,
                longitude=0.0,
                timezone="UTC",
                population=1000000,
            )

            # Import tourism metrics by year
            for year in range(2015, 2025):
                col_name = str(year)
                if col_name not in df.columns:
                    continue

                arrivals = row[col_name]
                if pd.isna(arrivals) or arrivals == 0:
                    continue

                # Create annual metric (we'll use Jan 1st of each year)
                metric_date = date(year, 1, 1)

                # Check if metric exists
                existing = self.db.query(TourismMetric).filter(
                    TourismMetric.city_id == city.id,
                    TourismMetric.date == metric_date
                ).first()

                if existing:
                    existing.total_visitors = int(arrivals)
                else:
                    metric = TourismMetric(
                        city_id=city.id,
                        date=metric_date,
                        total_visitors=int(arrivals),
                        international_visitors=int(arrivals * 0.7),  # Estimate
                        domestic_visitors=int(arrivals * 0.3),
                        avg_spending_per_visitor_usd=300,  # Default estimate
                    )
                    self.db.add(metric)
                    self.stats["tourism_metrics"] += 1

        self.db.commit()
        print(f"  ✅ Imported {self.stats['tourism_metrics']} tourism metrics")

    def import_google_mobility(self):
        """Import Google Mobility Reports"""
        print("\n📱 Importing Google Mobility Data...")

        mobility_file = SOURCES_DIR / "google_mobility" / "global_mobility_report.csv"
        if not mobility_file.exists():
            print("  ⚠️  Mobility file not found")
            return

        # Read CSV (large file, so chunk it)
        print("  📖 Reading mobility data (this may take a minute)...")
        df = pd.read_csv(mobility_file, low_memory=False)

        # Filter for our cities
        city_filters = {
            "London": ("United Kingdom", "England"),
            "Paris": ("France", "Île-de-France"),
            "Madrid": ("Spain", "Community of Madrid"),
            "Berlin": ("Germany", "Berlin"),
            "New York": ("United States", "New York"),
            "Tokyo": ("Japan", "Tokyo"),
        }

        for city_name, (country, region) in city_filters.items():
            city_data = df[
                (df["country_region"] == country) &
                (df["sub_region_1"] == region) &
                (df["sub_region_2"].isna())  # City level, not sub-districts
            ]

            if city_data.empty:
                print(f"  ⚠️  No data for {city_name}")
                continue

            city = self.get_or_create_city(
                city_name,
                country=country,
                country_code=city_data.iloc[0]["country_region_code"],
                continent="Unknown",
                latitude=0.0,
                longitude=0.0,
                timezone="UTC",
                population=1000000,
            )

            # Import mobility metrics
            for _, row in city_data.iterrows():
                if pd.isna(row["date"]):
                    continue

                metric_date = pd.to_datetime(row["date"]).date()

                # Calculate mobility index (average of key metrics)
                retail = row.get("retail_and_recreation_percent_change_from_baseline", 0)
                transit = row.get("transit_stations_percent_change_from_baseline", 0)
                parks = row.get("parks_percent_change_from_baseline", 0)

                if pd.isna(retail) and pd.isna(transit):
                    continue

                # Create mobility metric
                metric = MobilityMetric(
                    city_id=city.id,
                    date=metric_date,
                    public_transport_usage=int(100000 * (1 + (transit or 0) / 100)),  # Estimate
                    traffic_congestion_index=max(0, 5.0 + (retail or 0) / 20),  # Derived index
                )
                self.db.add(metric)
                self.stats["mobility_metrics"] += 1

            print(f"  ✅ Imported {len(city_data)} mobility records for {city_name}")

        self.db.commit()

    def import_london_marathon(self):
        """Import London Marathon data"""
        print("\n🏃 Importing London Marathon Data...")

        marathon_dir = SOURCES_DIR / "london_marathon"
        if not marathon_dir.exists():
            print("  ⚠️  Directory not found")
            return

        # Look for CSV files
        csv_files = list(marathon_dir.glob("*.csv"))
        if not csv_files:
            print("  ⚠️  No CSV files found")
            return

        # Get London city
        city = self.get_or_create_city(
            "London",
            country="United Kingdom",
            country_code="GBR",
            continent="Europe",
            latitude=51.5074,
            longitude=-0.1278,
            timezone="Europe/London",
            population=9000000,
        )

        # Marathon dates by year
        marathon_dates = {
            2018: date(2018, 4, 22),
            2019: date(2019, 4, 28),
            # 2020: Cancelled
            2021: date(2021, 10, 3),  # Postponed
            2022: date(2022, 10, 2),
            2023: date(2023, 4, 23),
            2024: date(2024, 4, 21),
        }

        for csv_file in csv_files:
            print(f"  📖 Reading {csv_file.name}...")
            df = pd.read_csv(csv_file)

            # Group by year
            if "Year" in df.columns or "year" in df.columns:
                year_col = "Year" if "Year" in df.columns else "year"

                for year, group in df.groupby(year_col):
                    if year not in marathon_dates:
                        continue

                    event_date = marathon_dates[year]
                    participants = len(group)

                    # Create event
                    event = Event(
                        city_id=city.id,
                        name=f"London Marathon {year}",
                        event_type=EventType.SPORTS,
                        description="World's largest marathon",
                        start_date=event_date,
                        end_date=event_date,
                        year=year,
                        expected_attendance=participants,
                        actual_attendance=participants,
                        venue_name="Central London",
                        is_recurring=True,
                        recurrence_pattern="annual",
                    )
                    self.db.add(event)
                    self.stats["events_created"] += 1

                    print(f"  ✅ Created event: London Marathon {year} ({participants:,} participants)")

        self.db.commit()

    def import_champions_league(self):
        """Import Champions League finals data"""
        print("\n⚽ Importing Champions League Data...")

        ucl_dir = SOURCES_DIR / "champions_league"
        if not ucl_dir.exists():
            print("  ⚠️  Directory not found")
            return

        # Look for finals CSV
        finals_files = list(ucl_dir.glob("*finals*.csv")) or list(ucl_dir.glob("*UCL_Finals*.csv"))
        if not finals_files:
            print("  ⚠️  No finals CSV found")
            return

        df = pd.read_csv(finals_files[0])
        print(f"  📖 Found {len(df)} finals")

        for _, row in df.iterrows():
            # Extract data
            season = row.get("season") or row.get("Season") or ""
            venue = row.get("venue") or row.get("Venue") or ""
            city_name = row.get("city") or row.get("City") or venue.split(",")[-1].strip()
            attendance = row.get("attendance") or row.get("Attendance") or 0

            # Parse date
            date_str = row.get("date") or row.get("Date") or ""
            try:
                if isinstance(date_str, str):
                    event_date = pd.to_datetime(date_str).date()
                else:
                    # Assume season format like "2023/24"
                    year = int(season.split("/")[0]) if "/" in str(season) else 2024
                    event_date = date(year, 5, 1)  # Approximate
            except:
                continue

            # Create or get city (simplified - use venue city)
            if city_name and city_name != "":
                city = self.get_or_create_city(
                    city_name,
                    country="Unknown",
                    country_code="UNK",
                    continent="Europe",
                    latitude=0.0,
                    longitude=0.0,
                    timezone="UTC",
                    population=1000000,
                )

                # Create event
                event = Event(
                    city_id=city.id,
                    name=f"UEFA Champions League Final {season}",
                    event_type=EventType.SPORTS,
                    description="UEFA Champions League Final",
                    start_date=event_date,
                    end_date=event_date,
                    year=event_date.year,
                    expected_attendance=int(attendance) if attendance else None,
                    actual_attendance=int(attendance) if attendance else None,
                    venue_name=venue,
                    is_recurring=False,
                )
                self.db.add(event)
                self.stats["events_created"] += 1

        self.db.commit()
        print(f"  ✅ Imported {self.stats['events_created']} Champions League finals")

    def print_summary(self):
        """Print import summary"""
        print("\n" + "=" * 60)
        print("📊 IMPORT SUMMARY")
        print("=" * 60)
        for key, value in self.stats.items():
            emoji = "✅" if value > 0 else "⚠️ "
            print(f"{emoji} {key.replace('_', ' ').title()}: {value:,}")
        print("=" * 60)


def main():
    """Main import orchestrator"""
    print("\n" + "=" * 60)
    print("  📥 EVENTLY - CSV Data Importer")
    print("  UNESCO MVP - Real Data Integration")
    print("=" * 60)
    print(f"\n📁 Source directory: {SOURCES_DIR}")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready\n")

    # Create session
    db = SessionLocal()
    importer = DataImporter(db)

    try:
        # Import from each source
        importer.import_worldbank_tourism()
        importer.import_google_mobility()
        importer.import_london_marathon()
        importer.import_champions_league()

        # Print summary
        importer.print_summary()

        print("\n💡 Next steps:")
        print("   1. Review imported data in database")
        print("   2. Run ML training: python data/scripts/train_models.py")
        print("   3. Generate predictions")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
