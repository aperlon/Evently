"""
Metrics models for tracking various impact indicators
"""
from sqlalchemy import Column, Integer, Float, Date, ForeignKey, JSON, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TourismMetric(Base):
    """Tourism metrics - daily visitor statistics"""

    __tablename__ = "tourism_metrics"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    # Visitor counts
    domestic_visitors = Column(Integer)
    international_visitors = Column(Integer)
    total_visitors = Column(Integer)

    # Demographics
    avg_stay_duration_days = Column(Float)
    avg_spending_per_visitor_usd = Column(Float)

    # Purposes
    business_visitors_pct = Column(Float)
    leisure_visitors_pct = Column(Float)
    event_visitors_pct = Column(Float)

    # Additional data
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    city = relationship("City", back_populates="tourism_metrics")

    __table_args__ = (
        Index('idx_tourism_city_date', 'city_id', 'date'),
    )


class HotelMetric(Base):
    """Hotel and accommodation metrics"""

    __tablename__ = "hotel_metrics"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    # Occupancy
    occupancy_rate_pct = Column(Float)
    available_rooms = Column(Integer)
    occupied_rooms = Column(Integer)

    # Pricing
    avg_price_usd = Column(Float)
    median_price_usd = Column(Float)
    min_price_usd = Column(Float)
    max_price_usd = Column(Float)

    # Revenue
    revenue_per_available_room_usd = Column(Float)  # RevPAR
    total_revenue_usd = Column(Float)

    # Market segments
    luxury_occupancy_pct = Column(Float)
    midscale_occupancy_pct = Column(Float)
    budget_occupancy_pct = Column(Float)

    # Additional data
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    city = relationship("City", back_populates="hotel_metrics")

    __table_args__ = (
        Index('idx_hotel_city_date', 'city_id', 'date'),
    )


class EconomicMetric(Base):
    """Economic impact metrics"""

    __tablename__ = "economic_metrics"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    # Overall spending
    total_spending_usd = Column(Float)
    accommodation_spending_usd = Column(Float)
    food_beverage_spending_usd = Column(Float)
    retail_spending_usd = Column(Float)
    entertainment_spending_usd = Column(Float)
    transport_spending_usd = Column(Float)

    # Employment
    temporary_jobs_created = Column(Integer)
    full_time_equivalent_jobs = Column(Float)

    # Business activity
    retail_transactions = Column(Integer)
    restaurant_reservations = Column(Integer)

    # Tax revenue
    estimated_tax_revenue_usd = Column(Float)

    # Additional data
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    city = relationship("City", back_populates="economic_metrics")

    __table_args__ = (
        Index('idx_economic_city_date', 'city_id', 'date'),
    )


class MobilityMetric(Base):
    """Mobility and transportation metrics"""

    __tablename__ = "mobility_metrics"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    # Air travel
    airport_arrivals = Column(Integer)
    airport_departures = Column(Integer)
    international_flights = Column(Integer)
    domestic_flights = Column(Integer)

    # Ground transportation
    train_arrivals = Column(Integer)
    bus_arrivals = Column(Integer)
    car_rentals = Column(Integer)

    # Urban mobility
    public_transport_usage = Column(Integer)
    taxi_rides = Column(Integer)
    rideshare_trips = Column(Integer)

    # Traffic
    traffic_congestion_index = Column(Float)
    avg_commute_time_minutes = Column(Float)

    # Additional data
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    city = relationship("City", back_populates="mobility_metrics")

    __table_args__ = (
        Index('idx_mobility_city_date', 'city_id', 'date'),
    )
