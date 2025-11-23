#!/bin/bash

# Evently - Quick Start Script
# This script helps you get the application running quickly

set -e

echo "========================================="
echo "  EVENTLY - Event Impact Analyzer"
echo "  Quick Start Script"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "   Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "   Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker is installed"
echo "✓ Docker Compose is installed"
echo ""

# Check if services are already running
if docker-compose ps | grep -q "Up"; then
    echo "⚠️  Services are already running"
    echo ""
    read -p "Do you want to restart them? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Stopping services..."
        docker-compose down
    else
        echo "Exiting..."
        exit 0
    fi
fi

# Start services
echo "🚀 Starting services..."
echo ""
docker-compose up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if services are healthy
echo ""
echo "🔍 Checking service health..."

if docker-compose ps | grep -q "evently-db.*Up"; then
    echo "  ✓ Database is running"
else
    echo "  ❌ Database failed to start"
    docker-compose logs db
    exit 1
fi

if docker-compose ps | grep -q "evently-backend.*Up"; then
    echo "  ✓ Backend API is running"
else
    echo "  ❌ Backend failed to start"
    docker-compose logs backend
    exit 1
fi

if docker-compose ps | grep -q "evently-frontend.*Up"; then
    echo "  ✓ Frontend is running"
else
    echo "  ❌ Frontend failed to start"
    docker-compose logs frontend
    exit 1
fi

# Wait a bit more for backend to be fully ready
echo ""
echo "⏳ Waiting for backend to be fully ready..."
sleep 10

# Check if data exists
echo ""
echo "🔍 Checking if sample data exists..."

if docker-compose exec -T backend python -c "from app.core.database import SessionLocal; from app.models import City; db = SessionLocal(); print(db.query(City).count())" 2>/dev/null | grep -q "6"; then
    echo "  ✓ Sample data already exists"
else
    echo "  📊 Loading data from historical CSVs..."
    # First, ensure CSVs exist
    if docker-compose exec -T backend test -f /data/examples/cities.csv; then
        echo "  ✓ CSV files found, loading into database..."
        docker-compose exec backend python /data/scripts/load_from_csvs.py
    else
        echo "  ⚠️  CSV files not found, generating them first..."
        docker-compose exec backend python /data/scripts/generate_historical_csvs.py
        docker-compose exec backend python /data/scripts/load_from_csvs.py
    fi
fi

# Test API
echo ""
echo "🧪 Testing API..."
sleep 2

if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "  ✓ API is responding"
else
    echo "  ⚠️  API might not be ready yet (this is normal on first start)"
fi

# Success message
echo ""
echo "========================================="
echo "  ✅ EVENTLY IS READY!"
echo "========================================="
echo ""
echo "Access the application:"
echo "  🌐 Frontend:  http://localhost:3000"
echo "  📡 API:       http://localhost:8000"
echo "  📚 API Docs:  http://localhost:8000/api/v1/docs"
echo ""
echo "View logs:"
echo "  docker-compose logs -f"
echo ""
echo "Stop the application:"
echo "  docker-compose down"
echo ""
echo "========================================="
