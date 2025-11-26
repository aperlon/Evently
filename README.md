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

---

## 📦 GUÍA DE INSTALACIÓN Y EJECUCIÓN

### ✅ Prerequisitos

Antes de comenzar, asegúrate de tener instalado:

1. **Python 3.11 o superior**
   - Descarga: https://www.python.org/downloads/
   - Verificar: `python --version` o `python3 --version`

2. **Node.js 18 o superior**
   - Descarga: https://nodejs.org/
   - Verificar: `node --version`

3. **PostgreSQL 15 o superior** (o usar Docker)
   - Descarga: https://www.postgresql.org/download/
   - Verificar: `psql --version`

4. **Git** (para clonar el repositorio)
   - Descarga: https://git-scm.com/downloads

**Opcional pero recomendado:**
- **Docker Desktop** (para ejecución simplificada)
  - Descarga: https://www.docker.com/products/docker-desktop/

---

## 🚀 OPCIÓN 1: Ejecución con Docker (MÁS FÁCIL - Recomendado)

Esta es la forma más sencilla de ejecutar el proyecto. Docker se encarga de todo automáticamente.

### Paso 1: Verificar Docker

Abre una terminal y verifica que Docker esté instalado:

```bash
docker --version
docker-compose --version
```

Si no tienes Docker, instálalo desde: https://www.docker.com/products/docker-desktop/

### Paso 2: Clonar el repositorio (si aún no lo tienes)

```bash
git clone <url-del-repositorio>
cd Evently
```

### Paso 3: Ejecutar el proyecto

**En Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**En Windows (PowerShell) - RECOMENDADO:**
```powershell
# Ejecutar el script automático
.\start.ps1
```

**En Windows (CMD o Git Bash):**
```bash
# Ejecutar directamente docker-compose
docker-compose up -d
```

**En Windows (WSL):**
```bash
./start.sh
```

### Paso 4: Esperar a que se inicien los servicios

El script automáticamente:
- ✅ Inicia PostgreSQL
- ✅ Inicia el backend (FastAPI)
- ✅ Inicia el frontend (React)
- ✅ Carga los datos de ejemplo

Esto puede tardar 2-5 minutos la primera vez.

### Paso 5: Acceder a la aplicación

Una vez que veas el mensaje "✅ EVENTLY IS READY!", abre tu navegador en:

- **🌐 Frontend (Aplicación Web)**: http://localhost:3000
- **📡 Backend (API)**: http://localhost:8000
- **📚 Documentación API**: http://localhost:8000/api/v1/docs

### Detener el proyecto

```bash
docker-compose down
```

---

## 🛠️ OPCIÓN 2: Ejecución Manual (Sin Docker)

Si prefieres ejecutar sin Docker, sigue estos pasos:

### Paso 1: Configurar Base de Datos PostgreSQL

**Opción A: PostgreSQL local**

1. Instala PostgreSQL desde: https://www.postgresql.org/download/
2. Crea una base de datos:
```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear base de datos y usuario
CREATE DATABASE evently;
CREATE USER evently WITH PASSWORD 'evently123';
GRANT ALL PRIVILEGES ON DATABASE evently TO evently;
\q
```

**Opción B: Docker solo para la base de datos**

```bash
docker run -d \
  --name evently-db \
  -e POSTGRES_USER=evently \
  -e POSTGRES_PASSWORD=evently123 \
  -e POSTGRES_DB=evently \
  -p 5432:5432 \
  postgres:15-alpine
```

### Paso 2: Configurar Backend

Abre una **Terminal 1** y ejecuta:

```bash
# Navegar a la carpeta del proyecto
cd Evently

# Ir a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Windows (CMD):
venv\Scripts\activate.bat
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env (si no existe)
# En Windows (PowerShell):
echo "DATABASE_URL=postgresql://evently:evently123@localhost:5432/evently" > .env
echo "SECRET_KEY=your-secret-key-change-in-production" >> .env
# En Linux/Mac:
cat > .env << EOF
DATABASE_URL=postgresql://evently:evently123@localhost:5432/evently
SECRET_KEY=your-secret-key-change-in-production
EOF

# Iniciar el servidor backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Deberías ver algo como:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**⚠️ IMPORTANTE:** Deja esta terminal abierta y corriendo.

### Paso 3: Cargar Datos en la Base de Datos

Abre una **Terminal 2** (nueva) y ejecuta:

```bash
cd Evently/backend

