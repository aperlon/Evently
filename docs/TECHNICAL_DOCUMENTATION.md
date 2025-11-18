# Evently - Technical Documentation

## Overview

Evently is a comprehensive event impact analysis platform that combines data analytics, economic modeling, and interactive visualization to measure the impact of major urban events on tourism, hospitality, and local economies.

## System Architecture

### High-Level Architecture

```
┌─────────────────┐
│  React Frontend │ (Port 3000)
│   (TypeScript)  │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI Backend│ (Port 8000)
│    (Python)     │
└────────┬────────┘
         │ SQLAlchemy
         ▼
┌─────────────────┐
│   PostgreSQL    │ (Port 5432)
│    Database     │
└─────────────────┘
```

### Backend Architecture

**Core Components:**

1. **API Layer** (`app/api/`)
   - REST endpoints using FastAPI
   - Request/response validation with Pydantic
   - Route handlers for all operations

2. **Data Models** (`app/models/`)
   - `City`: Urban areas hosting events
   - `Event`: Individual events with metadata
   - `TourismMetric`: Daily tourism statistics
   - `HotelMetric`: Accommodation data
   - `EconomicMetric`: Economic impact data
   - `MobilityMetric`: Transportation data
   - `EventImpact`: Calculated impact analysis

3. **Analytics Engine** (`app/analytics/`)
   - `ImpactAnalyzer`: Core analysis engine
   - `ScenarioSimulator`: What-if simulations
   - Time series analysis
   - Comparative analytics

4. **Services Layer** (`app/services/`)
   - Business logic
   - External API integrations
   - Data processing utilities

5. **ETL Module** (`app/etl/`)
   - Data extraction from sources
   - Transformation and normalization
   - Loading into database

### Database Schema

**Cities Table:**
```sql
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code VARCHAR(3) NOT NULL,
    continent VARCHAR(50) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    population INTEGER,
    area_km2 FLOAT,
    gdp_usd FLOAT,
    annual_tourists INTEGER,
    hotel_rooms INTEGER,
    avg_hotel_price_usd FLOAT,
    metadata_json JSON,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

**Events Table:**
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(id),
    name VARCHAR(200) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    description VARCHAR(1000),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    year INTEGER NOT NULL,
    expected_attendance INTEGER,
    actual_attendance INTEGER,
    ticket_revenue_usd FLOAT,
    economic_impact_usd FLOAT,
    venue_name VARCHAR(200),
    venue_capacity INTEGER,
    venue_location JSON,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50),
    edition_number INTEGER,
    website_url VARCHAR(500),
    official_hashtag VARCHAR(100),
    metadata_json JSON,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

**Metrics Tables:**
- `tourism_metrics`: Daily visitor statistics
- `hotel_metrics`: Accommodation pricing and occupancy
- `economic_metrics`: Spending by category
- `mobility_metrics`: Transportation and congestion

**Impact Table:**
```sql
CREATE TABLE event_impacts (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    baseline_daily_visitors INTEGER,
    event_period_daily_visitors INTEGER,
    visitor_increase_pct FLOAT,
    additional_visitors INTEGER,
    baseline_occupancy_pct FLOAT,
    event_occupancy_pct FLOAT,
    occupancy_increase_pct FLOAT,
    baseline_avg_price_usd FLOAT,
    event_avg_price_usd FLOAT,
    price_increase_pct FLOAT,
    total_economic_impact_usd FLOAT,
    direct_spending_usd FLOAT,
    indirect_spending_usd FLOAT,
    induced_spending_usd FLOAT,
    jobs_created INTEGER,
    tax_revenue_usd FLOAT,
    roi_ratio FLOAT,
    calculated_at TIMESTAMP DEFAULT NOW()
);
```

## Analytics Methodology

### Impact Calculation

**1. Baseline Period:**
- 30 days before event (configurable)
- Calculate average daily metrics
- Establish normal patterns

**2. Event Period:**
- Event start to end date
- Measure actual metrics
- Identify peaks and anomalies

**3. Post-Event Period:**
- 14 days after event (configurable)
- Measure residual effects

**4. Comparison:**
```python
visitor_increase_pct = (
    (event_avg - baseline_avg) / baseline_avg
) * 100
```

### Economic Impact Model

**Direct Impact:**
- Visitor spending at event
- Hotel accommodation
- Food and beverage
- Retail purchases

**Indirect Impact (40% of direct):**
- Supply chain effects
- Wholesale trade
- Services to businesses

**Induced Impact (30% of direct):**
- Employee spending
- Household consumption
- Secondary effects

**Total Impact:**
```python
total_impact = direct + indirect + induced
```

### What-If Simulation

**Attendance Change Simulation:**
```python
def simulate_attendance_change(
    event_id: int,
    attendance_change_pct: float,
    price_elasticity: float = 0.3,
    spending_multiplier: float = 1.0
):
    # Scale visitor metrics
    attendance_multiplier = 1 + (attendance_change_pct / 100)
    projected_visitors = base_visitors * attendance_multiplier

    # Price response (elastic)
    price_multiplier = 1 + (attendance_change_pct / 100) * price_elasticity
    projected_price = base_price * price_multiplier

    # Economic impact
    spending_factor = attendance_multiplier * spending_multiplier
    projected_impact = base_impact * spending_factor

    return projected_scenario
