# Evently - Event Impact Analyzer

> **🚀 Quick Start:** `./start.sh` - Ve a [QUICKSTART.md](QUICKSTART.md) para instrucciones en español

## 🎯 Descripción del Proyecto

**Evently** es un prototipo interactivo que permite analizar el impacto económico y turístico de grandes eventos urbanos (deporte, cultura, música, ferias internacionales) en distintas ciudades del mundo.

## 📊 Estado de los Datos

**Versión Actual: Datos Sintéticos Realistas**

Esta versión usa datos **simulados** basados en patrones reales porque:
- ✅ Prototipo funcional completo para demostración
- ✅ Datos realistas con patrones estacionales y de eventos
- ✅ Cobertura completa: **16 ciudades** × 365 días × 4 tipos de métricas
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

## 🌍 16 Ciudades Globales Analizadas

### Europa 🇪🇺
| Ciudad | País | Eventos Principales |
|--------|------|---------------------|
| **Londres** 🇬🇧 | Reino Unido | Wimbledon, Maratón, NFL London, conciertos masivos |
| **París** 🇫🇷 | Francia | Roland Garros, Fashion Week, Maratón |
| **Madrid** 🇪🇸 | España | Champions League, ferias, festivales |
| **Berlín** 🇩🇪 | Alemania | Maratón, festivales musicales, ferias tech |
| **Barcelona** 🇪🇸 | España | Mobile World Congress, Smart City Expo |
| **Amsterdam** 🇳🇱 | Países Bajos | Amsterdam Dance Event, festivales culturales |

### América 🌎
| Ciudad | País | Eventos Principales |
|--------|------|---------------------|
| **Nueva York** 🇺🇸 | Estados Unidos | NYC Marathon, US Open, eventos musicales |
| **Los Angeles** 🇺🇸 | Estados Unidos | Oscars, Grammy, Super Bowl, festivales |
| **Chicago** 🇺🇸 | Estados Unidos | Lollapalooza, Maratón, festivales de jazz |
| **Miami** 🇺🇸 | Estados Unidos | Art Basel, Ultra Music Festival, Miami Open |
| **Rio de Janeiro** 🇧🇷 | Brasil | Carnaval, Rock in Rio, eventos deportivos |
| **São Paulo** 🇧🇷 | Brasil | Formula 1, São Paulo Fashion Week, Lollapalooza |

### Asia-Pacífico 🌏
| Ciudad | País | Eventos Principales |
|--------|------|---------------------|
| **Tokio** 🇯🇵 | Japón | Tokyo Game Show, Maratón, eventos culturales |
| **Singapur** 🇸🇬 | Singapur | Formula 1, festivales gastronómicos, tech summits |
| **Dubai** 🇦🇪 | Emiratos Árabes | Dubai Expo, World Cup events, festivales |
| **Sydney** 🇦🇺 | Australia | Sydney Festival, Mardi Gras, eventos deportivos |

**Total: 16 ciudades en 5 continentes** 🌍🌎🌏🌍🌏

## 👥 Usuarios Objetivo

- 🏛️ Ayuntamientos y gobiernos locales
- 🎪 Organizadores de eventos
- 🏨 Cadenas hoteleras y alojamientos
- 📈 Consultores urbanos y económicos
- 🎓 Investigadores y académicos

## ✨ Funcionalidades Principales

### 🌍 1. Globo 3D Interactivo (Landing Page)
- Visualización 3D del planeta Tierra con rotación automática
- 16 pins rojos interactivos sobre ciudades analizadas
- Click en cada ciudad para ver información detallada
- Stats impactantes: $12.4B impacto analizado, 847K empleos creados, 420% ROI promedio
- Tecnología: `react-globe.gl` + `three.js`

### 📊 2. Dashboard Analítico
- Series temporales de turismo, precios y ocupación
- Marcadores de eventos en líneas temporales
- Comparativas antes/durante/después del evento
- KPIs principales: impacto económico, ROI, empleos creados

### 🔍 3. Análisis Comparativo
- Comparar diferentes ciudades lado a lado
- Comparar diferentes tipos de eventos
- Análisis multi-año y detección de estacionalidad
- Gráficos interactivos con Recharts

