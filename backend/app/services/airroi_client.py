"""
AIRROI API Client for fetching real hotel and tourism data
"""
import httpx
from typing import Dict, List, Optional
from datetime import date
from app.core.config import settings


class AirROIClient:
    """Client for AIRROI Data Portal API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.AIRROI_API_KEY
        self.base_url = settings.AIRROI_BASE_URL
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )

    async def get_hotel_data(
        self,
        city: str,
        start_date: date,
        end_date: date,
        metrics: List[str] = None
    ) -> Dict:
        """
        Fetch hotel data from AIRROI

        Args:
            city: City name or code
            start_date: Start date for data
            end_date: End date for data
            metrics: List of metrics to fetch (occupancy, adr, revpar, etc.)

        Returns:
            Dictionary with hotel metrics
        """
        if metrics is None:
            metrics = ["occupancy", "adr", "revpar", "demand"]

        params = {
            "city": city,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "metrics": ",".join(metrics)
        }

        # Example endpoint - adjust based on actual AIRROI API documentation
        response = await self.client.get(
            f"{self.base_url}/api/hotel-metrics",
            params=params
        )

        response.raise_for_status()
        return response.json()

    async def get_tourism_data(
        self,
        city: str,
        start_date: date,
        end_date: date
    ) -> Dict:
        """
        Fetch tourism data from AIRROI

        Args:
            city: City name or code
            start_date: Start date
            end_date: End date

        Returns:
            Tourism statistics
        """
        params = {
            "city": city,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

        response = await self.client.get(
            f"{self.base_url}/api/tourism-data",
            params=params
        )

        response.raise_for_status()
        return response.json()

    async def get_event_impact(
        self,
        city: str,
        event_name: str,
        event_date: date
    ) -> Dict:
        """
        Get pre-calculated event impact from AIRROI

        Args:
            city: City name
            event_name: Name of the event
            event_date: Event date

        Returns:
            Event impact data
        """
        params = {
            "city": city,
            "event": event_name,
            "date": event_date.isoformat()
        }

        response = await self.client.get(
            f"{self.base_url}/api/event-impact",
            params=params
        )

        response.raise_for_status()
        return response.json()

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Example usage function
async def fetch_and_store_airroi_data(
    city_name: str,
    start_date: date,
    end_date: date,
    db
):
    """
    Fetch data from AIRROI and store in database

    Example:
        await fetch_and_store_airroi_data(
            "London",
            date(2024, 1, 1),
            date(2024, 12, 31),
            db_session
        )
    """
    from app.models import City, HotelMetric, TourismMetric

    async with AirROIClient() as client:
        # Get city from database
        city = db.query(City).filter(City.name == city_name).first()
        if not city:
            raise ValueError(f"City {city_name} not found in database")

        # Fetch hotel data
        hotel_data = await client.get_hotel_data(
            city_name,
            start_date,
            end_date
        )

        # Store hotel metrics
        for daily_data in hotel_data.get("daily_metrics", []):
            metric = HotelMetric(
                city_id=city.id,
                date=date.fromisoformat(daily_data["date"]),
                occupancy_rate_pct=daily_data.get("occupancy"),
                avg_price_usd=daily_data.get("adr"),  # Average Daily Rate
                revenue_per_available_room_usd=daily_data.get("revpar"),
                available_rooms=daily_data.get("available_rooms"),
                occupied_rooms=daily_data.get("occupied_rooms"),
            )
            db.add(metric)

        # Fetch tourism data
        tourism_data = await client.get_tourism_data(
            city_name,
            start_date,
            end_date
        )

        # Store tourism metrics
        for daily_data in tourism_data.get("daily_metrics", []):
            metric = TourismMetric(
                city_id=city.id,
                date=date.fromisoformat(daily_data["date"]),
                total_visitors=daily_data.get("total_visitors"),
                international_visitors=daily_data.get("international_visitors"),
                domestic_visitors=daily_data.get("domestic_visitors"),
                avg_spending_per_visitor_usd=daily_data.get("avg_spending"),
            )
            db.add(metric)

        db.commit()
        print(f"✓ Imported AIRROI data for {city_name}")


# Script to import data for all cities
async def import_all_cities_from_airroi(db):
    """
    Import data from AIRROI for all cities in database
    """
    from app.models import City

    cities = db.query(City).all()

    for city in cities:
        try:
            print(f"Importing data for {city.name}...")
            await fetch_and_store_airroi_data(
                city.name,
                date(2024, 1, 1),
                date(2024, 12, 31),
                db
            )
        except Exception as e:
            print(f"Error importing {city.name}: {str(e)}")
            continue


# To use this, create a script like:
# python scripts/import_airroi_data.py
"""
import asyncio
from app.core.database import SessionLocal
from app.services.airroi_client import import_all_cities_from_airroi

async def main():
    db = SessionLocal()
    try:
        await import_all_cities_from_airroi(db)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
"""
