"""
Event model for storing information about urban events
"""
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, JSON, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class EventType(str, Enum):
    """Types of events"""
    SPORTS = "sports"
    MUSIC = "music"
    CULTURE = "culture"
    BUSINESS = "business"
    FAIR = "fair"
    FESTIVAL = "festival"
    CONFERENCE = "conference"
    OTHER = "other"


class Event(Base):
    """Event model representing major urban events"""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False, index=True)

    # Basic information
    name = Column(String(200), nullable=False, index=True)
    event_type = Column(SQLEnum(EventType), nullable=False, index=True)
    description = Column(String(1000))

    # Dates
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)

    # Event characteristics
    expected_attendance = Column(Integer)
    actual_attendance = Column(Integer)
    ticket_revenue_usd = Column(Float)
    economic_impact_usd = Column(Float)  # Estimated total economic impact

    # Venue information
    venue_name = Column(String(200))
    venue_capacity = Column(Integer)
    venue_location = Column(JSON)  # {"lat": x, "lon": y}

    # Event recurrence
    is_recurring = Column(Integer, default=False)  # Using Integer as boolean
    recurrence_pattern = Column(String(50))  # "annual", "biennial", etc.
    edition_number = Column(Integer)  # e.g., "25th edition"

    # External links
    website_url = Column(String(500))
    official_hashtag = Column(String(100))

    # Metadata
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    city = relationship("City", back_populates="events")
    impacts = relationship("EventImpact", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Event(name={self.name}, type={self.event_type}, date={self.start_date})>"

    @property
    def duration_days(self):
        """Calculate event duration in days"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0
