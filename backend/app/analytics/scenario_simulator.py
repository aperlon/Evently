"""
What-If Scenario Simulator
Simulates the impact of changes in event parameters
"""
from typing import Dict
from sqlalchemy.orm import Session

from app.models import Event, EventImpact
from app.analytics.impact_analyzer import ImpactAnalyzer


class ScenarioSimulator:
    """
    Simulates what-if scenarios for event planning and analysis
    """

    def __init__(self, db: Session):
        self.db = db
        self.analyzer = ImpactAnalyzer(db)

    def simulate_attendance_change(
        self,
        event_id: int,
        attendance_change_pct: float,
        price_elasticity: float = 0.3,
        spending_multiplier: float = 1.0,
    ) -> Dict:
        """
        Simulate impact of changing event attendance

        Args:
            event_id: Event to simulate
            attendance_change_pct: Percentage change in attendance (-100 to 500)
            price_elasticity: How much prices respond to demand (0-1)
            spending_multiplier: Multiplier for visitor spending

        Returns:
            Dictionary with base and projected scenarios
        """
        # Get base event impact
        base_impact = (
            self.db.query(EventImpact)
            .filter(EventImpact.event_id == event_id)
            .first()
        )

        if not base_impact:
            # Calculate if not exists
            base_impact = self.analyzer.calculate_event_impact(event_id)
            if not base_impact:
                return {}

        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return {}

        # Calculate projected impact
        attendance_multiplier = 1 + (attendance_change_pct / 100)

        # Visitor metrics
        projected_additional_visitors = int(
            base_impact.additional_visitors * attendance_multiplier
            if base_impact.additional_visitors
            else 0
        )
        projected_event_visitors = int(
            base_impact.event_period_daily_visitors * attendance_multiplier
            if base_impact.event_period_daily_visitors
            else 0
        )

        # Calculate new visitor increase percentage
        if base_impact.baseline_daily_visitors and base_impact.baseline_daily_visitors > 0:
            projected_visitor_increase_pct = (
                (projected_event_visitors - base_impact.baseline_daily_visitors)
                / base_impact.baseline_daily_visitors
            ) * 100
        else:
            projected_visitor_increase_pct = 0

        # Hotel metrics with price elasticity
        # Price increases more with higher demand, but not linearly
        price_change_multiplier = 1 + (
            (attendance_change_pct / 100) * price_elasticity
        )

        projected_event_price = (
            base_impact.event_avg_price_usd * price_change_multiplier
            if base_impact.event_avg_price_usd
            else 0
        )

        if base_impact.baseline_avg_price_usd and base_impact.baseline_avg_price_usd > 0:
            projected_price_increase_pct = (
                (projected_event_price - base_impact.baseline_avg_price_usd)
                / base_impact.baseline_avg_price_usd
            ) * 100
        else:
            projected_price_increase_pct = 0

        # Occupancy (capped at 100%)
        occupancy_change = (attendance_change_pct / 100) * (
            base_impact.event_occupancy_pct - base_impact.baseline_occupancy_pct
            if base_impact.event_occupancy_pct and base_impact.baseline_occupancy_pct
            else 0
        )

        projected_event_occupancy = min(
            100,
            (base_impact.event_occupancy_pct or 0) + occupancy_change
        )

        if base_impact.baseline_occupancy_pct and base_impact.baseline_occupancy_pct > 0:
            projected_occupancy_increase_pct = (
                (projected_event_occupancy - base_impact.baseline_occupancy_pct)
                / base_impact.baseline_occupancy_pct
            ) * 100
        else:
            projected_occupancy_increase_pct = 0

        # Economic impact
        # More visitors = more spending, with adjustable multiplier
        spending_change_factor = attendance_multiplier * spending_multiplier

        projected_direct_spending = (
            base_impact.direct_spending_usd * spending_change_factor
            if base_impact.direct_spending_usd
            else 0
        )

        # Recalculate indirect and induced with same ratios
        projected_indirect_spending = projected_direct_spending * 0.4
        projected_induced_spending = projected_direct_spending * 0.3

        projected_total_impact = (
            projected_direct_spending
            + projected_indirect_spending
            + projected_induced_spending
        )

        # Jobs scale roughly with economic activity
        projected_jobs = int(
            (base_impact.jobs_created or 0) * spending_change_factor
        )

        # Tax revenue
        projected_tax_revenue = (
            (base_impact.tax_revenue_usd or 0) * spending_change_factor
        )

        # ROI recalculation
        if base_impact.event_cost_usd and base_impact.event_cost_usd > 0:
            projected_roi = projected_total_impact / base_impact.event_cost_usd
        else:
            projected_roi = base_impact.roi_ratio

        # Mobility impacts scale with attendance
        projected_airport_increase = (
            (base_impact.airport_arrivals_increase_pct or 0) * attendance_multiplier
        )
        projected_transport_increase = (
            (base_impact.public_transport_increase_pct or 0) * attendance_multiplier
        )
        projected_congestion_increase = (
            (base_impact.traffic_congestion_increase_pct or 0) * attendance_multiplier
        )

        # Build scenario comparison
        base_scenario = {
            "scenario_name": "Current/Historical",
            "attendance": event.actual_attendance or event.expected_attendance,
            "additional_visitors": base_impact.additional_visitors,
            "visitor_increase_pct": base_impact.visitor_increase_pct,
            "avg_price_usd": base_impact.event_avg_price_usd,
            "price_increase_pct": base_impact.price_increase_pct,
            "occupancy_pct": base_impact.event_occupancy_pct,
            "occupancy_increase_pct": base_impact.occupancy_increase_pct,
            "total_economic_impact_usd": base_impact.total_economic_impact_usd,
            "jobs_created": base_impact.jobs_created,
            "roi_ratio": base_impact.roi_ratio,
        }

        projected_scenario = {
            "scenario_name": f"Attendance {attendance_change_pct:+.0f}%",
            "attendance": int(
                (event.actual_attendance or event.expected_attendance or 0)
                * attendance_multiplier
            ),
            "additional_visitors": projected_additional_visitors,
            "visitor_increase_pct": round(projected_visitor_increase_pct, 2),
            "avg_price_usd": round(projected_event_price, 2),
            "price_increase_pct": round(projected_price_increase_pct, 2),
            "occupancy_pct": round(projected_event_occupancy, 2),
            "occupancy_increase_pct": round(projected_occupancy_increase_pct, 2),
            "total_economic_impact_usd": round(projected_total_impact, 2),
            "jobs_created": projected_jobs,
            "roi_ratio": round(projected_roi, 2),
        }

        # Calculate changes
        changes = {}
        for key in base_scenario:
            if key == "scenario_name":
                continue
            base_val = base_scenario[key] or 0
            proj_val = projected_scenario[key] or 0

            if base_val != 0:
                pct_change = ((proj_val - base_val) / base_val) * 100
                changes[key] = round(pct_change, 2)
            else:
                changes[key] = 0

        return {
            "event_name": event.name,
            "simulation_parameters": {
                "attendance_change_pct": attendance_change_pct,
                "price_elasticity": price_elasticity,
                "spending_multiplier": spending_multiplier,
            },
            "base_scenario": base_scenario,
            "projected_scenario": projected_scenario,
            "changes": changes,
        }

    def simulate_event_growth(
        self, event_id: int, years: int = 5, annual_growth_pct: float = 10
    ) -> Dict:
        """
        Simulate multi-year event growth trajectory

        Args:
            event_id: Event to simulate
            years: Number of years to project
            annual_growth_pct: Annual growth rate in attendance

        Returns:
            Dictionary with year-by-year projections
        """
        projections = []
        current_growth = 0

        for year in range(1, years + 1):
            current_growth += annual_growth_pct
            year_projection = self.simulate_attendance_change(
                event_id, attendance_change_pct=current_growth
            )

            if year_projection:
                projections.append({
                    "year": year,
                    "cumulative_growth_pct": current_growth,
                    **year_projection["projected_scenario"],
                })

        return {
            "event_id": event_id,
            "projection_years": years,
            "annual_growth_rate": annual_growth_pct,
            "projections": projections,
        }

    def simulate_new_event(
        self,
        city_id: int,
        expected_attendance: int,
        event_duration_days: int,
        reference_event_id: Optional[int] = None,
    ) -> Dict:
        """
        Simulate impact of a completely new event

        Args:
            city_id: City where event would take place
            expected_attendance: Expected number of attendees
            event_duration_days: Duration of the event
            reference_event_id: Optional reference event for benchmarking

        Returns:
            Projected impact metrics for the new event
        """
        # If reference event provided, use it as baseline
        if reference_event_id:
            reference_impact = (
                self.db.query(EventImpact, Event)
                .join(Event, EventImpact.event_id == Event.id)
                .filter(Event.id == reference_event_id)
                .first()
            )

            if reference_impact:
                impact, ref_event = reference_impact

                # Scale based on attendance ratio
                attendance_ratio = (
                    expected_attendance / (ref_event.actual_attendance or ref_event.expected_attendance)
                    if (ref_event.actual_attendance or ref_event.expected_attendance)
                    else 1
                )

                # Scale based on duration ratio
                duration_ratio = event_duration_days / (
                    (ref_event.end_date - ref_event.start_date).days + 1
                )

                combined_multiplier = attendance_ratio * duration_ratio

                return {
                    "projected_impact": {
                        "total_economic_impact_usd": (impact.total_economic_impact_usd or 0) * combined_multiplier,
                        "additional_visitors": int((impact.additional_visitors or 0) * combined_multiplier),
                        "jobs_created": int((impact.jobs_created or 0) * combined_multiplier),
                        "price_increase_pct": (impact.price_increase_pct or 0) * attendance_ratio,
                        "occupancy_increase_pct": min(100, (impact.occupancy_increase_pct or 0) * attendance_ratio),
                    },
                    "reference_event": ref_event.name,
                    "scaling_factors": {
                        "attendance_ratio": round(attendance_ratio, 2),
                        "duration_ratio": round(duration_ratio, 2),
                        "combined_multiplier": round(combined_multiplier, 2),
                    },
                }

        # If no reference, use city averages
        # This is a simplified estimation
        return {
            "projected_impact": {
                "total_economic_impact_usd": expected_attendance * 300,  # Rough estimate: $300 per attendee
                "additional_visitors": int(expected_attendance * 0.7),  # 70% visitors from outside
                "jobs_created": int(expected_attendance / 100),  # 1 job per 100 attendees
                "price_increase_pct": 15.0,  # Typical increase
                "occupancy_increase_pct": 20.0,  # Typical increase
            },
            "note": "Estimates based on industry averages - no reference event used",
        }
