"""
Event Impact Analyzer - Core analytics engine for calculating event impacts
"""
from datetime import timedelta, date
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import (
    Event,
    City,
    TourismMetric,
    HotelMetric,
    EconomicMetric,
    MobilityMetric,
    EventImpact
)
from app.core.config import settings


class ImpactAnalyzer:
    """
    Analyzes the impact of events on tourism, hotels, and economy
    """

    def __init__(self, db: Session):
        self.db = db
        self.window_before = settings.EVENT_IMPACT_WINDOW_BEFORE_DAYS
        self.window_after = settings.EVENT_IMPACT_WINDOW_AFTER_DAYS

    def calculate_event_impact(self, event_id: int) -> Optional[EventImpact]:
        """
        Calculate comprehensive impact for a specific event

        Args:
            event_id: ID of the event to analyze

        Returns:
            EventImpact object with calculated metrics
        """
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        # Define analysis windows
        baseline_start = event.start_date - timedelta(days=self.window_before + 30)
        baseline_end = event.start_date - timedelta(days=self.window_before)
        event_start = event.start_date
        event_end = event.end_date
        post_event_end = event.end_date + timedelta(days=self.window_after)

        # Calculate tourism impact
        tourism_impact = self._calculate_tourism_impact(
            event.city_id, baseline_start, baseline_end, event_start, event_end
        )

        # Calculate hotel impact
        hotel_impact = self._calculate_hotel_impact(
            event.city_id, baseline_start, baseline_end, event_start, event_end
        )

        # Calculate economic impact
        economic_impact = self._calculate_economic_impact(
            event.city_id, baseline_start, baseline_end, event_start, event_end
        )

        # Calculate mobility impact
        mobility_impact = self._calculate_mobility_impact(
            event.city_id, baseline_start, baseline_end, event_start, event_end
        )

        # Create or update EventImpact record
        impact = EventImpact(
            event_id=event_id,
            **tourism_impact,
            **hotel_impact,
            **economic_impact,
            **mobility_impact,
            days_before_analyzed=self.window_before,
            days_after_analyzed=self.window_after,
        )

        # Calculate ROI if cost is available
        if event.economic_impact_usd and impact.total_economic_impact_usd:
            impact.event_cost_usd = event.economic_impact_usd
            impact.roi_ratio = (
                impact.total_economic_impact_usd / event.economic_impact_usd
            )
            impact.benefit_cost_ratio = impact.roi_ratio

        return impact

    def _calculate_tourism_impact(
        self,
        city_id: int,
        baseline_start: date,
        baseline_end: date,
        event_start: date,
        event_end: date,
    ) -> Dict:
        """Calculate tourism-related impact metrics"""

        # Get baseline metrics
        baseline_metrics = (
            self.db.query(TourismMetric)
            .filter(
                and_(
                    TourismMetric.city_id == city_id,
                    TourismMetric.date >= baseline_start,
                    TourismMetric.date <= baseline_end,
                )
            )
            .all()
        )

        # Get event period metrics
        event_metrics = (
            self.db.query(TourismMetric)
            .filter(
                and_(
                    TourismMetric.city_id == city_id,
                    TourismMetric.date >= event_start,
                    TourismMetric.date <= event_end,
                )
            )
            .all()
        )

        if not baseline_metrics or not event_metrics:
            return {}

        # Calculate averages
        baseline_avg_visitors = np.mean(
            [m.total_visitors for m in baseline_metrics if m.total_visitors]
        )
        event_avg_visitors = np.mean(
            [m.total_visitors for m in event_metrics if m.total_visitors]
        )

        # Calculate increases
        visitor_increase_pct = (
            ((event_avg_visitors - baseline_avg_visitors) / baseline_avg_visitors) * 100
            if baseline_avg_visitors > 0
            else 0
        )

        additional_visitors = int(
            (event_avg_visitors - baseline_avg_visitors) * len(event_metrics)
        )

        return {
            "baseline_daily_visitors": int(baseline_avg_visitors),
            "event_period_daily_visitors": int(event_avg_visitors),
            "visitor_increase_pct": round(visitor_increase_pct, 2),
            "additional_visitors": max(0, additional_visitors),
        }

    def _calculate_hotel_impact(
        self,
        city_id: int,
        baseline_start: date,
        baseline_end: date,
        event_start: date,
        event_end: date,
    ) -> Dict:
        """Calculate hotel-related impact metrics"""

        # Get baseline metrics
        baseline_metrics = (
            self.db.query(HotelMetric)
            .filter(
                and_(
                    HotelMetric.city_id == city_id,
                    HotelMetric.date >= baseline_start,
                    HotelMetric.date <= baseline_end,
                )
            )
            .all()
        )

        # Get event period metrics
        event_metrics = (
            self.db.query(HotelMetric)
            .filter(
                and_(
                    HotelMetric.city_id == city_id,
                    HotelMetric.date >= event_start,
                    HotelMetric.date <= event_end,
                )
            )
            .all()
        )

        if not baseline_metrics or not event_metrics:
            return {}

        # Calculate occupancy metrics
        baseline_occupancy = np.mean(
            [m.occupancy_rate_pct for m in baseline_metrics if m.occupancy_rate_pct]
        )
        event_occupancy = np.mean(
            [m.occupancy_rate_pct for m in event_metrics if m.occupancy_rate_pct]
        )

        occupancy_increase_pct = (
            ((event_occupancy - baseline_occupancy) / baseline_occupancy) * 100
            if baseline_occupancy > 0
            else 0
        )

        # Calculate price metrics
        baseline_price = np.mean(
            [m.avg_price_usd for m in baseline_metrics if m.avg_price_usd]
        )
        event_price = np.mean(
            [m.avg_price_usd for m in event_metrics if m.avg_price_usd]
        )

        price_increase_pct = (
            ((event_price - baseline_price) / baseline_price) * 100
            if baseline_price > 0
            else 0
        )

        return {
            "baseline_occupancy_pct": round(baseline_occupancy, 2),
            "event_occupancy_pct": round(event_occupancy, 2),
            "occupancy_increase_pct": round(occupancy_increase_pct, 2),
            "baseline_avg_price_usd": round(baseline_price, 2),
            "event_avg_price_usd": round(event_price, 2),
            "price_increase_pct": round(price_increase_pct, 2),
        }

    def _calculate_economic_impact(
        self,
        city_id: int,
        baseline_start: date,
        baseline_end: date,
        event_start: date,
        event_end: date,
    ) -> Dict:
        """Calculate economic impact metrics"""

        # Get event period metrics
        event_metrics = (
            self.db.query(EconomicMetric)
            .filter(
                and_(
                    EconomicMetric.city_id == city_id,
                    EconomicMetric.date >= event_start,
                    EconomicMetric.date <= event_end,
                )
            )
            .all()
        )

        if not event_metrics:
            return {}

        # Calculate total spending
        total_spending = sum(
            m.total_spending_usd for m in event_metrics if m.total_spending_usd
        )

        # Estimate multiplier effects (simplified)
        # Direct: actual spending
        # Indirect: supply chain impacts (estimated at 40% of direct)
        # Induced: employee spending (estimated at 30% of direct)
        direct_spending = total_spending
        indirect_spending = total_spending * 0.4
        induced_spending = total_spending * 0.3

        total_economic_impact = direct_spending + indirect_spending + induced_spending

        # Jobs and tax revenue estimates
        jobs_created = sum(
            m.temporary_jobs_created for m in event_metrics if m.temporary_jobs_created
        )
        tax_revenue = sum(
            m.estimated_tax_revenue_usd
            for m in event_metrics
            if m.estimated_tax_revenue_usd
        )

        return {
            "total_economic_impact_usd": round(total_economic_impact, 2),
            "direct_spending_usd": round(direct_spending, 2),
            "indirect_spending_usd": round(indirect_spending, 2),
            "induced_spending_usd": round(induced_spending, 2),
            "jobs_created": int(jobs_created),
            "tax_revenue_usd": round(tax_revenue, 2),
        }

    def _calculate_mobility_impact(
        self,
        city_id: int,
        baseline_start: date,
        baseline_end: date,
        event_start: date,
        event_end: date,
    ) -> Dict:
        """Calculate mobility and transportation impact metrics"""

        # Get baseline metrics
        baseline_metrics = (
            self.db.query(MobilityMetric)
            .filter(
                and_(
                    MobilityMetric.city_id == city_id,
                    MobilityMetric.date >= baseline_start,
                    MobilityMetric.date <= baseline_end,
                )
            )
            .all()
        )

        # Get event period metrics
        event_metrics = (
            self.db.query(MobilityMetric)
            .filter(
                and_(
                    MobilityMetric.city_id == city_id,
                    MobilityMetric.date >= event_start,
                    MobilityMetric.date <= event_end,
                )
            )
            .all()
        )

        if not baseline_metrics or not event_metrics:
            return {}

        # Calculate airport arrivals increase
        baseline_arrivals = np.mean(
            [m.airport_arrivals for m in baseline_metrics if m.airport_arrivals]
        )
        event_arrivals = np.mean(
            [m.airport_arrivals for m in event_metrics if m.airport_arrivals]
        )

        arrivals_increase_pct = (
            ((event_arrivals - baseline_arrivals) / baseline_arrivals) * 100
            if baseline_arrivals > 0
            else 0
        )

        # Calculate public transport usage increase
        baseline_transport = np.mean(
            [
                m.public_transport_usage
                for m in baseline_metrics
                if m.public_transport_usage
            ]
        )
        event_transport = np.mean(
            [m.public_transport_usage for m in event_metrics if m.public_transport_usage]
        )

        transport_increase_pct = (
            ((event_transport - baseline_transport) / baseline_transport) * 100
            if baseline_transport > 0
            else 0
        )

        # Calculate traffic congestion increase
        baseline_congestion = np.mean(
            [
                m.traffic_congestion_index
                for m in baseline_metrics
                if m.traffic_congestion_index
            ]
        )
        event_congestion = np.mean(
            [
                m.traffic_congestion_index
                for m in event_metrics
                if m.traffic_congestion_index
            ]
        )

        congestion_increase_pct = (
            ((event_congestion - baseline_congestion) / baseline_congestion) * 100
            if baseline_congestion > 0
            else 0
        )

        return {
            "airport_arrivals_increase_pct": round(arrivals_increase_pct, 2),
            "public_transport_increase_pct": round(transport_increase_pct, 2),
            "traffic_congestion_increase_pct": round(congestion_increase_pct, 2),
        }

    def get_time_series(
        self,
        city_id: int,
        metric_type: str,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """
        Get time series data for a specific metric

        Args:
            city_id: City ID
            metric_type: Type of metric (tourism, hotel, economic, mobility)
            start_date: Start date for time series
            end_date: End date for time series

        Returns:
            DataFrame with time series data
        """
        metric_model_map = {
            "tourism": TourismMetric,
            "hotel": HotelMetric,
            "economic": EconomicMetric,
            "mobility": MobilityMetric,
        }

        model = metric_model_map.get(metric_type)
        if not model:
            return pd.DataFrame()

        metrics = (
            self.db.query(model)
            .filter(
                and_(
                    model.city_id == city_id,
                    model.date >= start_date,
                    model.date <= end_date,
                )
            )
            .order_by(model.date)
            .all()
        )

        # Convert to DataFrame
        data = []
        for m in metrics:
            data.append({col: getattr(m, col) for col in m.__table__.columns.keys()})

        return pd.DataFrame(data)

    def compare_events(self, event_ids: List[int]) -> pd.DataFrame:
        """
        Compare multiple events based on their impact metrics

        Args:
            event_ids: List of event IDs to compare

        Returns:
            DataFrame with comparison metrics
        """
        impacts = (
            self.db.query(EventImpact, Event)
            .join(Event, EventImpact.event_id == Event.id)
            .filter(Event.id.in_(event_ids))
            .all()
        )

        comparison_data = []
        for impact, event in impacts:
            comparison_data.append({
                "event_id": event.id,
                "event_name": event.name,
                "event_type": event.event_type,
                "visitor_increase_pct": impact.visitor_increase_pct,
                "price_increase_pct": impact.price_increase_pct,
                "occupancy_increase_pct": impact.occupancy_increase_pct,
                "total_economic_impact_usd": impact.total_economic_impact_usd,
                "roi_ratio": impact.roi_ratio,
                "jobs_created": impact.jobs_created,
            })

        return pd.DataFrame(comparison_data)

    def compare_cities(self, city_ids: List[int]) -> pd.DataFrame:
        """
        Compare cities based on average event impacts

        Args:
            city_ids: List of city IDs to compare

        Returns:
            DataFrame with city comparison metrics
        """
        city_data = []

        for city_id in city_ids:
            city = self.db.query(City).filter(City.id == city_id).first()
            if not city:
                continue

            # Get all event impacts for this city
            impacts = (
                self.db.query(EventImpact)
                .join(Event, EventImpact.event_id == Event.id)
                .filter(Event.city_id == city_id)
                .all()
            )

            if not impacts:
                continue

            # Calculate averages
            city_data.append({
                "city_id": city_id,
                "city_name": city.name,
                "num_events": len(impacts),
                "avg_visitor_increase_pct": np.mean(
                    [i.visitor_increase_pct for i in impacts if i.visitor_increase_pct]
                ),
                "avg_price_increase_pct": np.mean(
                    [i.price_increase_pct for i in impacts if i.price_increase_pct]
                ),
                "avg_occupancy_increase_pct": np.mean(
                    [i.occupancy_increase_pct for i in impacts if i.occupancy_increase_pct]
                ),
                "total_economic_impact_usd": sum(
                    i.total_economic_impact_usd for i in impacts if i.total_economic_impact_usd
                ),
                "total_jobs_created": sum(i.jobs_created for i in impacts if i.jobs_created),
            })

        return pd.DataFrame(city_data)
