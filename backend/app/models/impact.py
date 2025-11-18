"""
Event impact analysis model
"""
from sqlalchemy import Column, Integer, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class EventImpact(Base):
    """
    Calculated impact analysis for events
    Stores aggregated metrics and KPIs for event periods
    """

    __tablename__ = "event_impacts"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)

    # Tourism Impact
    baseline_daily_visitors = Column(Integer)  # Average before event
    event_period_daily_visitors = Column(Integer)  # Average during event
    visitor_increase_pct = Column(Float)
    additional_visitors = Column(Integer)

    # Hotel Impact
    baseline_occupancy_pct = Column(Float)
    event_occupancy_pct = Column(Float)
    occupancy_increase_pct = Column(Float)

    baseline_avg_price_usd = Column(Float)
    event_avg_price_usd = Column(Float)
    price_increase_pct = Column(Float)

    # Economic Impact
    total_economic_impact_usd = Column(Float)
    direct_spending_usd = Column(Float)
    indirect_spending_usd = Column(Float)
    induced_spending_usd = Column(Float)

    jobs_created = Column(Integer)
    tax_revenue_usd = Column(Float)

    # ROI Metrics
    event_cost_usd = Column(Float)
    roi_ratio = Column(Float)
    benefit_cost_ratio = Column(Float)

    # Mobility Impact
    airport_arrivals_increase_pct = Column(Float)
    public_transport_increase_pct = Column(Float)
    traffic_congestion_increase_pct = Column(Float)

    # Temporal Analysis
    days_before_analyzed = Column(Integer, default=14)
    days_after_analyzed = Column(Integer, default=14)

    # Peak metrics
    peak_occupancy_date = Column(DateTime(timezone=True))
    peak_price_date = Column(DateTime(timezone=True))
    peak_visitors_date = Column(DateTime(timezone=True))

    # Additional analysis data
    analysis_metadata = Column(JSON, default={})
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    event = relationship("Event", back_populates="impacts")

    def __repr__(self):
        return f"<EventImpact(event_id={self.event_id}, economic_impact=${self.total_economic_impact_usd})>"

    @property
    def summary_kpis(self):
        """Return key performance indicators as dict"""
        return {
            "visitor_increase_pct": self.visitor_increase_pct,
            "price_increase_pct": self.price_increase_pct,
            "occupancy_increase_pct": self.occupancy_increase_pct,
            "total_impact_usd": self.total_economic_impact_usd,
            "roi_ratio": self.roi_ratio,
            "jobs_created": self.jobs_created,
        }