```

## API Design

### RESTful Principles

- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Status codes (200, 201, 400, 404, 500)
- JSON request/response

### Endpoint Patterns

**CRUD Operations:**
```
GET    /api/v1/cities          # List all
GET    /api/v1/cities/{id}     # Get one
POST   /api/v1/cities          # Create
PUT    /api/v1/cities/{id}     # Update
DELETE /api/v1/cities/{id}     # Delete
```

**Analytics Operations:**
```
GET  /api/v1/events/{id}/impact
POST /api/v1/analytics/compare/events
POST /api/v1/analytics/compare/cities
GET  /api/v1/analytics/timeseries/{city_id}
POST /api/v1/analytics/whatif/attendance
```

### Request/Response Examples

**Get Event Impact:**
```bash
curl http://localhost:8000/api/v1/events/1/impact
```

Response:
```json
{
  "id": 1,
  "event_id": 1,
  "visitor_increase_pct": 35.2,
  "price_increase_pct": 22.5,
  "occupancy_increase_pct": 18.3,
  "total_economic_impact_usd": 45000000,
  "jobs_created": 850,
  "roi_ratio": 3.2
}
```

**What-If Simulation:**
```bash
curl -X POST http://localhost:8000/api/v1/analytics/whatif/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "attendance_change_pct": 25,
    "price_elasticity": 0.3,
    "spending_multiplier": 1.1
  }'
```

## Frontend Architecture

### Component Structure

```
src/
├── pages/              # Route components
│   ├── Dashboard.tsx
│   ├── EventsList.tsx
│   ├── EventDetails.tsx
│   ├── CitiesComparison.tsx
│   └── WhatIfSimulator.tsx
│
├── components/         # Reusable components
│   ├── charts/
│   ├── cards/
│   └── forms/
│
├── services/          # API client
│   └── api.ts
│
└── utils/            # Utilities
    └── formatters.ts
```

### State Management

**React Query** for server state:
- Automatic caching
- Background refetching
- Optimistic updates

```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['events'],
  queryFn: apiService.getEvents,
})
```

### Styling

**TailwindCSS** utility-first approach:
```tsx
<div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
  <h3 className="text-sm font-medium opacity-90">Total Events</h3>
  <p className="text-4xl font-bold mt-2">{count}</p>
</div>
```

## Data Flow

### Event Impact Analysis Flow

```
1. User requests event impact
   └─> GET /api/v1/events/{id}/impact

2. API checks for existing analysis
   └─> Query EventImpact table

