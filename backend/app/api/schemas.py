"""
Pydantic schemas for API request/response validation
"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from app.models.event import EventType


# ============================================================================
# City Schemas
# ============================================================================

class CityBase(BaseModel):
    """Base city schema"""
    name: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)
    country_code: str = Field(..., max_length=3)
    continent: str = Field(..., max_length=50)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: str = Field(..., max_length=50)
    population: Optional[int] = None
    area_km2: Optional[float] = None
    gdp_usd: Optional[float] = None
    annual_tourists: Optional[int] = None
    hotel_rooms: Optional[int] = None
    avg_hotel_price_usd: Optional[float] = None


class CityCreate(CityBase):
    """Schema for creating a city"""
    pass


class CityUpdate(BaseModel):
    """Schema for updating a city"""
    name: Optional[str] = None
    population: Optional[int] = None
    gdp_usd: Optional[float] = None
    annual_tourists: Optional[int] = None
    hotel_rooms: Optional[int] = None
    avg_hotel_price_usd: Optional[float] = None


class CityResponse(CityBase):
    """Schema for city response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# Event Schemas
# ============================================================================

class EventBase(BaseModel):
    """Base event schema"""
    name: str = Field(..., max_length=200)
    event_type: EventType
    description: Optional[str] = Field(None, max_length=1000)
    start_date: date
    end_date: date
    expected_attendance: Optional[int] = None
    actual_attendance: Optional[int] = None
    ticket_revenue_usd: Optional[float] = None
    economic_impact_usd: Optional[float] = None
    venue_name: Optional[str] = Field(None, max_length=200)
    venue_capacity: Optional[int] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = Field(None, max_length=50)
    edition_number: Optional[int] = None
    website_url: Optional[str] = Field(None, max_length=500)
    official_hashtag: Optional[str] = Field(None, max_length=100)

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class EventCreate(EventBase):
    """Schema for creating an event"""
    city_id: int


class EventUpdate(BaseModel):
    """Schema for updating an event"""
    name: Optional[str] = None
    description: Optional[str] = None
    actual_attendance: Optional[int] = None
    economic_impact_usd: Optional[float] = None


class EventResponse(EventBase):
    """Schema for event response"""
    id: int
    city_id: int
    year: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EventWithCity(EventResponse):
    """Event response with city information"""
    city: CityResponse


# ============================================================================
# Metrics Schemas
# ============================================================================

class MetricBase(BaseModel):
    """Base metric schema"""
    city_id: int
    date: date


class TourismMetricCreate(MetricBase):
    """Schema for creating tourism metric"""
    domestic_visitors: Optional[int] = None
    international_visitors: Optional[int] = None
    total_visitors: Optional[int] = None
    avg_stay_duration_days: Optional[float] = None
    avg_spending_per_visitor_usd: Optional[float] = None


class HotelMetricCreate(MetricBase):
    """Schema for creating hotel metric"""
    occupancy_rate_pct: Optional[float] = Field(None, ge=0, le=100)
    available_rooms: Optional[int] = None
    occupied_rooms: Optional[int] = None
    avg_price_usd: Optional[float] = None
    median_price_usd: Optional[float] = None
    min_price_usd: Optional[float] = None
    max_price_usd: Optional[float] = None


class EconomicMetricCreate(MetricBase):
    """Schema for creating economic metric"""
    total_spending_usd: Optional[float] = None
    accommodation_spending_usd: Optional[float] = None
    food_beverage_spending_usd: Optional[float] = None
    retail_spending_usd: Optional[float] = None
    entertainment_spending_usd: Optional[float] = None
    transport_spending_usd: Optional[float] = None


class MobilityMetricCreate(MetricBase):
    """Schema for creating mobility metric"""
    airport_arrivals: Optional[int] = None
    airport_departures: Optional[int] = None
    international_flights: Optional[int] = None
    domestic_flights: Optional[int] = None


# ============================================================================
# Impact Analysis Schemas
# ============================================================================

class EventImpactResponse(BaseModel):
    """Schema for event impact analysis response"""
    id: int
    event_id: int

    # Tourism Impact
    baseline_daily_visitors: Optional[int] = None
    event_period_daily_visitors: Optional[int] = None
    visitor_increase_pct: Optional[float] = None
    additional_visitors: Optional[int] = None

    # Hotel Impact
    baseline_occupancy_pct: Optional[float] = None
    event_occupancy_pct: Optional[float] = None
    occupancy_increase_pct: Optional[float] = None
    baseline_avg_price_usd: Optional[float] = None
    event_avg_price_usd: Optional[float] = None
    price_increase_pct: Optional[float] = None

    # Economic Impact
    total_economic_impact_usd: Optional[float] = None
    direct_spending_usd: Optional[float] = None
    jobs_created: Optional[int] = None
    tax_revenue_usd: Optional[float] = None
    roi_ratio: Optional[float] = None

    calculated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Analytics Schemas
# ============================================================================

class TimeSeriesDataPoint(BaseModel):
    """Single data point in time series"""
    date: date
    value: float
    label: Optional[str] = None


class TimeSeriesResponse(BaseModel):
    """Time series data response"""
    metric_name: str
    city_name: str
    data_points: List[TimeSeriesDataPoint]
    events: List[Dict[str, Any]]  # Events that occurred during this period


class ComparisonMetrics(BaseModel):
    """Metrics for city/event comparison"""
    city_name: str
    event_name: Optional[str] = None
    avg_visitor_increase_pct: float
    avg_price_increase_pct: float
    avg_occupancy_increase_pct: float
    total_economic_impact_usd: float
    roi_ratio: float


class ComparisonResponse(BaseModel):
    """Comparison analysis response"""
    comparison_type: str  # "cities" or "events"
    items: List[ComparisonMetrics]


# ============================================================================
# What-If Scenario Schemas
# ============================================================================

class WhatIfScenarioInput(BaseModel):
    """Input for what-if scenario simulation"""
    event_id: int
    attendance_change_pct: float = Field(..., ge=-100, le=500)
    price_elasticity: float = Field(default=0.3, ge=0, le=1)
    spending_multiplier: float = Field(default=1.0, ge=0.5, le=3.0)


class WhatIfScenarioOutput(BaseModel):
    """Output of what-if scenario simulation"""
    scenario_name: str
    base_scenario: EventImpactResponse
    projected_scenario: EventImpactResponse
    changes: Dict[str, float]  # Percentage changes for key metrics


# ============================================================================
# Dashboard KPI Schemas
# ============================================================================

class DashboardKPIs(BaseModel):
    """Key performance indicators for dashboard"""
    total_events_analyzed: int
    total_cities: int
    avg_economic_impact_per_event_usd: float
    avg_visitor_increase_pct: float
    avg_hotel_price_increase_pct: float
    total_jobs_created: int
    highest_impact_event: EventResponse
    highest_impact_city: CityResponse


# ============================================================================
# Filter and Query Schemas
# ============================================================================

class EventFilters(BaseModel):
    """Filters for event queries"""
    city_id: Optional[int] = None
    event_type: Optional[EventType] = None
    year: Optional[int] = None
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=1000)


class PaginatedResponse(BaseModel):
    """Generic paginated response"""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[Any]
