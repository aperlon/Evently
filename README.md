# Evently - Event Impact Analyzer

> **🚀 Quick Start:** `./start.sh` - Ve a [QUICKSTART.md](QUICKSTART.md) para instrucciones en español

## 🎯 Descripción del Proyecto

**Evently** es un prototipo interactivo que permite analizar el impacto económico y turístico de grandes eventos urbanos (deporte, cultura, música, ferias internacionales) en distintas ciudades del mundo.

## 📊 Estado de los Datos

**Versión Actual: Datos Sintéticos Realistas**

Esta versión usa datos **simulados** basados en patrones reales porque:
- ✅ Prototipo funcional completo para demostración
- ✅ Datos realistas con patrones estacionales y de eventos
- ✅ Cobertura completa: 6 ciudades × 365 días × 4 tipos de métricas
- ⚠️ No requiere API keys ni suscripciones (ideal para testing)

**Para Producción: Integración con Datos Reales**

El sistema está **preparado para integrar fuentes reales**:
- 🌐 AIRROI Data Portal (configuración lista en `backend/.env`)
- 🇪🇺 Eurostat (script de importación incluido)
- 🌍 World Bank (API implementation disponible)
- 📱 Google Mobility (descarga automática)

Ver [data/scripts/import_real_data.py](data/scripts/import_real_data.py) para integrar datos reales.

## 🌍 Alcance

La solución analiza cómo eventos masivos influyen en:

- 📊 **Turismo**: Flujos de visitantes internacionales y locales
- 🏨 **Demanda hotelera**: Tasas de ocupación y disponibilidad
- 💰 **Precios de alojamiento**: Fluctuaciones antes/durante/después del evento
- 💵 **Gasto estimado**: Impacto económico por visitante
- 🏪 **Actividad económica local**: Comercio, restauración, servicios
- ✈️ **Movilidad y llegadas**: Tráfico aéreo y terrestre

## 🏙️ Ciudades y Eventos Analizados

| Ciudad | Eventos Principales |
|--------|---------------------|
| **Londres** | Maratón, Wimbledon, NFL London, conciertos masivos |
| **Tokio** | Maratón, grandes ferias, eventos culturales |
| **París** | Roland Garros, Fashion Week, conciertos |
| **Nueva York** | NYC Marathon, US Open, eventos musicales |
| **Madrid** | Champions League, conciertos, ferias, festivales |
| **Berlín/Chicago** | Maratones, festivales musicales |

## 👥 Usuarios Objetivo

- 🏛️ Ayuntamientos y gobiernos locales
- 🎪 Organizadores de eventos
- 🏨 Cadenas hoteleras y alojamientos
- 📈 Consultores urbanos y económicos
- 🎓 Investigadores y académicos

## ✨ Funcionalidades Principales

### 1. Visualización de Tendencias
- Series temporales de turismo, precios y ocupación
- Marcadores de eventos en líneas temporales
- Comparativas antes/durante/después del evento

### 2. Análisis Comparativo
- Comparar diferentes ciudades
- Comparar diferentes tipos de eventos
- Análisis multi-año y estacionalidad

### 3. Simulador "What-If"
- Escenarios de crecimiento del evento
- Proyecciones de impacto económico
- Sensibilidad de variables clave

### 4. KPIs y Métricas
- Impacto económico total
- ROI para organizadores
- Beneficio turístico neto
- Índice de saturación hotelera

## 🏗️ Arquitectura del Sistema

```
Evently/
├── backend/                 # API REST + Analytics Engine
│   ├── app/
│   │   ├── api/            # Endpoints FastAPI
│   │   ├── models/         # SQLAlchemy models
│   │   ├── services/       # Lógica de negocio
│   │   ├── analytics/      # Motor de análisis
│   │   └── etl/            # Procesos ETL
│   ├── tests/
│   └── requirements.txt
│
├── frontend/               # React Dashboard
│   ├── src/
│   │   ├── components/    # Componentes reutilizables
│   │   ├── pages/         # Páginas principales
│   │   ├── services/      # API client
│   │   └── utils/         # Utilidades
│   ├── public/
│   └── package.json
│
├── data/                   # Datos y scripts ETL
│   ├── raw/               # Datos crudos
│   ├── processed/         # Datos procesados
│   ├── schemas/           # Esquemas de BD
│   └── scripts/           # Scripts de procesamiento
│
├── notebooks/             # Jupyter notebooks (análisis exploratorio)
│
├── docker-compose.yml     # Orquestación de servicios
└── docs/                  # Documentación técnica
```

## 🚀 Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para PostgreSQL
- **Pandas**: Procesamiento y análisis de datos
- **NumPy**: Computación numérica
- **Scikit-learn**: Modelos predictivos
- **Pydantic**: Validación de datos

