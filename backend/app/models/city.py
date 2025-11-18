"""
City model for storing information about cities
"""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class City(Base):
    """City model representing urban areas hosting events"""

    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    country = Column(String(100), nullable=False)
    country_code = Column(String(3), nullable=False)
    continent = Column(String(50), nullable=False)

    # Geographic data
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone = Column(String(50), nullable=False)

    # City characteristics
    population = Column(Integer)
    area_km2 = Column(Float)
    gdp_usd = Column(Float)  # GDP in USD

    # Tourism baseline
    annual_tourists = Column(Integer)
    hotel_rooms = Column(Integer)
    avg_hotel_price_usd = Column(Float)

    # Metadata
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    events = relationship("Event", back_populates="city", cascade="all, delete-orphan")
    tourism_metrics = relationship("TourismMetric", back_populates="city", cascade="all, delete-orphan")
    hotel_metrics = relationship("HotelMetric", back_populates="city", cascade="all, delete-orphan")
    economic_metrics = relationship("EconomicMetric", back_populates="city", cascade="all, delete-orphan")
    mobility_metrics = relationship("MobilityMetric", back_populates="city", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<City(name={self.name}, country={self.country})>"
