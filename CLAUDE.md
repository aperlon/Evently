# CLAUDE.md - AI Assistant Guide for Evently

> **Last Updated:** 2025-11-25
> **Version:** 1.0.0
> **Purpose:** Comprehensive guide for AI assistants working with the Evently codebase

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Codebase Structure](#2-codebase-structure)
3. [Tech Stack & Dependencies](#3-tech-stack--dependencies)
4. [Development Setup](#4-development-setup)
5. [Code Conventions & Patterns](#5-code-conventions--patterns)
6. [API Architecture](#6-api-architecture)
7. [Database Schema](#7-database-schema)
8. [Frontend Patterns](#8-frontend-patterns)
9. [Backend Patterns](#9-backend-patterns)
10. [ML & Analytics](#10-ml--analytics)
11. [Common Tasks](#11-common-tasks)
12. [Deployment](#12-deployment)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Project Overview

### What is Evently?

**Evently** is an Event Impact Analyzer - a full-stack web application that analyzes the economic and touristic impact of major urban events (sports, culture, music, festivals, conferences) across global cities.

### Core Capabilities

- **Impact Analysis**: Calculate economic impact, jobs created, ROI for events
- **Predictive Analytics**: ML-powered predictions for future event impacts
- **Comparative Analysis**: Compare events across cities and time periods
- **What-If Simulations**: Scenario modeling for event planning
- **Data Visualization**: Interactive 3D globe, charts, and dashboards

### Target Users

- City governments and local administrations
- Event organizers and planners
- Hotel chains and hospitality businesses
- Urban consultants and economists
- Academic researchers

### Current Status

- **MVP Complete**: 16 global cities across 5 continents
- **Data**: Synthetic realistic data + framework for real data integration
- **Deployment**: Ready for Vercel (frontend) + Railway (backend) + Supabase (database)

---

## 2. Codebase Structure

### High-Level Architecture

```
Evently/
├── backend/                    # FastAPI REST API + Analytics Engine
│   ├── app/
│   │   ├── api/               # API endpoints and schemas
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── services/          # Business logic services
│   │   ├── analytics/         # Impact analysis and simulations
│   │   ├── ml/                # Machine learning models
│   │   ├── core/              # Configuration and database setup
│   │   └── main.py            # FastAPI application entry point
│   ├── tests/                 # Unit and integration tests
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Container definition
│   └── Procfile               # Railway deployment config
│
├── frontend/                   # React + TypeScript Dashboard
│   ├── src/
│   │   ├── pages/             # Main application pages (10 pages)
│   │   ├── components/        # Reusable UI components
│   │   ├── services/          # API client and service layer
│   │   ├── App.tsx            # Root component with routing
│   │   ├── main.tsx           # App entry point + React Query
│   │   ├── index.css          # Global styles
│   │   └── fonts.css          # Custom font definitions
│   ├── public/                # Static assets
│   ├── media/                 # Brand images and logos
│   ├── package.json           # Node dependencies
│   ├── vite.config.ts         # Vite build configuration
│   ├── tsconfig.json          # TypeScript configuration
│   ├── tailwind.config.js     # TailwindCSS configuration
│   └── Dockerfile             # Container definition
│
├── data/                       # Data and ETL scripts
│   ├── examples/              # Sample CSV files (cities, events, metrics)
│   ├── scripts/               # Data processing and generation scripts
│   ├── processed/             # Processed data cache
│   ├── raw/                   # Raw data storage
│   └── schemas/               # Database schemas
│
├── docs/                       # Additional documentation
├── notebooks/                  # Jupyter notebooks (exploratory analysis)
│
├── docker-compose.yml         # Local development orchestration
├── vercel.json                # Vercel deployment config
├── package.json               # Root package.json (three.js dependency)
├── README.md                  # Main project documentation
├── DEPLOYMENT.md              # Production deployment guide
├── QUICKSTART.md              # Quick start guide (Spanish)
└── *.md                       # Various documentation files

```

### Key Directories

- **backend/app/api/**: All API endpoints and request/response schemas
- **backend/app/models/**: Database models (City, Event, EventImpact, Metrics)
- **backend/app/analytics/**: Core impact calculation and scenario simulation logic
- **backend/app/ml/**: Machine learning models for prediction
- **frontend/src/pages/**: Complete application pages (GlobeLanding, Dashboard, etc.)
- **frontend/src/services/api.ts**: Single source of truth for API communication
- **data/scripts/**: ETL scripts for data generation and import

### File Counts

- **Backend**: 26 Python files
- **Frontend**: 17 TypeScript/TSX files
- **Total Codebase**: ~16MB (excluding node_modules)
- **API Endpoints**: 20+ RESTful endpoints

---

## 3. Tech Stack & Dependencies

### Frontend Stack

```typescript
// Core Framework
React 18.2.0              // UI framework
TypeScript 5.3.3          // Type safety
Vite 5.0.11              // Build tool (ultra-fast HMR)
React Router 6.21.3       // Client-side routing

// State Management & Data Fetching
@tanstack/react-query 5.17.19  // Server state management
Axios 1.6.5                     // HTTP client

// 3D Visualization
react-globe.gl 2.27.0     // 3D interactive globe
Three.js 0.171.0          // WebGL 3D rendering
Cobe 0.6.5               // Additional globe effects

// Charts & Data Visualization
Recharts 2.10.4          // Interactive charts and graphs

// UI/UX
TailwindCSS 3.4.1        // Utility-first CSS framework
Framer Motion 12.23.24   // Professional animations
Lucide React 0.554.0     // 110+ high-quality icons
date-fns 3.2.0           // Date utilities

// Custom Fonts
- The Bold Font          // Display font
- VCR OSD Mono          // Monospace font
```

### Backend Stack

```python
# Web Framework
FastAPI 0.109.0          # Modern async API framework
Uvicorn 0.27.0          # ASGI server
Pydantic 2.5.3          # Data validation

# Database
SQLAlchemy 2.0.25       # ORM
PostgreSQL 15           # Relational database
Alembic 1.13.1          # Database migrations
psycopg2-binary 2.9.9   # PostgreSQL adapter

# Data Processing
Pandas 2.1.4            # Data manipulation
NumPy 1.26.3            # Numerical computing
PyArrow 14.0.2          # Columnar data
OpenPyXL 3.1.2          # Excel file support

# Machine Learning
Scikit-learn 1.4.0      # ML algorithms
Prophet 1.1.5           # Time series forecasting
XGBoost 2.0.3           # Gradient boosting
Statsmodels 0.14.1      # Statistical models
Joblib 1.3.2            # Model persistence

# Testing & Quality
Pytest 7.4.4            # Testing framework
Black 23.12.1           # Code formatting
MyPy 1.8.0              # Type checking
```

### Database

- **PostgreSQL 15**: Alpine Linux image
- **Optional**: TimescaleDB extension for time-series optimization
- **Connection Pooling**: 10 base connections, 20 max overflow

### DevOps

- **Docker & Docker Compose**: Containerization and local orchestration
- **Vercel**: Frontend deployment (recommended)
- **Railway/Render**: Backend deployment options
- **Supabase**: Managed PostgreSQL (recommended)

---

## 4. Development Setup

### Prerequisites

**Without Docker (Faster for Development):**
- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Git

**With Docker:**
- Docker Desktop
- Docker Compose

### Quick Start (Choose One)

#### Option 1: Automatic Script (Easiest)

```bash
# With Docker (automatic setup)
./start.sh

# Without Docker (faster, manual PostgreSQL required)
./dev.sh
```

#### Option 2: Manual Setup (Recommended for Active Development)

```bash
# Terminal 1: Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup database
export DATABASE_URL="postgresql://evently:evently123@localhost:5432/evently"
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Generate sample data
cd ..
python data/scripts/generate_sample_data.py

# Start backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

#### Option 3: Docker Compose

```bash
docker-compose up -d
docker-compose exec backend python /data/scripts/generate_sample_data.py
```

### Access URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs (Swagger UI)
- **Database**: localhost:5432 (if running locally)

### Environment Variables

#### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://evently:evently123@localhost:5432/evently

# Security
SECRET_KEY=your-secret-key-change-in-production

# CORS (add frontend URL)
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Optional: External APIs
AIRROI_API_KEY=your-api-key-if-available
```

#### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

---

## 5. Code Conventions & Patterns

### General Principles

1. **Type Safety**: Use TypeScript strict mode (frontend) and type hints (backend)
2. **Separation of Concerns**: Keep business logic separate from API routes
3. **DRY Principle**: Avoid code duplication, create reusable components/functions
4. **Explicit over Implicit**: Clear, readable code over clever tricks
5. **Documentation**: Docstrings for Python functions, JSDoc for TypeScript when needed

### Naming Conventions

#### Backend (Python)

```python
# Files and modules: snake_case
# api_endpoints.py, impact_analyzer.py

# Classes: PascalCase
class EventImpact:
    pass

class ImpactAnalyzer:
    pass

# Functions and variables: snake_case
def calculate_event_impact(event_id: int) -> EventImpact:
    total_economic_impact = 0.0
    return impact

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_MULTIPLIER = 1.7
API_V1_STR = "/api/v1"

# Private methods: _leading_underscore
def _internal_helper():
    pass
```

#### Frontend (TypeScript/React)

```typescript
// Files: PascalCase for components, camelCase for utilities
// GlobeLanding.tsx, EventDetails.tsx, api.ts

// Components: PascalCase
function EventCard({ event }: { event: Event }) {
  return <div>...</div>
}

// Functions and variables: camelCase
const calculateImpact = (attendance: number): number => {
  return attendance * multiplier
}

// Interfaces and Types: PascalCase
interface EventImpact {
  totalImpact: number
  jobsCreated: number
}

type EventType = 'sports' | 'music' | 'culture'

// Constants: UPPER_SNAKE_CASE or camelCase (modern preference)
const API_BASE_URL = 'http://localhost:8000/api/v1'
const defaultMultiplier = 1.7
```

### Code Style

#### Backend (Python)

- **Formatter**: Black (line length: 100)
- **Linter**: MyPy for type checking
- **Docstrings**: Google style

```python
def calculate_event_impact(
    event_id: int,
    db: Session,
    recalculate: bool = False
) -> EventImpact:
    """
    Calculate the economic impact of an event.

    Args:
        event_id: The ID of the event to analyze
        db: Database session
        recalculate: Whether to force recalculation

    Returns:
        EventImpact object with calculated metrics

    Raises:
        ValueError: If event not found
    """
    # Implementation
    pass
```

#### Frontend (TypeScript)

- **Formatter**: Prettier (via Vite)
- **Linter**: ESLint (standard React rules)
- **Style**: Functional components with hooks

```typescript
// Good: Functional component with TypeScript
interface EventCardProps {
  event: Event
  onSelect?: (id: number) => void
}

export function EventCard({ event, onSelect }: EventCardProps) {
  const handleClick = () => {
    onSelect?.(event.id)
  }

  return (
    <div onClick={handleClick}>
      {event.name}
    </div>
  )
}

// Avoid: Class components (unless necessary)
```

### Import Organization

#### Backend (Python)

```python
# Standard library imports
from datetime import datetime, date
from typing import List, Optional

# Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

# Local application imports
from app.models.event import Event
from app.core.database import get_db
from app.api.schemas import EventResponse
```

#### Frontend (TypeScript)

```typescript
// React imports
import { useState, useEffect } from 'react'

// Third-party imports
import { useQuery } from '@tanstack/react-query'
import { useParams, useNavigate } from 'react-router-dom'

// Local imports
import { apiService, Event } from '../services/api'
import { EventCard } from '../components/EventCard'
```

---

## 6. API Architecture

### API Versioning

- **Base URL**: `http://localhost:8000/api/v1`
- **Version**: v1 (current)
- **Format**: RESTful JSON API

### Endpoint Structure

```
/api/v1/
├── cities/                    # City CRUD operations
├── events/                    # Event CRUD operations
├── analytics/                 # Analytics and comparisons
│   ├── dashboard/kpis        # Dashboard metrics
│   ├── timeseries/{city_id}  # Time series data
│   ├── compare/events        # Event comparison
│   ├── compare/cities        # City comparison
│   └── whatif/               # Scenario simulations
├── predict/                   # ML predictions
│   ├── options               # Available prediction options
│   └── (POST)                # Make prediction
└── upload/                    # File upload endpoints
    ├── cities                # Upload cities CSV/XLSX
    ├── events                # Upload events CSV/XLSX
    ├── hotel-metrics         # Upload hotel data
    └── tourism-metrics       # Upload tourism data
```

### Key Endpoints Reference

#### Cities

```
GET    /api/v1/cities              # List all cities
GET    /api/v1/cities/{id}         # Get city by ID
POST   /api/v1/cities              # Create new city
PUT    /api/v1/cities/{id}         # Update city
DELETE /api/v1/cities/{id}         # Delete city
```

#### Events

```
GET    /api/v1/events              # List events (filterable)
GET    /api/v1/events/{id}         # Get event by ID
POST   /api/v1/events              # Create new event
GET    /api/v1/events/{id}/impact  # Get/calculate event impact
POST   /api/v1/events/batch-analyze # Bulk impact analysis
```

#### Analytics

```
GET    /api/v1/analytics/dashboard/kpis        # Dashboard KPIs
GET    /api/v1/analytics/timeseries/{city_id}  # Time series data
POST   /api/v1/analytics/compare/events        # Compare events
POST   /api/v1/analytics/compare/cities        # Compare cities
POST   /api/v1/analytics/whatif/attendance     # Attendance scenario
GET    /api/v1/analytics/whatif/growth/{id}    # Multi-year growth
```

#### ML Predictions

```
GET    /api/v1/predict/options     # Get available options
POST   /api/v1/predict             # Predict event impact
POST   /api/v1/predict/detailed    # Detailed prediction
```

### Request/Response Patterns

#### Standard Response Format

```json
// Success Response
{
  "id": 1,
  "name": "London",
  "country": "United Kingdom",
  "population": 9000000,
  "created_at": "2024-01-01T00:00:00Z"
}

// Error Response
{
  "detail": "Event not found"
}
```

#### Pagination (Future Enhancement)

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

### Authentication (Not Yet Implemented)

Future implementation will use:
- JWT tokens
- Bearer authentication
- Token refresh mechanism

---

## 7. Database Schema

### Core Tables

#### cities

```sql
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
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
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

#### events

```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(id),
    name VARCHAR(200) NOT NULL,
    event_type VARCHAR(50) NOT NULL,  -- sports, music, culture, etc.
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    expected_attendance INTEGER,
    actual_attendance INTEGER,
    ticket_revenue_usd FLOAT,
    economic_impact_usd FLOAT,
    venue_name VARCHAR(200),
    venue_capacity INTEGER,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50),
    edition_number INTEGER,
    website_url VARCHAR(500),
    official_hashtag VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

#### event_impacts

```sql
CREATE TABLE event_impacts (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id) UNIQUE,
    baseline_daily_visitors FLOAT,
    event_period_daily_visitors FLOAT,
    visitor_increase_pct FLOAT NOT NULL,
    additional_visitors INTEGER,
    baseline_avg_hotel_price FLOAT,
    event_avg_hotel_price FLOAT,
    price_increase_pct FLOAT NOT NULL,
    baseline_occupancy_rate FLOAT,
    event_occupancy_rate FLOAT,
    occupancy_increase_pct FLOAT NOT NULL,
    total_economic_impact_usd FLOAT NOT NULL,
    direct_spending_usd FLOAT,
    indirect_spending_usd FLOAT,
    jobs_created INTEGER NOT NULL,
    roi_ratio FLOAT NOT NULL,
    analysis_start_date DATE,
    analysis_end_date DATE,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

#### Time-Series Tables

```sql
-- Tourism metrics (daily)
CREATE TABLE tourism_metrics (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(id),
    date DATE NOT NULL,
    daily_visitors INTEGER,
    international_visitors INTEGER,
    domestic_visitors INTEGER,
    avg_stay_days FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Hotel metrics (daily)
CREATE TABLE hotel_metrics (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(id),
    date DATE NOT NULL,
    occupancy_rate FLOAT,
    avg_daily_rate_usd FLOAT,
    revenue_per_available_room FLOAT,
    available_rooms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Economic metrics (daily)
CREATE TABLE economic_metrics (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(id),
    date DATE NOT NULL,
    daily_spending_usd FLOAT,
    retail_sales_usd FLOAT,
    food_beverage_sales_usd FLOAT,
    transport_spending_usd FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Mobility metrics (daily)
CREATE TABLE mobility_metrics (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(id),
    date DATE NOT NULL,
    airport_arrivals INTEGER,
    train_arrivals INTEGER,
    public_transport_usage_pct FLOAT,
    traffic_index FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Relationships

```
cities (1) ----< (N) events
events (1) ----< (1) event_impacts

cities (1) ----< (N) tourism_metrics
cities (1) ----< (N) hotel_metrics
cities (1) ----< (N) economic_metrics
cities (1) ----< (N) mobility_metrics
```

### SQLAlchemy Model Pattern

```python
# backend/app/models/event.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Relationships
    city = relationship("City", back_populates="events")
    impact = relationship("EventImpact", back_populates="event", uselist=False)
```

---

## 8. Frontend Patterns

### Component Structure

```typescript
// Standard functional component pattern
import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiService, Event } from '../services/api'

export function EventsList() {
  // State hooks
  const [selectedCity, setSelectedCity] = useState<number | null>(null)

  // React Query for data fetching
  const { data: events, isLoading, error } = useQuery({
    queryKey: ['events', selectedCity],
    queryFn: () => apiService.getEvents({ city_id: selectedCity || undefined }),
    staleTime: 15 * 60 * 1000, // 15 minutes
  })

  // Event handlers
  const handleCityChange = (cityId: number) => {
    setSelectedCity(cityId)
  }

  // Render
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading events</div>

  return (
    <div>
      {events?.map(event => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  )
}
```

### React Query Setup

```typescript
// frontend/src/main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 15 * 60 * 1000,    // 15 minutes
      refetchOnWindowFocus: false,   // Don't refetch on window focus
      retry: 1,                      // Only retry once on failure
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
)
```

### Routing Pattern

```typescript
// frontend/src/App.tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <Routes>
        {/* Full-screen pages (no layout) */}
        <Route path="/" element={<GlobeLanding />} />

        {/* Pages with layout (header + footer) */}
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/events" element={<EventsList />} />
          <Route path="/events/:id" element={<EventDetails />} />
          <Route path="/predict" element={<EventPredictor />} />
          <Route path="/about" element={<AboutUs />} />
        </Route>
      </Routes>
    </Router>
  )
}
```

### API Service Pattern

All API calls go through a centralized service:

```typescript
// frontend/src/services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  getCities: async (): Promise<City[]> => {
    const response = await api.get('/cities')
    return response.data
  },

  getEvents: async (filters?: EventFilters): Promise<Event[]> => {
    const response = await api.get('/events', { params: filters })
    return response.data
  },

  predictEvent: async (params: PredictionParams) => {
    const response = await api.post('/predict', params)
    return response.data
  },
}
```

### Styling with TailwindCSS

```tsx
// Use Tailwind utility classes
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
  <h1 className="text-3xl font-display text-gray-900">
    Evently
  </h1>
  <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
    Analyze Event
  </button>
</div>

// Custom colors defined in tailwind.config.js
<div className="bg-mellow-cream text-mellow-peach">
  Custom branded colors
</div>
```

### Animation with Framer Motion

```tsx
import { motion } from 'framer-motion'

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  <EventCard event={event} />
</motion.div>
```

---

## 9. Backend Patterns

### FastAPI Router Pattern

```python
# backend/app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.schemas import EventResponse, EventCreate

router = APIRouter(tags=["events"])

@router.get("/events", response_model=List[EventResponse])
async def get_events(
    city_id: Optional[int] = None,
    event_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve list of events with optional filters.
    """
    query = db.query(Event)
    if city_id:
        query = query.filter(Event.city_id == city_id)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    return query.all()

@router.post("/events", response_model=EventResponse, status_code=201)
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new event.
    """
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
```

### Dependency Injection for Database

```python
# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """
    Database session dependency.
    Use with FastAPI Depends() for automatic cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Pydantic Schema Validation

```python
# backend/app/api/schemas.py
from pydantic import BaseModel, Field, validator
from datetime import date

class EventCreate(BaseModel):
    """Schema for creating an event"""
    name: str = Field(..., max_length=200)
    city_id: int
    start_date: date
    end_date: date
    expected_attendance: Optional[int] = None

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class EventResponse(BaseModel):
    """Schema for event response"""
    id: int
    name: str
    city_id: int
    start_date: date
    end_date: date

    class Config:
        from_attributes = True  # For SQLAlchemy models
```

### Business Logic Pattern

Separate business logic from API endpoints:

```python
# backend/app/analytics/impact_analyzer.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

class ImpactAnalyzer:
    """Service class for calculating event impacts"""

    def __init__(self, db: Session):
        self.db = db

    def calculate_event_impact(self, event_id: int) -> EventImpact:
        """
        Calculate the economic impact of an event.

        Args:
            event_id: The ID of the event to analyze

        Returns:
            EventImpact object with all calculated metrics
        """
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise ValueError(f"Event {event_id} not found")

        # Define analysis windows
        baseline_start = event.start_date - timedelta(days=30)
        baseline_end = event.start_date - timedelta(days=1)

        # Calculate metrics
        baseline_metrics = self._get_baseline_metrics(event.city_id, baseline_start, baseline_end)
        event_metrics = self._get_event_metrics(event.city_id, event.start_date, event.end_date)

        # Calculate impact
        impact = self._calculate_impact(baseline_metrics, event_metrics, event)

        return impact
```

### Error Handling

```python
from fastapi import HTTPException

@router.get("/events/{event_id}")
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/predict")
async def predict_event(params: PredictionParams):
    try:
        model = get_ml_model()
        prediction = model.predict(params)
        return prediction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## 10. ML & Analytics

### ML Model Architecture

**Algorithm**: Gradient Boosting Regressor (scikit-learn)

**Performance Metrics**:
- R² Score: 0.9719 (97.19% variance explained)
- MAPE: 11.63% (Mean Absolute Percentage Error)
- Training time: ~2-3 seconds
- Prediction time: <100ms

**Features Used (14 total)**:
1. Event characteristics: type, duration, attendance
2. City characteristics: population, annual tourists, hotel capacity
3. Time-series baselines: avg visitors, occupancy, prices (30 days before)
4. Seasonal factors: month, day of week
5. Historical patterns: event type × city combinations

### ML Model Pattern

```python
# backend/app/ml/economic_impact_model.py
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import pandas as pd

class EconomicImpactModel:
    """
    Machine learning model for predicting event economic impact.
    """

    def __init__(self):
        self.model = None
        self.feature_columns = [...]  # 14 feature names

    def train(self, training_data: pd.DataFrame):
        """Train the model on historical event data"""
        X = training_data[self.feature_columns]
        y = training_data['total_economic_impact_usd']

        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X, y)

    def predict(self, event_params: dict) -> dict:
        """
        Predict economic impact for a new event.

        Returns:
            dict with prediction, confidence interval, jobs created, etc.
        """
        features = self._extract_features(event_params)
        predicted_impact = self.model.predict([features])[0]

        # Calculate additional metrics
        jobs_created = self._calculate_jobs(predicted_impact, event_params['city'])
        roi = self._calculate_roi(predicted_impact, event_params)

        return {
            'total_economic_impact_usd': predicted_impact,
            'jobs_created': jobs_created,
            'roi_ratio': roi,
            'confidence_score': 0.85  # Based on model R²
        }

    def save(self, filepath: str):
        """Save trained model to disk"""
        joblib.dump(self.model, filepath)

    def load(self, filepath: str):
        """Load trained model from disk"""
        self.model = joblib.load(filepath)
```

### Singleton Pattern for ML Model

```python
# backend/app/ml/predictors.py
_ml_model = None

def get_ml_model() -> EconomicImpactModel:
    """
    Get singleton instance of ML model.
    Loads model from disk on first call.
    """
    global _ml_model
    if _ml_model is None:
        _ml_model = EconomicImpactModel()
        _ml_model.load('backend/app/ml/saved_models/gradient_boosting_model.pkl')
    return _ml_model
```

### Impact Calculation Logic

```python
# backend/app/analytics/impact_analyzer.py
class ImpactAnalyzer:

    def calculate_event_impact(self, event_id: int) -> EventImpact:
        """
        Calculate impact using time-series comparison:
        1. Baseline period: 30 days before event
        2. Event period: event dates
        3. Post-event period: 14 days after (optional)
        """

        # Get baseline metrics (30 days before)
        baseline = self._aggregate_metrics(
            city_id=event.city_id,
            start_date=event.start_date - timedelta(days=30),
            end_date=event.start_date - timedelta(days=1)
        )

        # Get event period metrics
        event_period = self._aggregate_metrics(
            city_id=event.city_id,
            start_date=event.start_date,
            end_date=event.end_date
        )

        # Calculate percentage changes
        visitor_increase_pct = (
            (event_period.avg_daily_visitors - baseline.avg_daily_visitors)
            / baseline.avg_daily_visitors * 100
        )

        # Calculate total economic impact
        duration_days = (event.end_date - event.start_date).days + 1
        additional_visitors = (
            event_period.avg_daily_visitors - baseline.avg_daily_visitors
        ) * duration_days

        avg_spending_per_visitor = 150  # USD (city-specific)
        direct_spending = additional_visitors * avg_spending_per_visitor

        # Apply economic multiplier
        multiplier = 1.7  # Default multiplier
        total_impact = direct_spending * multiplier

        # Calculate jobs created (city-specific ratio)
        jobs_per_million = event.city.jobs_per_million_usd or 22
        jobs_created = int(total_impact / 1_000_000 * jobs_per_million)

        return EventImpact(
            event_id=event_id,
            visitor_increase_pct=visitor_increase_pct,
            total_economic_impact_usd=total_impact,
            jobs_created=jobs_created,
            # ... other fields
        )
```

### Economic Multipliers

```python
# Default multipliers used
ECONOMIC_MULTIPLIER = 1.7        # Direct spending → Total economic impact
JOBS_PER_MILLION_USD = {
    'default': 22,
    'london': 18,
    'paris': 20,
    'rio_de_janeiro': 30,
    # ... city-specific ratios
}

AVG_SPENDING_PER_VISITOR = {
    'default': 150,
    'luxury_cities': 250,
    'budget_cities': 100,
}
```

---

## 11. Common Tasks

### Adding a New API Endpoint

1. Define Pydantic schema in `backend/app/api/schemas.py`
2. Add endpoint to `backend/app/api/endpoints.py`
3. Add corresponding function to `frontend/src/services/api.ts`
4. Use in component with React Query

```python
# 1. Backend schema
class NewFeatureRequest(BaseModel):
    param1: str
    param2: int

class NewFeatureResponse(BaseModel):
    result: str

# 2. Backend endpoint
@router.post("/new-feature", response_model=NewFeatureResponse)
async def new_feature(request: NewFeatureRequest, db: Session = Depends(get_db)):
    # Implementation
    return NewFeatureResponse(result="success")
```

```typescript
// 3. Frontend service
export const apiService = {
  // ... existing methods

  newFeature: async (params: { param1: string; param2: number }) => {
    const response = await api.post('/new-feature', params)
    return response.data
  }
}

// 4. Use in component
const { data, isLoading } = useQuery({
  queryKey: ['new-feature'],
  queryFn: () => apiService.newFeature({ param1: 'test', param2: 123 })
})
```

### Adding a New Page

1. Create component in `frontend/src/pages/NewPage.tsx`
2. Add route in `frontend/src/App.tsx`
3. Add navigation link in header

```tsx
// 1. Create page
// frontend/src/pages/NewPage.tsx
export default function NewPage() {
  return (
    <div>
      <h1>New Page</h1>
    </div>
  )
}

// 2. Add route
// frontend/src/App.tsx
import NewPage from './pages/NewPage'

<Route path="/new-page" element={<NewPage />} />

// 3. Add navigation
<Link to="/new-page" className="text-gray-800 hover:text-gray-900">
  New Page
</Link>
```

### Adding a New Database Model

1. Create model in `backend/app/models/`
2. Update database (run migrations or recreate)
3. Create Pydantic schemas
4. Add CRUD endpoints

```python
# 1. Create model
# backend/app/models/new_model.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class NewModel(Base):
    __tablename__ = "new_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

# 2. Create tables
from app.core.database import Base, engine
Base.metadata.create_all(bind=engine)

# 3. Create schemas
class NewModelResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
```

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests (if configured)
cd frontend
npm test

# Run specific test file
pytest tests/test_impact_analyzer.py -v

# Run with coverage
pytest --cov=app tests/
```

### Generating Sample Data

```bash
# From project root
python data/scripts/generate_sample_data.py

# This will:
# 1. Create 16 cities
# 2. Generate 1,102 events
# 3. Create 5,856 daily records per metric type
# 4. Calculate event impacts
```

### Database Migrations (Future)

```bash
# Initialize Alembic (if not already done)
cd backend
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Adding a New City

```python
# Via Python script
from app.core.database import SessionLocal
from app.models.city import City

db = SessionLocal()
new_city = City(
    name="Tokyo",
    country="Japan",
    country_code="JP",
    continent="Asia",
    latitude=35.6762,
    longitude=139.6503,
    timezone="Asia/Tokyo",
    population=13960000,
    annual_tourists=15000000,
    hotel_rooms=150000,
    avg_hotel_price_usd=180
)
db.add(new_city)
db.commit()
```

Or via CSV upload through the API (recommended):
```bash
POST /api/v1/upload/cities
Content-Type: multipart/form-data
file: cities.csv
```

### Training ML Model

```bash
# Train/retrain the economic impact model
cd backend
python app/ml/train_model.py

# This will:
# 1. Load historical event data
# 2. Extract features
# 3. Train Gradient Boosting model
# 4. Save model to app/ml/saved_models/
# 5. Print performance metrics
```

---

## 12. Deployment

### Quick Deployment (Recommended Stack)

**Frontend: Vercel**
1. Go to https://vercel.com
2. Import GitHub repository
3. Configure:
   - Framework: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment Variable: `VITE_API_URL=<your-backend-url>`
4. Deploy (auto-deploys on every push to main)

**Database: Supabase**
1. Go to https://supabase.com
2. Create new project
3. Copy PostgreSQL connection string
4. Create tables:
   ```bash
   cd backend
   export DATABASE_URL=<supabase-connection-string>
   python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
   python ../data/scripts/generate_sample_data.py
   ```

**Backend: Railway**
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select repository
4. Configure:
   - Root Directory: `backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     - `DATABASE_URL=<supabase-connection-string>`
     - `SECRET_KEY=<generate-random-key>`
     - `BACKEND_CORS_ORIGINS=["https://your-app.vercel.app"]`
5. Deploy (auto-deploys on every push)

**Total Cost**: $0-5/month (all have free tiers)

**Deployment Time**: ~10 minutes total

### Environment Configuration

#### Production Backend (.env)

```bash
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY=<generate-with-python -c "import secrets; print(secrets.token_urlsafe(32))">
BACKEND_CORS_ORIGINS=["https://evently.vercel.app"]
AIRROI_API_KEY=<optional>
```

#### Production Frontend (.env)

```bash
VITE_API_URL=https://evently-production.up.railway.app/api/v1
```

### Docker Deployment

```bash
# Build images
docker-compose build

# Run in production mode
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Security Checklist

- [ ] Change `SECRET_KEY` to a random secure value
- [ ] Enable HTTPS (Vercel/Railway provide this automatically)
- [ ] Restrict CORS to production domain only
- [ ] Never commit `.env` files to Git
- [ ] Use environment variables for all secrets
- [ ] Enable rate limiting (consider adding slowapi)
- [ ] Review database connection limits
- [ ] Enable database backups

### Monitoring

**Railway/Render**:
- Real-time logs in dashboard
- CPU/RAM metrics
- Request/response times

**Vercel**:
- Web analytics
- Web Vitals (performance metrics)
- Build logs

**Supabase**:
- Database usage
- Query performance
- Connection pooling stats

### CI/CD

**Automatic Deployments**:
- Push to `main` branch → Auto-deploy to production
- Pull requests → Preview deployments (Vercel)
- All providers support GitHub integration

**Manual Deployment**:
```bash
# Vercel CLI
vercel --prod

# Railway CLI
railway up
```

---

## 13. Troubleshooting

### Common Issues & Solutions

#### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Run with correct path
uvicorn app.main:app --reload
```

#### Database connection error

**Error**: `could not connect to server: Connection refused`

**Solution**:
```bash
# Check if PostgreSQL is running
pg_isready

# Check DATABASE_URL
echo $DATABASE_URL

# Verify credentials
psql $DATABASE_URL

# If using Docker
docker-compose ps
docker-compose up -d db
```

#### Frontend can't reach backend (CORS error)

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
1. Check `VITE_API_URL` in frontend `.env`
2. Verify backend `BACKEND_CORS_ORIGINS` includes frontend URL
3. Restart both frontend and backend

```python
# backend/app/core/config.py
BACKEND_CORS_ORIGINS = [
    "http://localhost:3000",    # Development
    "https://your-app.vercel.app"  # Production
]
```

#### ML model predictions fail

**Error**: `FileNotFoundError: saved_models/gradient_boosting_model.pkl`

**Solution**:
```bash
# Train and save the model
cd backend
python app/ml/train_model.py

# Verify model file exists
ls -la app/ml/saved_models/
```

#### React Query not refetching data

**Issue**: Data not updating after changes

**Solution**:
```typescript
// Invalidate query after mutation
import { useQueryClient } from '@tanstack/react-query'

const queryClient = useQueryClient()

// After creating/updating data
queryClient.invalidateQueries({ queryKey: ['events'] })
```

#### Build fails on Vercel

**Error**: `Cannot find module 'three'`

**Solution**:
- Verify `package.json` includes all dependencies
- Check that `frontend` directory structure is correct
- Ensure `rootDirectory` is set to `frontend` in Vercel settings

#### Out of memory (Railway/Render)

**Error**: `Process killed (out of memory)`

**Solution**:
1. Upgrade to plan with more RAM
2. Optimize database queries (add indexes)
3. Reduce concurrent connections
4. Consider pagination for large datasets

#### Slow page loads

**Issues**: Dashboard taking >5 seconds to load

**Solutions**:
1. Check database indexes:
   ```sql
   CREATE INDEX idx_events_city_id ON events(city_id);
   CREATE INDEX idx_tourism_metrics_city_date ON tourism_metrics(city_id, date);
   ```

2. Add React Query caching:
   ```typescript
   const { data } = useQuery({
     queryKey: ['events'],
     queryFn: apiService.getEvents,
     staleTime: 15 * 60 * 1000,  // Cache for 15 minutes
   })
   ```

3. Paginate large datasets
4. Use connection pooling (already configured)

---

## Quick Reference Commands

```bash
# Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev

# Database (local)
psql postgresql://evently:evently123@localhost:5432/evently

# Generate data
python data/scripts/generate_sample_data.py

# Train ML model
cd backend && python app/ml/train_model.py

# Run tests
cd backend && pytest

# Docker
docker-compose up -d
docker-compose logs -f backend
docker-compose exec backend bash

# Git
git status
git add .
git commit -m "feat: description"
git push origin main
```

---

## Additional Resources

- **Main Documentation**: [README.md](README.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Setup Guide**: [SETUP.md](SETUP.md)
- **ML Documentation**: [MODELO_ML_DOCUMENTACION.md](MODELO_ML_DOCUMENTACION.md)
- **API Documentation**: http://localhost:8000/api/v1/docs (when running)

---

## Key Takeaways for AI Assistants

1. **Architecture**: Separate frontend (React) and backend (FastAPI) with PostgreSQL database
2. **Data Flow**: Frontend → API Service → FastAPI Endpoints → SQLAlchemy ORM → PostgreSQL
3. **Conventions**: TypeScript strict mode, Python type hints, functional components, dependency injection
4. **API**: RESTful JSON API at `/api/v1/*` with Pydantic validation
5. **State**: React Query for server state, useState for local state
6. **Styling**: TailwindCSS utility classes with Framer Motion for animations
7. **ML**: Gradient Boosting model for predictions, ImpactAnalyzer for historical analysis
8. **Deployment**: Vercel (frontend) + Railway (backend) + Supabase (database) = Free/Low-cost
9. **Development**: Use `./dev.sh` for fastest local development without Docker
10. **Documentation**: API docs auto-generated at `/api/v1/docs` via FastAPI

---

**Last Updated**: November 25, 2025
**Maintainer**: Evently Team
**License**: MIT