### Frontend
- **React 18**: Framework UI
- **TypeScript**: Tipado estático
- **Recharts**: Visualizaciones interactivas
- **TailwindCSS**: Estilos modernos
- **React Query**: Gestión de estado y cache
- **Axios**: Cliente HTTP

### Base de Datos
- **PostgreSQL 15**: Base de datos relacional
- **TimescaleDB** (opcional): Extensión para series temporales

### DevOps
- **Docker**: Contenedorización
- **Docker Compose**: Orquestación local
- **Nginx**: Reverse proxy (producción)

## 📦 Instalación y Uso

### 🚀 Tres Formas de Ejecutar (¡elige la que prefieras!)

**1️⃣ Script Automático (Lo más fácil):**
```bash
cd Evently

# Con Docker (setup automático)
./start.sh

# SIN Docker (más rápido para desarrollo)
./dev.sh
```

**2️⃣ Docker Compose (Para producción):**
```bash
docker-compose up -d
docker-compose exec backend python /app/../data/scripts/generate_sample_data.py
```

**3️⃣ Manual - Solo 2 Terminales (Para desarrollo activo):**
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # Crear con: python3 -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

### 📖 Guías Detalladas

- **[QUICKSTART.md](QUICKSTART.md)** - Inicio en 5 minutos (español)
- **[SIN_DOCKER.md](SIN_DOCKER.md)** - Desarrollo sin Docker (¡MÁS RÁPIDO!)
- **[SETUP.md](SETUP.md)** - Documentación completa

### Prerequisitos

| Con Docker | Sin Docker |
|------------|------------|
| Docker y Docker Compose | Python 3.11+ |
| | Node.js 18+ |
| | PostgreSQL 15 |

### URLs de Acceso

- 🌐 **Frontend**: http://localhost:3000
- 📡 **API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/api/v1/docs

## 📊 Fuentes de Datos

- **AirROI Data Portal**: https://www.airroi.com/data-portal/
- APIs de turismo oficiales
- Datos abiertos de ciudades
- Plataformas hoteleras (Booking, Airbnb)
- Estadísticas de eventos

## 🔬 Metodología

### Design Thinking
1. **Empatizar**: Entrevistas con stakeholders
2. **Definir**: Problemas y necesidades clave
3. **Idear**: Soluciones y funcionalidades
4. **Prototipar**: MVP con datos reales
5. **Testear**: Validación con usuarios finales

### Proceso ETL
1. **Extract**: Recopilación de datos de múltiples fuentes
2. **Transform**: Limpieza, normalización y enriquecimiento
3. **Load**: Carga en base de datos estructurada

### Analytics
- Análisis de series temporales
- Detección de anomalías
- Modelos de regresión para predicciones
- Clustering de patrones de eventos

## 📈 Roadmap

### Fase 1: MVP ✅ COMPLETADO
- [x] Arquitectura base
- [x] Modelos de datos (City, Event, Metrics, Impact)
- [x] ETL básico (generador de datos)
- [x] API REST (15+ endpoints)
- [x] Dashboard básico (React + TypeScript)
- [x] 6 ciudades + 12 eventos
- [x] Analytics engine (impact analyzer)
- [x] Simulador what-if
- [x] Deployment guides (Vercel, Railway, Supabase)

### Fase 2: Expansion
- [ ] Integración con datos reales (AIRROI, Eurostat, World Bank)
- [ ] ML para predicciones
- [ ] Visualizaciones avanzadas (charts, maps)
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Multi-idioma

### Fase 3: Producción
- [ ] Autenticación y roles
- [ ] SaaS multi-tenant
- [ ] Mobile app
- [ ] Real-time data
- [ ] Marketplace de datos

## 🌐 Deployment en Producción

**¿Listo para llevar a producción?** Lee **[DEPLOYMENT.md](DEPLOYMENT.md)**

**Stack recomendado (GRATIS):**
- 🎨 **Frontend**: Vercel (deploy en 2 min)
- ⚙️ **Backend**: Railway ($5 crédito gratis)
- 🗄️ **Database**: Supabase (PostgreSQL gratis)

```bash
# Deploy rápido:
# 1. Frontend → vercel.com (importar repo)
# 2. Database → supabase.com (crear proyecto)
# 3. Backend → railway.app (importar repo)
# ¡Listo en 10 minutos!
```

## 🤝 Contribución

Este es un proyecto de investigación y desarrollo. Las contribuciones son bienvenidas.

## 📄 Licencia

MIT License - ver archivo LICENSE para detalles

## 📧 Contacto

Para consultas y colaboraciones: [contacto@evently-project.com]

---

**Construido con ❤️ para ayuntamientos, organizadores y consultores urbanos**