# Activar entorno virtual (igual que antes)
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Verificar si existen los CSVs de ejemplo
# Si existen, cargarlos:
python ../data/scripts/load_from_csvs.py

# Si no existen, generarlos primero:
python ../data/scripts/generate_historical_csvs.py
python ../data/scripts/load_from_csvs.py
```

### Paso 4: Configurar Frontend

Abre una **Terminal 3** (nueva) y ejecuta:

```bash
# Navegar a la carpeta del proyecto
cd Evently

# Ir a la carpeta frontend
cd frontend

# Instalar dependencias (solo la primera vez)
npm install

# Iniciar el servidor de desarrollo
npm run dev
```

Deberías ver algo como:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**⚠️ IMPORTANTE:** Deja esta terminal abierta y corriendo.

### Paso 5: Acceder a la aplicación

Abre tu navegador en:

- **🌐 Frontend (Aplicación Web)**: http://localhost:3000
- **📡 Backend (API)**: http://localhost:8000
- **📚 Documentación API**: http://localhost:8000/api/v1/docs

### Detener el proyecto

Presiona `Ctrl+C` en cada terminal para detener los servidores.

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "No se puede conectar a la base de datos"

**Solución:**
1. Verifica que PostgreSQL esté corriendo:
   ```bash
   # Windows
   Get-Service postgresql*
   
   # Linux/Mac
   sudo systemctl status postgresql
   ```

2. Verifica la conexión:
   ```bash
   psql -U evently -d evently -h localhost
   ```

3. Revisa el archivo `.env` en `backend/` y asegúrate de que `DATABASE_URL` sea correcto.

### Error: "puerto 8000 ya está en uso"

**Solución:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

O cambia el puerto en el comando uvicorn:
```bash
uvicorn app.main:app --reload --port 8001
```

### Error: "puerto 3000 ya está en uso"

**Solución:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

O cambia el puerto en `frontend/vite.config.ts` o usa:
```bash
npm run dev -- --port 3001
```

### Error: "ModuleNotFoundError" en Python

**Solución:**
1. Asegúrate de tener el entorno virtual activado
2. Reinstala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Error: "npm ERR!" al instalar dependencias

**Solución:**
1. Limpia la caché de npm:
   ```bash
   npm cache clean --force
   ```

2. Elimina `node_modules` y reinstala:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

### Error: "Docker no se encuentra"

**Solución:**
1. Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop/
2. Asegúrate de que Docker Desktop esté corriendo (verifica el ícono en la bandeja del sistema)
3. Reinicia tu terminal después de instalar Docker

### El frontend no se conecta al backend

**Solución:**
1. Verifica que el backend esté corriendo en http://localhost:8000
2. Abre http://localhost:8000/health en tu navegador - debería mostrar `{"status":"healthy"}`
3. Verifica que no haya errores de CORS en la consola del navegador (F12)
4. Revisa `frontend/vite.config.ts` - el proxy debería apuntar a `http://localhost:8000`

---

## 📊 Datos del Proyecto

El proyecto incluye un generador de datos sintéticos realistas. Al ejecutar por primera vez, se generarán automáticamente:

- 16 ciudades globales en 5 continentes
- 48+ eventos históricos (2022-2024)
- Métricas diarias de turismo, ocupación hotelera y precios
- Análisis de impacto económico

Los datos se cargan automáticamente desde los archivos CSV en `data/examples/`:
- `cities.csv` - Información de ciudades
- `events.csv` - Eventos históricos
- `event_impacts.csv` - Impactos económicos
- `tourism_metrics.csv` - Métricas de turismo
- `hotel_metrics.csv` - Métricas hoteleras
- `mobility_metrics.csv` - Métricas de movilidad
- `economic_metrics.csv` - Métricas económicas