3. If not exists or recalculate=true:
   └─> ImpactAnalyzer.calculate_event_impact()
       ├─> Get baseline metrics (30 days before)
       ├─> Get event period metrics
       ├─> Calculate tourism impact
       ├─> Calculate hotel impact
       ├─> Calculate economic impact
       ├─> Calculate mobility impact
       └─> Save EventImpact record

4. Return impact analysis to frontend
   └─> JSON response

5. Frontend displays results
   └─> Dashboard cards and charts
```

## Performance Considerations

### Database Optimization

- Indexes on foreign keys
- Composite indexes on (city_id, date)
- Connection pooling (10-20 connections)

### Caching Strategy

- Frontend: React Query (5 min TTL)
- Backend: Consider Redis for heavy computations
- Database: PostgreSQL query cache

### Batch Operations

```python
# Analyze multiple events in one request
POST /api/v1/events/batch-analyze
{
  "event_ids": [1, 2, 3, 4, 5]
}
```

## Security

### API Security

- CORS configuration
- Request validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)
- Rate limiting (future)
- Authentication (future)

### Data Validation

```python
class EventCreate(BaseModel):
    name: str = Field(..., max_length=200)
    start_date: date
    end_date: date

    @validator('end_date')
    def end_after_start(cls, v, values):
        if v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

**Test Coverage:**
- Unit tests for analytics functions
- Integration tests for API endpoints
- Database transaction tests

### Frontend Tests

```bash
cd frontend
npm test
```

## Deployment

### Docker Deployment

```bash
docker-compose up -d
```

Services:
- `db`: PostgreSQL database
- `backend`: FastAPI application
- `frontend`: React development server

### Production Deployment

**Backend:**
- Use Gunicorn with Uvicorn workers
- Nginx reverse proxy
- SSL/TLS certificates
- Environment-based configuration

**Frontend:**
- Build for production: `npm run build`
- Serve static files with Nginx
- CDN for assets

**Database:**
- Managed PostgreSQL (AWS RDS, Google Cloud SQL)
- Regular backups
- Read replicas for scaling

## Monitoring and Logging

### Application Logs

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Calculating impact for event {}", event_id)
```

### Metrics to Monitor

- API response times
- Database query performance
- Error rates
- User activity
- System resource usage

## Future Enhancements

### Phase 2 Features

1. **Machine Learning:**
   - Predictive models for event impact
   - Anomaly detection
   - Clustering similar events

2. **Real-time Data:**
   - Live event tracking
   - Real-time dashboard updates
   - WebSocket connections

3. **Advanced Visualizations:**
   - Interactive maps (Mapbox)
   - D3.js custom charts
   - Time-series forecasting

4. **Multi-tenancy:**
   - Organization accounts
   - Role-based access control
   - Custom branding

5. **Reporting:**
   - PDF report generation
   - Excel export
   - Scheduled reports

6. **External Integrations:**
   - AirROI API
   - Booking.com API
   - City tourism APIs
   - Event ticketing platforms

## Troubleshooting

### Common Issues

**Database Connection:**
```bash
# Check PostgreSQL status
docker-compose ps db
docker-compose logs db

# Test connection
psql postgresql://evently:evently123@localhost:5432/evently
```

**API Errors:**
```bash
# Check logs
docker-compose logs backend

# Test endpoint
curl http://localhost:8000/health
```

**Frontend Build:**
```bash
# Clear cache
rm -rf node_modules
npm install

# Check TypeScript
npm run build
```

## Contributing

See CONTRIBUTING.md for guidelines on:
- Code style
- Commit messages
- Pull request process
- Testing requirements

## Resources

- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- SQLAlchemy: https://www.sqlalchemy.org/
- PostgreSQL: https://www.postgresql.org/
- Docker: https://docs.docker.com/

---

**Version:** 1.0.0
**Last Updated:** 2024-01-15
**Maintainers:** Evently Development Team
