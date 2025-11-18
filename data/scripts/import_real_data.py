"""
Script to import real data from various sources
"""
import sys
import os
import asyncio
from datetime import date

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from app.core.database import SessionLocal
from app.services.airroi_client import AirROIClient
from app.models import City


async def import_from_airroi():
    """
    Import data from AIRROI Data Portal

    Requirements:
    1. Set AIRROI_API_KEY in backend/.env
    2. Ensure cities exist in database
    """
    print("\n🌐 Importing data from AIRROI Data Portal")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Check if API key is configured
        from app.core.config import settings
        if not settings.AIRROI_API_KEY:
            print("❌ AIRROI_API_KEY not configured in .env")
            print("   Please add your API key to backend/.env")
            print("   AIRROI_API_KEY=your-api-key-here")
            return

        # Get all cities
        cities = db.query(City).all()
        print(f"Found {len(cities)} cities in database\n")

        async with AirROIClient() as client:
            for city in cities:
                print(f"📊 Fetching data for {city.name}...")

                try:
                    # Fetch hotel data
                    hotel_data = await client.get_hotel_data(
                        city=city.name,
                        start_date=date(2024, 1, 1),
                        end_date=date(2024, 12, 31),
                        metrics=["occupancy", "adr", "revpar"]
                    )

                    print(f"   ✓ Hotel data: {len(hotel_data.get('daily_metrics', []))} days")

                    # Fetch tourism data
                    tourism_data = await client.get_tourism_data(
                        city=city.name,
                        start_date=date(2024, 1, 1),
                        end_date=date(2024, 12, 31)
                    )

                    print(f"   ✓ Tourism data: {len(tourism_data.get('daily_metrics', []))} days")

                    # TODO: Store in database
                    # See airroi_client.py for implementation

                except Exception as e:
                    print(f"   ❌ Error: {str(e)}")
                    continue

        print("\n✅ AIRROI data import completed")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        db.close()


def import_from_eurostat():
    """
    Import tourism data from Eurostat

    API Documentation:
    https://ec.europa.eu/eurostat/web/json-and-unicode-web-services
    """
    print("\n🇪🇺 Importing data from Eurostat")
    print("=" * 60)

    import requests

    # Example: Tourism nights spent
    # Dataset: tour_occ_nim (Nights spent at tourist accommodation establishments)

    base_url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
    dataset = "tour_occ_nim"

    # Parameters
    params = {
        "format": "JSON",
        "lang": "EN",
        "freq": "M",  # Monthly
        "unit": "NR",  # Number
        "nace_r2": "I551-I553",  # Hotels and similar
        "geo": "ES,FR,DE,UK",  # Spain, France, Germany, UK
        "time": "2024"
    }

    try:
        response = requests.get(f"{base_url}/{dataset}", params=params)
        response.raise_for_status()

        data = response.json()
        print("✓ Data fetched from Eurostat")
        print(f"  Dimensions: {list(data.get('dimension', {}).keys())}")

        # TODO: Parse and store in database

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def import_from_world_bank():
    """
    Import economic data from World Bank

    API Documentation:
    https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
    """
    print("\n🌍 Importing data from World Bank")
    print("=" * 60)

    import requests

    # Example: International tourism, number of arrivals
    # Indicator: ST.INT.ARVL

    countries = {
        "GBR": "United Kingdom",
        "JPN": "Japan",
        "FRA": "France",
        "USA": "United States",
        "ESP": "Spain",
        "DEU": "Germany"
    }

    for code, name in countries.items():
        try:
            url = f"https://api.worldbank.org/v2/country/{code}/indicator/ST.INT.ARVL"
            params = {
                "format": "json",
                "date": "2020:2024",
                "per_page": 100
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            if len(data) > 1:
                values = data[1]
                print(f"✓ {name}: {len(values)} data points")

                # TODO: Store in database

        except Exception as e:
            print(f"❌ {name}: {str(e)}")


def import_from_google_mobility():
    """
    Import mobility data from Google COVID-19 Mobility Reports

    Note: This dataset is publicly available as CSV
    Download from: https://www.google.com/covid19/mobility/
    """
    print("\n📱 Importing data from Google Mobility Reports")
    print("=" * 60)

    import pandas as pd

    # URL to the global mobility report
    url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"

    try:
        print("Downloading mobility data (this may take a minute)...")
        df = pd.read_csv(url)

        # Filter for our cities
        cities_filter = df['sub_region_1'].isin([
            'England',  # London
            'Tokyo',
            'Île-de-France',  # Paris
            'New York',
            'Community of Madrid',
            'Berlin'
        ])

        city_data = df[cities_filter]
        print(f"✓ Found {len(city_data)} mobility records")
        print(f"  Date range: {city_data['date'].min()} to {city_data['date'].max()}")

        # Columns available:
        # - retail_and_recreation_percent_change_from_baseline
        # - grocery_and_pharmacy_percent_change_from_baseline
        # - parks_percent_change_from_baseline
        # - transit_stations_percent_change_from_baseline
        # - workplaces_percent_change_from_baseline
        # - residential_percent_change_from_baseline

        print("  Metrics: Retail, Transit, Workplaces, Parks, etc.")

        # TODO: Map to our cities and store in database

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Main function to import data from all sources"""
    print("\n" + "=" * 60)
    print("  EVENTLY - Real Data Import Tool")
    print("=" * 60)

    print("\nAvailable data sources:")
    print("1. AIRROI Data Portal (Hotel & Tourism)")
    print("2. Eurostat (European Tourism)")
    print("3. World Bank (Global Tourism)")
    print("4. Google Mobility Reports (Movement Data)")
    print("5. All of the above")
    print("0. Exit")

    choice = input("\nSelect source (0-5): ")

    if choice == "1":
        asyncio.run(import_from_airroi())
    elif choice == "2":
        import_from_eurostat()
    elif choice == "3":
        import_from_world_bank()
    elif choice == "4":
        import_from_google_mobility()
    elif choice == "5":
        print("\nImporting from all sources...")
        asyncio.run(import_from_airroi())
        import_from_eurostat()
        import_from_world_bank()
        import_from_google_mobility()
    elif choice == "0":
        print("Exiting...")
        return
    else:
        print("Invalid choice")
        return

    print("\n" + "=" * 60)
    print("Import process completed!")
    print("\nNext steps:")
    print("1. Review imported data in the database")
    print("2. Run impact analysis: python data/scripts/calculate_impacts.py")
    print("3. Start the application: docker-compose up -d")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