Para cargar datos reales, puedes subir archivos CSV/XLSX desde la aplicación o usar las APIs de fuentes externas (AIRROI, Eurostat, World Bank).

---

## 🏗️ Estructura del Proyecto

```
Evently/
├── backend/                # API REST + Motor de análisis
│   ├── app/
│   │   ├── api/           # Endpoints FastAPI
│   │   ├── models/        # Modelos de base de datos
│   │   ├── services/      # Lógica de negocio
│   │   ├── analytics/     # Motor de análisis de impacto
│   │   ├── ml/            # Modelos de Machine Learning
│   │   └── main.py        # Punto de entrada FastAPI
│   ├── requirements.txt   # Dependencias Python
│   └── Dockerfile         # Imagen Docker del backend
│
├── frontend/              # Dashboard React
│   ├── src/
│   │   ├── components/   # Componentes reutilizables
│   │   ├── pages/        # Páginas principales
│   │   ├── services/     # Cliente API
│   │   └── config/        # Configuración
│   ├── package.json      # Dependencias Node.js
│   └── Dockerfile        # Imagen Docker del frontend
│
├── data/                  # Datos y scripts
│   ├── scripts/          # Generadores y ETL
│   ├── examples/         # Ejemplos de CSV
│   └── processed/        # Datos procesados
│
├── docker-compose.yml     # Orquestación de servicios
├── start.sh              # Script de inicio (Linux/Mac)
├── dev.sh                # Script de desarrollo
└── README.md             # Este archivo
```

---

## 🌐 URLs de Acceso

Una vez ejecutado el proyecto, accede a:

- **🌐 Frontend (Aplicación Web)**: http://localhost:3000
- **📡 Backend (API)**: http://localhost:8000
- **📚 Documentación API (Swagger)**: http://localhost:8000/api/v1/docs
- **📚 Documentación API (ReDoc)**: http://localhost:8000/api/v1/redoc
- **❤️ Health Check**: http://localhost:8000/health

---

## 🧪 Verificar que todo funciona

### 1. Verificar Backend

Abre tu navegador en http://localhost:8000/health

Deberías ver:
```json
{"status":"healthy","service":"evently-api"}
```

### 2. Verificar Base de Datos

```bash
# Conectarse a PostgreSQL
psql -U evently -d evently -h localhost

# Verificar ciudades
SELECT COUNT(*) FROM cities;
# Debería mostrar 16

# Verificar eventos
SELECT COUNT(*) FROM events;
# Debería mostrar 48+

\q
```

### 3. Verificar Frontend

Abre http://localhost:3000 en tu navegador. Deberías ver:
- El globo 3D interactivo
- Pins en 16 ciudades
- Navegación funcional

---

## 🚀 Despliegue en Producción

El proyecto está optimizado para desplegarse en servicios cloud gratuitos:

- **Frontend**: Vercel (https://vercel.com)
- **Backend**: Railway (https://railway.app) o Render (https://render.com)
- **Base de datos**: Supabase (https://supabase.com) o Railway PostgreSQL

---

## 📝 Comandos Útiles

### Backend

```bash
# Entrenar modelo de ML
python backend/train_model.py

# Ver métricas del modelo
python show_model_metrics.py

# Ejecutar tests
cd backend
pytest
```

### Frontend

```bash
# Construir para producción
cd frontend
npm run build

# Preview de producción
npm run preview
```

### Docker

```bash
# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend

# Reiniciar servicios
docker-compose restart

# Reconstruir imágenes
docker-compose build --no-cache

# Limpiar todo (¡cuidado! elimina datos)
docker-compose down -v
```

---

## 📧 Soporte

Si encuentras problemas:

1. Revisa la sección "Solución de Problemas Comunes" arriba
2. Verifica los logs:
   - Backend: `docker-compose logs backend` o la terminal donde corre uvicorn
   - Frontend: `docker-compose logs frontend` o la terminal donde corre npm
3. Asegúrate de tener todas las dependencias instaladas correctamente

---

**Desarrollado con React, FastAPI y PostgreSQL** 🚀
