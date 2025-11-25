# Evently - Analizador de Impacto de Eventos

## 📌 ¿Qué es Evently?

**Evently** es una plataforma web interactiva que analiza el impacto económico y turístico de grandes eventos (deportivos, culturales, musicales, ferias) en ciudades de todo el mundo.

Cuenta con un **globo 3D interactivo** que muestra 16 ciudades globales, visualizaciones de datos en tiempo real, y simuladores para proyectar el impacto económico de eventos futuros.

## 🎯 Características principales

- **Globo 3D Interactivo**: Visualización del planeta con pins en 16 ciudades
- **Dashboard Analítico**: Gráficos y métricas de turismo, ocupación hotelera y precios
- **Análisis Comparativo**: Compara el impacto entre diferentes ciudades y eventos
- **Simulador What-If**: Proyecciones de impacto económico con diferentes escenarios
- **Casos de Estudio**: Rio Carnival, Paris Fashion Week, Tokyo Game Show

## 🛠️ Tecnologías

### Frontend
- **React 18** + **TypeScript** + **Vite**
- **TailwindCSS** (estilos modernos)
- **React Globe GL** + **Three.js** (globo 3D)
- **Recharts** (gráficos interactivos)
- **Framer Motion** (animaciones)
- **React Router** (navegación)

### Backend
- **FastAPI** (API REST)
- **PostgreSQL** (base de datos)
- **SQLAlchemy** (ORM)
- **Pandas** + **NumPy** (análisis de datos)
- **Scikit-learn** (modelos predictivos)

## 📦 Instalación y Ejecución

### Prerequisitos

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 15**

### Opción 1: Ejecución rápida con scripts automáticos

```bash
cd Evently

# Con Docker (setup automático completo)
./start.sh

# Sin Docker (más rápido, para desarrollo)
./dev.sh
```

### Opción 2: Ejecución manual (2 terminales)

#### Terminal 1: Backend

```bash
cd backend

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos (crear archivo .env con tu configuración)
# DATABASE_URL=postgresql://usuario:password@localhost:5432/evently

# Ejecutar servidor
uvicorn app.main:app --reload
```

#### Terminal 2: Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

### Opción 3: Con Docker Compose

```bash
docker-compose up -d
docker-compose exec backend python /data/scripts/generate_sample_data.py
```

## 🌐 URLs de Acceso

Una vez ejecutado el proyecto, accede a:

- **Frontend (Aplicación Web)**: http://localhost:3000
- **Backend (API)**: http://localhost:8000
- **Documentación API**: http://localhost:8000/api/v1/docs

## 📊 Datos

El proyecto incluye un generador de datos sintéticos realistas. Al ejecutar por primera vez, se generarán automáticamente:

- 16 ciudades globales en 5 continentes
- 48+ eventos históricos (2022-2024)
- Métricas diarias de turismo, ocupación hotelera y precios
- Análisis de impacto económico

Para cargar datos reales, puedes subir archivos CSV/XLSX desde la aplicación o usar las APIs de fuentes externas (AIRROI, Eurostat, World Bank).

## 🏗️ Estructura del Proyecto

```
Evently/
├── backend/                # API REST + Motor de análisis
│   ├── app/
│   │   ├── api/           # Endpoints FastAPI
│   │   ├── models/        # Modelos de base de datos
│   │   ├── services/      # Lógica de negocio
│   │   └── analytics/     # Motor de análisis de impacto
│   └── requirements.txt
│
├── frontend/              # Dashboard React
│   ├── src/
│   │   ├── components/   # Componentes reutilizables
│   │   ├── pages/        # Páginas principales
│   │   └── services/     # Cliente API
│   └── package.json
│
├── data/                  # Datos y scripts
│   ├── scripts/          # Generadores y ETL
│   └── examples/         # Ejemplos de CSV
│
└── docker-compose.yml     # Orquestación de servicios
```

## 🚀 Despliegue en Producción

El proyecto está optimizado para desplegarse en servicios cloud gratuitos:

- **Frontend**: Vercel
- **Backend**: Railway
- **Base de datos**: Supabase (PostgreSQL)

## 📧 Contacto

Para preguntas sobre el proyecto: contacto@evently-project.com

---

**Desarrollado con React, FastAPI y PostgreSQL** 🚀
