#!/bin/bash
# =============================================================================
# Evently MVP - UNESCO Pipeline
# Complete automation: Download → Import → Train → Test
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "============================================================================"
echo "   ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗  ██╗   ██╗"
echo "  ██╔════╝ ██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║  ╚██╗ ██╔╝"
echo "  █████╗   ██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ╚████╔╝ "
echo "  ██╔══╝   ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║    ╚██╔╝  "
echo "  ███████╗  ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████╗██║   "
echo "  ╚══════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝   "
echo ""
echo "  MVP Pipeline - UNESCO Event Impact Analyzer with ML"
echo "============================================================================"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "MVP_UNESCO_README.md" ]; then
    echo -e "${RED}❌ Error: Must be run from Evently root directory${NC}"
    exit 1
fi

# Function to print step headers
print_step() {
    echo ""
    echo -e "${BLUE}============================================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================================================${NC}"
    echo ""
}

# Function to check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# =============================================================================
# STEP 0: Prerequisites Check
# =============================================================================

print_step "STEP 0: Checking Prerequisites"

echo -n "  Checking Python 3... "
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi

echo -n "  Checking PostgreSQL... "
if command_exists psql; then
    PSQL_VERSION=$(psql --version | awk '{print $3}')
    echo -e "${GREEN}✓ Found PostgreSQL $PSQL_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ PostgreSQL not found (may be ok if using Docker)${NC}"
fi

echo -n "  Checking virtual environment... "
if [ -d "backend/venv" ]; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${YELLOW}⚠ Not found, creating...${NC}"
    cd backend
    python3 -m venv venv
    cd ..
    echo -e "${GREEN}✓ Created${NC}"
fi

echo -n "  Activating virtual environment... "
source backend/venv/bin/activate
echo -e "${GREEN}✓ Activated${NC}"

# =============================================================================
# STEP 1: Install Dependencies
# =============================================================================

print_step "STEP 1: Installing Python Dependencies"

cd backend
echo "  Installing requirements.txt..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✓ All dependencies installed${NC}"
else
    echo -e "${RED}  ✗ Failed to install dependencies${NC}"
    exit 1
fi

# Check if Kaggle is installed
if pip show kaggle >/dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Kaggle API installed${NC}"
    if [ -f "$HOME/.kaggle/kaggle.json" ]; then
        echo -e "${GREEN}  ✓ Kaggle credentials found${NC}"
    else
        echo -e "${YELLOW}  ⚠ Kaggle credentials not found (manual download required)${NC}"
    fi
else
    echo -e "${YELLOW}  ⚠ Kaggle API not installed${NC}"
    echo "     To install: pip install kaggle"
    echo "     Credentials: https://www.kaggle.com/account → API → Create Token"
fi

cd ..

# =============================================================================
# STEP 2: Download Real Data
# =============================================================================

print_step "STEP 2: Downloading Real Data from Public Sources"

echo -e "${YELLOW}  This may take 5-10 minutes depending on your connection...${NC}"
echo ""

cd data/scripts
python3 download_real_data.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✓ Data download completed${NC}"
else
    echo -e "${YELLOW}  ⚠ Some downloads may have failed (check output above)${NC}"
    echo -e "${YELLOW}     You can download manually - see data/REAL_DATA_SOURCES.md${NC}"
fi

cd ../..

# =============================================================================
# STEP 3: Create Database
# =============================================================================

print_step "STEP 3: Setting Up Database"

# Check if database exists
DB_NAME="evently_unesco"
echo -n "  Checking database '$DB_NAME'... "

if psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME 2>/dev/null; then
    echo -e "${GREEN}✓ Exists${NC}"
    echo -n "  Drop and recreate? (y/N): "
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        dropdb $DB_NAME 2>/dev/null || true
        createdb $DB_NAME
        echo -e "${GREEN}  ✓ Database recreated${NC}"
    else
        echo "  Using existing database"
    fi
else
    echo -e "${YELLOW}Not found${NC}"
    echo "  Creating database..."
    createdb $DB_NAME || {
        echo -e "${YELLOW}  ⚠ Could not create database automatically${NC}"
        echo "     Please run manually: createdb $DB_NAME"
        echo "     Or use Docker: docker-compose up -d postgres"
    }
fi

# =============================================================================
# STEP 4: Import Data to Database
# =============================================================================

print_step "STEP 4: Importing Data to PostgreSQL"

cd data/scripts
python3 import_csv_to_db.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✓ Data import completed${NC}"
else
    echo -e "${RED}  ✗ Data import failed${NC}"
    echo "     Check database connection in backend/.env"
    exit 1
fi

cd ../..

# =============================================================================
# STEP 5: Train ML Models
# =============================================================================

print_step "STEP 5: Training Machine Learning Models"

cd data/scripts
python3 train_models.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✓ ML training completed${NC}"
else
    echo -e "${RED}  ✗ ML training failed${NC}"
    exit 1
fi

cd ../..

# =============================================================================
# STEP 6: Run Tests
# =============================================================================

print_step "STEP 6: Running Unit Tests"

cd backend
pytest tests/test_ml.py -v --tb=short

if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✓ All tests passed${NC}"
else
    echo -e "${YELLOW}  ⚠ Some tests failed (see output above)${NC}"
fi

cd ..

# =============================================================================
# STEP 7: Start Services (Optional)
# =============================================================================

print_step "STEP 7: Starting Services"

echo "  Would you like to start the backend API? (y/N): "
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo -e "${GREEN}  Starting backend API...${NC}"
    echo -e "${YELLOW}  Press Ctrl+C to stop${NC}"
    echo ""
    cd backend
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
    echo "  Skipping API start"
fi

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print_step "✅ PIPELINE COMPLETED!"

echo -e "${GREEN}Summary:${NC}"
echo "  ✓ Dependencies installed (Prophet, XGBoost, scikit-learn)"
echo "  ✓ Real data downloaded from multiple sources"
echo "  ✓ Data imported to PostgreSQL"
echo "  ✓ ML models trained and saved"
echo "  ✓ Tests executed"
echo ""
echo -e "${BLUE}📊 Trained Models:${NC}"
echo "  - TourismPredictor (Prophet/RandomForest)"
echo "  - HotelPricePredictor (RandomForest)"
echo "  - ImpactPredictor (Linear Regression)"
echo "  - Models saved to: backend/app/ml/saved_models/"
echo ""
echo -e "${BLUE}📁 Data Sources:${NC}"
echo "  - London Marathon: 2018-2023"
echo "  - Champions League: 1955-2023"
echo "  - World Bank: Tourism statistics"
echo "  - Eurostat: European tourism data"
echo "  - Google Mobility: Urban movement patterns"
echo ""
echo -e "${BLUE}🚀 Next Steps:${NC}"
echo "  1. Review model metrics in train_models.py output"
echo "  2. Start API: cd backend && uvicorn app.main:app --reload"
echo "  3. API Docs: http://localhost:8000/api/v1/docs"
echo "  4. Start Frontend: cd frontend && npm run dev"
echo "  5. Read: MVP_UNESCO_README.md for full documentation"
echo ""
echo -e "${BLUE}📖 Documentation:${NC}"
echo "  - MVP_UNESCO_README.md - Complete guide"
echo "  - data/REAL_DATA_SOURCES.md - Data sources reference"
echo "  - backend/tests/test_ml.py - Test suite"
echo ""
echo -e "${GREEN}🎉 Ready for UNESCO presentation!${NC}"
echo ""
