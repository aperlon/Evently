#!/bin/bash

# Evently - Development Mode (Sin Docker)
# Este script inicia todo en modo desarrollo

set -e

echo "========================================="
echo "  EVENTLY - Modo Desarrollo"
echo "========================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "   Instálalo desde: https://www.python.org/downloads/"
    exit 1
fi

# Verificar Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado"
    echo "   Instálalo desde: https://nodejs.org/"
    exit 1
fi

# Verificar PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL no está instalado"
    echo ""
    echo "Opciones:"
    echo "  1. Instalar PostgreSQL localmente"
    echo "  2. O usar Docker solo para la base de datos:"
    echo "     docker run -d -p 5432:5432 -e POSTGRES_USER=evently -e POSTGRES_PASSWORD=evently123 -e POSTGRES_DB=evently postgres:15-alpine"
    echo ""
    read -p "¿Continuar de todos modos? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✓ Python: $(python3 --version)"
echo "✓ Node: $(node --version)"
echo ""

# ============================================
# BACKEND
# ============================================
echo "📦 Configurando Backend..."

cd backend

# Crear venv si no existe
if [ ! -d "venv" ]; then
    echo "   Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar venv
source venv/bin/activate

# Instalar dependencias si es necesario
if [ ! -f "venv/.installed" ]; then
    echo "   Instalando dependencias de Python..."
    pip install -q -r requirements.txt
    touch venv/.installed
fi

# Configurar .env si no existe
if [ ! -f ".env" ]; then
    echo "   Creando archivo .env..."
    cp .env.example .env
fi

cd ..

# ============================================
# GENERAR DATOS (si no existen)
# ============================================
echo ""
echo "📊 Verificando datos de muestra..."

cd backend
source venv/bin/activate

# Verificar si hay datos
HAS_DATA=$(python3 -c "
try:
    from app.core.database import SessionLocal
    from app.models import City
    db = SessionLocal()
    count = db.query(City).count()
    db.close()
    print(count)
except:
    print(0)
" 2>/dev/null || echo "0")

cd ..

if [ "$HAS_DATA" = "6" ]; then
    echo "   ✓ Datos ya existen"
else
    echo "   Cargando datos desde CSVs históricos..."
    # Verificar si existen los CSVs
    if [ -f "data/examples/cities.csv" ]; then
        echo "   ✓ CSVs encontrados, cargando en base de datos..."
        cd backend
        source venv/bin/activate
        python ../data/scripts/load_from_csvs.py
        cd ..
    else
        echo "   ⚠️  CSVs no encontrados, generándolos primero..."
        cd backend
        source venv/bin/activate
        python ../data/scripts/generate_historical_csvs.py
        python ../data/scripts/load_from_csvs.py
        cd ..
    fi
fi

# ============================================
# FRONTEND
# ============================================
echo ""
echo "📦 Configurando Frontend..."

cd frontend

# Instalar dependencias si es necesario
if [ ! -d "node_modules" ]; then
    echo "   Instalando dependencias de Node.js..."
    npm install
fi

# Configurar .env si no existe
if [ ! -f ".env" ]; then
    echo "   Creando archivo .env..."
    cp .env.example .env
fi

cd ..

# ============================================
# INICIAR SERVICIOS
# ============================================
echo ""
echo "========================================="
echo "  🚀 Iniciando servicios..."
echo "========================================="
echo ""

# Función para matar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup INT TERM

# Iniciar Backend
echo "🔧 Iniciando Backend API..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

sleep 3

# Verificar que el backend esté corriendo
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend falló al iniciar"
    echo "   Ver logs: tail -f backend.log"
    exit 1
fi

echo "   ✓ Backend corriendo (PID: $BACKEND_PID)"

# Iniciar Frontend
echo "🎨 Iniciando Frontend..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

sleep 3

# Verificar que el frontend esté corriendo
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo "❌ Frontend falló al iniciar"
    echo "   Ver logs: tail -f frontend.log"
    kill $BACKEND_PID
    exit 1
fi

echo "   ✓ Frontend corriendo (PID: $FRONTEND_PID)"

# ============================================
# LISTO!
# ============================================
echo ""
echo "========================================="
echo "  ✅ ¡TODO LISTO!"
echo "========================================="
echo ""
echo "🌐 Accede a la aplicación:"
echo "   Frontend:  http://localhost:3000"
echo "   API:       http://localhost:8000"
echo "   API Docs:  http://localhost:8000/api/v1/docs"
echo ""
echo "📋 Logs en tiempo real:"
echo "   Backend:   tail -f backend.log"
echo "   Frontend:  tail -f frontend.log"
echo ""
echo "🛑 Para detener: Ctrl+C"
echo "========================================="
echo ""

# Esperar
wait
