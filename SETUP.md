# Evently Setup Guide

Complete setup instructions for the Event Impact Analyzer prototype.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** and **Docker Compose** (recommended for easiest setup)
- **Python 3.11+** (for local development)
- **Node.js 18+** and npm (for frontend development)
- **PostgreSQL 15** (if running without Docker)

## Quick Start with Docker (Recommended)

The fastest way to get Evently running:

```bash
# 1. Clone the repository
git clone https://github.com/aperlon/Evently.git
cd Evently

# 2. Start all services
docker-compose up -d

# 3. Wait for services to be ready (about 30 seconds)
docker-compose logs -f

# 4. Generate sample data
docker-compose exec backend python /app/../data/scripts/generate_sample_data.py

# 5. Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/api/v1/docs
```

## Local Development Setup

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Generate sample data
cd ..
python data/scripts/generate_sample_data.py

# Start the API server
cd backend
uvicorn app.main:app --reload

# API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/api/v1/docs
```

### Frontend Setup

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will be available at http://localhost:3000
```

### Database Setup (Without Docker)

```bash
# Install PostgreSQL 15

# Create database
createdb evently

# Create user (if needed)
psql -c "CREATE USER evently WITH PASSWORD 'evently123';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE evently TO evently;"

# Update DATABASE_URL in backend/.env
DATABASE_URL=postgresql://evently:evently123@localhost:5432/evently
```

## Sample Data Generation

The sample data generator creates realistic data for:

**Cities:**
- London, UK
- Tokyo, Japan
- Paris, France
- New York, USA
- Madrid, Spain
- Berlin, Germany

**Events (2024):**
- London Marathon
- Wimbledon
- Tokyo Marathon
- Roland Garros
- US Open
- NYC Marathon
- Champions League Final
- And more...

**Metrics:** Full year 2024 daily metrics for:
- Tourism (visitors, spending)
- Hotels (occupancy, pricing)
- Economic impact (spending by category)
- Mobility (transportation, congestion)

```bash
# Run the data generator
python data/scripts/generate_sample_data.py

# Output:
# ✓ Database tables created
# ✓ Created 6 cities
# ✓ Created 12 events
# ✓ Generated all metrics
```

## Using the Application

### 1. Dashboard

Visit http://localhost:3000 to see:
- Total events analyzed
- Average economic impact
- Total jobs created
- Visitor and price increase metrics

### 2. Browse Events

Navigate to http://localhost:3000/events to:
- See all analyzed events
- Filter by city, type, or year
- Click on an event to see detailed impact analysis

### 3. Analyze Event Impact

Use the API to calculate event impacts:

```bash
# Get event impact analysis
curl http://localhost:8000/api/v1/events/1/impact

# Force recalculation
curl http://localhost:8000/api/v1/events/1/impact?recalculate=true
```

### 4. Compare Events or Cities

```bash
# Compare multiple events
curl -X POST http://localhost:8000/api/v1/analytics/compare/events \
  -H "Content-Type: application/json" \
  -d '[1, 2, 3]'

# Compare cities
curl -X POST http://localhost:8000/api/v1/analytics/compare/cities \
  -H "Content-Type: application/json" \
  -d '[1, 2, 3]'
```

### 5. What-If Scenarios

Simulate different scenarios:

```bash
# Simulate 20% attendance increase
curl -X POST http://localhost:8000/api/v1/analytics/whatif/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "attendance_change_pct": 20,
    "price_elasticity": 0.3,
    "spending_multiplier": 1.0
  }'

# Simulate 5-year growth
curl http://localhost:8000/api/v1/analytics/whatif/growth/1?years=5&annual_growth_pct=10
```

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### Key Endpoints

**Cities:**
- `GET /api/v1/cities` - List all cities
- `GET /api/v1/cities/{id}` - Get city details
- `POST /api/v1/cities` - Create new city

**Events:**
- `GET /api/v1/events` - List all events (with filters)
- `GET /api/v1/events/{id}` - Get event details
- `POST /api/v1/events` - Create new event

**Impact Analysis:**
- `GET /api/v1/events/{id}/impact` - Get event impact analysis
- `POST /api/v1/events/batch-analyze` - Analyze multiple events

**Analytics:**
- `GET /api/v1/analytics/timeseries/{city_id}` - Time series data
- `POST /api/v1/analytics/compare/events` - Compare events
- `POST /api/v1/analytics/compare/cities` - Compare cities
- `GET /api/v1/analytics/dashboard/kpis` - Dashboard KPIs

**Simulations:**
- `POST /api/v1/analytics/whatif/attendance` - Simulate attendance change
- `GET /api/v1/analytics/whatif/growth/{id}` - Simulate growth trajectory

## Architecture Overview

```
Evently/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints and schemas
│   │   ├── models/      # SQLAlchemy database models
│   │   ├── analytics/   # Impact analyzer & simulator
│   │   ├── core/        # Configuration & database
│   │   └── main.py      # FastAPI application
│   └── requirements.txt
│
├── frontend/            # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/      # Dashboard, Events, etc.
│   │   ├── services/   # API client
│   │   └── main.tsx    # React entry point
│   └── package.json
│
├── data/               # Data and scripts
│   ├── scripts/        # Data generation scripts
│   ├── raw/           # Raw data (from external sources)
│   └── processed/     # Processed data
│
└── docker-compose.yml # Docker orchestration
```

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Pandas & NumPy (Data processing)
- Scikit-learn (Analytics)

**Frontend:**
- React 18 (UI framework)
- TypeScript (Type safety)
- Vite (Build tool)
- TailwindCSS (Styling)
- Recharts (Visualizations)
- React Query (Data fetching)

**DevOps:**
- Docker & Docker Compose
- PostgreSQL 15
- Nginx (production)

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Frontend Not Loading

```bash
# Check if API is running
curl http://localhost:8000/health

# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
cd frontend && npm install && npm run dev
```

### No Data in Dashboard

Make sure you've run the sample data generator:

```bash
python data/scripts/generate_sample_data.py

# Or with Docker:
docker-compose exec backend python /app/../data/scripts/generate_sample_data.py
```

### Port Already in Use

If ports 3000, 8000, or 5432 are already in use:

```bash
# Stop Docker services
docker-compose down

# Change ports in docker-compose.yml
# Then restart
docker-compose up -d
```

## Production Deployment

For production deployment:

1. Update environment variables in `.env`
2. Set strong `SECRET_KEY`
3. Configure proper database credentials
4. Use production-grade web server (Gunicorn + Nginx)
5. Enable HTTPS
6. Set up monitoring and logging
7. Configure backups

## Data Sources

The prototype uses simulated data based on realistic patterns. For production use, integrate with:

- **AirROI Data Portal**: https://www.airroi.com/data-portal/
- City tourism APIs
- Hotel booking platforms (Booking.com, Airbnb)
- Event ticketing systems
- Airport/transportation data
- Economic statistics databases

## Next Steps

1. **Expand Data Coverage**: Add more cities and events
2. **Real Data Integration**: Connect to AirROI and other APIs
3. **Advanced ML**: Implement predictive models
4. **Enhanced Visualizations**: Add interactive charts and maps
5. **User Authentication**: Add login and role-based access
6. **Reporting**: Generate PDF/Excel reports
7. **Mobile App**: Create mobile companion app

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/aperlon/Evently
- Documentation: See `/docs` folder

## License

MIT License - see LICENSE file for details