### 🔮 4. Simulador "What-If"
- Escenarios de crecimiento del evento
- Proyecciones de impacto económico
- Sensibilidad de variables clave (asistencia, precios, duración)
- Simulaciones multi-año

### 📄 5. About Us / Sobre Nosotros
- Misión y visión del proyecto
- Propuesta de valor clara
- Público objetivo: gobiernos, organizadores, hoteles, consultoras
- Stats de impacto con animaciones

### 🧪 6. Metodología
- Proceso Design Thinking (5 fases)
- Pipeline ETL visualizado (Extract → Transform → Load)
- Motor de análisis de impacto explicado
- Cálculo de métricas paso a paso

### 📚 7. Case Studies / Casos de Éxito
- **Rio Carnival 2024**: $1.2B impacto, 47K empleos, 520% ROI
- **Paris Fashion Week 2024**: $685M impacto, 12.5K empleos, 380% ROI
- **Tokyo Game Show 2024**: $428M impacto, 8.9K empleos, 340% ROI
- Breakdown económico detallado por evento
- Timeline de impacto (antes, durante, después)

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
- **Vite**: Build tool ultrarrápido
- **React Router**: Navegación y routing
- **React Query**: Gestión de estado y cache
- **Recharts**: Visualizaciones de datos interactivas
- **react-globe.gl**: Globo 3D interactivo
- **Three.js**: Renderizado 3D WebGL
- **Framer Motion**: Animaciones fluidas y profesionales
- **Lucide React**: 110+ iconos SVG de alta calidad
- **TailwindCSS**: Estilos modernos y responsivos
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

### **Importación de Datos**

**Tres formas de cargar datos:**

1. **📁 Upload de Archivos CSV/XLSX** (Recomendado - MÁS FÁCIL)
   ```bash
   # Sube tus propios datos desde Excel o CSV
   POST /api/v1/upload/cities
   POST /api/v1/upload/events
   POST /api/v1/upload/hotel-metrics
   POST /api/v1/upload/tourism-metrics
   ```
   ✅ No requiere API keys
   ✅ Funciona offline
   ✅ Importa miles de registros en segundos

   📖 **Guía completa:** [docs/FILE_UPLOADS.md](docs/FILE_UPLOADS.md)

   📥 **Ejemplos:** Ver `data/examples/` para CSV de ejemplo

2. **🌐 APIs Externas**
   - **AirROI Data Portal**: https://www.airroi.com/data-portal/
   - **Eurostat** (turismo europeo)
   - **World Bank** (estadísticas globales)
   - **Google Mobility** (movilidad urbana)

   Ver [data/scripts/import_real_data.py](data/scripts/import_real_data.py)

3. **🔧 Datos Sintéticos** (para testing)
   ```bash
   python data/scripts/generate_sample_data.py
   ```

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
- [x] Arquitectura base (FastAPI + React + PostgreSQL)
- [x] Modelos de datos (City, Event, Metrics, Impact)
- [x] ETL básico (generador de datos sintéticos)
- [x] API REST (20+ endpoints)
- [x] **16 ciudades globales** en 5 continentes
- [x] **Globo 3D interactivo** con pins clickables
- [x] Dashboard completo con visualizaciones
- [x] Analytics engine (impact analyzer con baseline vs event)
- [x] Simulador what-if (scenarios y predicciones)
- [x] **Upload de CSV/XLSX** para importar datos
- [x] **About Us page** (misión, visión, público objetivo)
- [x] **Methodology page** (Design Thinking + ETL pipeline)
- [x] **Case Studies page** (3 casos con datos detallados)
- [x] **Footer profesional** con navegación completa
- [x] **Animaciones con Framer Motion**
- [x] Deployment guides (Vercel, Railway, Supabase)
- [x] Modo desarrollo sin Docker (más rápido)

### Fase 2: Expansion 🚧 EN PROGRESO
- [ ] Integración con datos reales (AIRROI, Eurostat, World Bank)
- [ ] ML para predicciones avanzadas (ARIMA, Prophet)
- [ ] Mapas de calor interactivos
- [ ] Exportación de reportes (PDF/Excel con branding)
- [ ] Multi-idioma (ES/EN)
- [ ] Dark mode toggle
- [ ] Tour guiado para nuevos usuarios
- [ ] Más ciudades (expandir a 30+ ciudades)
- [ ] API pública con documentación Swagger

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
