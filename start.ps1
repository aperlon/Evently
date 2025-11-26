# Evently - Quick Start Script para Windows PowerShell
# Este script ayuda a iniciar la aplicación rápidamente

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  EVENTLY - Event Impact Analyzer" -ForegroundColor Cyan
Write-Host "  Quick Start Script (Windows)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker no está instalado" -ForegroundColor Red
    Write-Host "   Por favor instala Docker Desktop desde: https://docs.docker.com/get-docker/" -ForegroundColor Yellow
    exit 1
}

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose no está instalado" -ForegroundColor Red
    Write-Host "   Por favor instala Docker Desktop desde: https://docs.docker.com/compose/install/" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Docker está instalado" -ForegroundColor Green
Write-Host "✓ Docker Compose está instalado" -ForegroundColor Green
Write-Host ""

# Verificar si Docker Desktop está corriendo
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker Desktop no está corriendo" -ForegroundColor Red
    Write-Host "   Por favor inicia Docker Desktop y espera a que esté listo" -ForegroundColor Yellow
    exit 1
}

# Verificar si los servicios ya están corriendo
$running = docker-compose ps 2>$null | Select-String "Up"
if ($running) {
    Write-Host "⚠️  Los servicios ya están corriendo" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "¿Quieres reiniciarlos? (s/n)"
    if ($response -eq "s" -or $response -eq "S") {
        Write-Host "Deteniendo servicios..." -ForegroundColor Yellow
        docker-compose down
    } else {
        Write-Host "Saliendo..." -ForegroundColor Yellow
        exit 0
    }
}

# Iniciar servicios
Write-Host "🚀 Iniciando servicios..." -ForegroundColor Cyan
Write-Host ""
docker-compose up -d

# Esperar a que los servicios estén listos
Write-Host ""
Write-Host "⏳ Esperando a que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar salud de los servicios
Write-Host ""
Write-Host "🔍 Verificando salud de los servicios..." -ForegroundColor Cyan

$dbStatus = docker-compose ps db 2>$null | Select-String "Up"
if ($dbStatus) {
    Write-Host "  ✓ Base de datos está corriendo" -ForegroundColor Green
} else {
    Write-Host "  ❌ Base de datos falló al iniciar" -ForegroundColor Red
    docker-compose logs db
    exit 1
}

$backendStatus = docker-compose ps backend 2>$null | Select-String "Up"
if ($backendStatus) {
    Write-Host "  ✓ Backend API está corriendo" -ForegroundColor Green
} else {
    Write-Host "  ❌ Backend falló al iniciar" -ForegroundColor Red
    docker-compose logs backend
    exit 1
}

$frontendStatus = docker-compose ps frontend 2>$null | Select-String "Up"
if ($frontendStatus) {
    Write-Host "  ✓ Frontend está corriendo" -ForegroundColor Green
} else {
    Write-Host "  ❌ Frontend falló al iniciar" -ForegroundColor Red
    docker-compose logs frontend
    exit 1
}

# Esperar un poco más para que el backend esté completamente listo
Write-Host ""
Write-Host "⏳ Esperando a que el backend esté completamente listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar si hay datos
Write-Host ""
Write-Host "🔍 Verificando si existen datos de muestra..." -ForegroundColor Cyan

try {
    $cityCount = docker-compose exec -T backend python -c "from app.core.database import SessionLocal; from app.models import City; db = SessionLocal(); print(db.query(City).count())" 2>$null
    if ($cityCount -and [int]$cityCount -ge 6) {
        Write-Host "  ✓ Datos de muestra ya existen" -ForegroundColor Green
    } else {
        Write-Host "  📊 Cargando datos desde CSVs históricos..." -ForegroundColor Yellow
        $csvExists = docker-compose exec -T backend Test-Path /data/examples/cities.csv 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Archivos CSV encontrados, cargando en base de datos..." -ForegroundColor Green
            docker-compose exec backend python /data/scripts/load_from_csvs.py
        } else {
            Write-Host "  ⚠️  Archivos CSV no encontrados, generándolos primero..." -ForegroundColor Yellow
            docker-compose exec backend python /data/scripts/generate_historical_csvs.py
            docker-compose exec backend python /data/scripts/load_from_csvs.py
        }
    }
} catch {
    Write-Host "  ⚠️  No se pudieron verificar los datos (esto es normal en el primer inicio)" -ForegroundColor Yellow
}

# Probar API
Write-Host ""
Write-Host "🧪 Probando API..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    if ($response.Content -match "healthy") {
        Write-Host "  ✓ API está respondiendo" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️  API podría no estar lista aún (esto es normal en el primer inicio)" -ForegroundColor Yellow
}

# Mensaje de éxito
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  ✅ ¡EVENTLY ESTÁ LISTO!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Accede a la aplicación:" -ForegroundColor Cyan
Write-Host "  🌐 Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "  📡 API:       http://localhost:8000" -ForegroundColor White
Write-Host "  📚 API Docs:  http://localhost:8000/api/v1/docs" -ForegroundColor White
Write-Host ""
Write-Host "Ver logs:" -ForegroundColor Cyan
Write-Host "  docker-compose logs -f" -ForegroundColor White
Write-Host ""
Write-Host "Detener la aplicación:" -ForegroundColor Cyan
Write-Host "  docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green

