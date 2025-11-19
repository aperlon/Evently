# 🚀 Tutorial Completo: Cómo Correr Evently desde Cero

**Guía paso a paso para principiantes** - ¡En 15 minutos tendrás todo funcionando!

---

## 📋 Índice

1. [Prerequisitos](#-prerequisitos)
2. [Opción 1: Con Docker (MÁS FÁCIL)](#-opción-1-con-docker-más-fácil-recomendado)
3. [Opción 2: Sin Docker (Más rápido para desarrollo)](#-opción-2-sin-docker-más-rápido-para-desarrollo)
4. [Verificar que Funciona](#-verificar-que-funciona)
5. [Explorar la Aplicación](#-explorar-la-aplicación)
6. [BONUS: Deploy en Producción (Vercel + Supabase)](#-bonus-deploy-en-producción-gratis)
7. [Troubleshooting](#-troubleshooting)

---

## 📦 Prerequisitos

### ¿Qué necesitas instalar?

Depende de cómo quieras correr el proyecto:

| Con Docker ✅ | Sin Docker ⚙️ |
|--------------|---------------|
| **Solo necesitas:** | **Necesitas instalar:** |
| • Docker Desktop | • Python 3.11+ |
| • Git | • Node.js 18+ |
| | • PostgreSQL 15 |
| | • Git |

---

## 🔽 Instalación de Prerequisitos

### 1️⃣ Instalar Git

**Windows:**
```bash
# Descarga de: https://git-scm.com/download/win
# Ejecuta el instalador
```

**Mac:**
```bash
# Usando Homebrew
brew install git

# O descarga de: https://git-scm.com/download/mac
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install git
```

### 2️⃣ Opción A: Instalar Docker Desktop (RECOMENDADO)

**¿Por qué Docker?** Todo funciona automáticamente sin configuración manual.

**Windows/Mac:**
1. Descarga Docker Desktop: https://www.docker.com/products/docker-desktop
2. Instala el archivo descargado
3. Abre Docker Desktop
4. Espera a que diga "Docker Desktop is running"

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# Añade tu usuario al grupo docker
sudo usermod -aG docker $USER
# Cierra sesión y vuelve a entrar
```

**Verificar instalación:**
```bash
docker --version
# Debería mostrar: Docker version 24.x.x

docker-compose --version
# Debería mostrar: docker-compose version 2.x.x
```

### 2️⃣ Opción B: Instalar Python, Node y PostgreSQL (SIN DOCKER)

Solo si NO quieres usar Docker.

**Python 3.11+:**
- Windows/Mac: https://www.python.org/downloads/
- Linux: `sudo apt install python3.11 python3.11-venv python3-pip`

**Node.js 18+:**
- Windows/Mac: https://nodejs.org/ (descarga LTS)
- Linux:
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  sudo apt install nodejs
  ```

**PostgreSQL 15:**
- Windows: https://www.postgresql.org/download/windows/
- Mac: `brew install postgresql@15`
- Linux:
  ```bash
  sudo apt install postgresql-15 postgresql-contrib-15
  sudo systemctl start postgresql
  ```

**Verificar instalaciones:**
```bash
python3 --version  # Python 3.11+
node --version     # v18.x.x
npm --version      # 9.x.x
psql --version     # PostgreSQL 15.x
```

---

## 🎯 Clonar el Repositorio

```bash
# 1. Ve a tu carpeta de proyectos
cd ~/Proyectos  # o donde prefieras

# 2. Clona el repositorio
git clone https://github.com/aperlon/Evently.git

# 3. Entra al directorio
cd Evently

# 4. Verifica que estás en la carpeta correcta
ls -la
# Deberías ver: backend/, frontend/, data/, docker-compose.yml, etc.
```

---

## 🐳 Opción 1: Con Docker (MÁS FÁCIL - RECOMENDADO)

### Paso 1: Iniciar Todo con Un Solo Comando

```bash
# Ve al directorio del proyecto
cd Evently

# Ejecuta el script mágico ✨
./start.sh
```

**¿Qué hace este script?**
1. ✅ Verifica que Docker esté corriendo
2. ✅ Inicia PostgreSQL, Backend y Frontend
3. ✅ Genera 16 ciudades con datos de 2024
4. ✅ Verifica que todo funcione correctamente

**Esto tarda ~2-3 minutos la primera vez** (descarga imágenes Docker).

### Paso 2: ¡Ya Está! 🎉

Abre tu navegador:
- **Frontend**: http://localhost:3000 🌍 (Globo 3D interactivo)
- **API Docs**: http://localhost:8000/api/v1/docs 📚
- **API Health**: http://localhost:8000/health ✅

---

## ⚙️ Opción 2: Sin Docker (Más rápido para desarrollo)

### Paso 1: Setup de PostgreSQL

```bash
# Crear usuario y base de datos
sudo -u postgres psql

# Dentro de psql:
CREATE DATABASE evently;
CREATE USER evently WITH PASSWORD 'evently123';
GRANT ALL PRIVILEGES ON DATABASE evently TO evently;
\q
```

### Paso 2: Setup del Backend

```bash
# 1. Ve a la carpeta backend
cd Evently/backend

# 2. Crea entorno virtual de Python
python3 -m venv venv

# 3. Activa el entorno virtual
# En Mac/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 4. Instala dependencias
pip install -r requirements.txt

# 5. Configura variables de entorno
cp .env.example .env
# Edita .env si es necesario (la configuración por defecto funciona)

# 6. Inicia el backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Deja esta terminal abierta** ✅

### Paso 3: Setup del Frontend (Nueva Terminal)

```bash
# 1. Abre una NUEVA terminal y ve al frontend
cd Evently/frontend

# 2. Instala dependencias de Node
npm install

# 3. Inicia el frontend
npm run dev
```

**Deja esta terminal abierta también** ✅

### Paso 4: Generar Datos (Tercera Terminal)

```bash
# 1. Abre una TERCERA terminal
cd Evently/backend

# 2. Activa el entorno virtual
source venv/bin/activate  # Mac/Linux
# o
venv\Scripts\activate  # Windows

# 3. Genera los datos de las 16 ciudades
python ../data/scripts/generate_sample_data.py
```

**Verás algo como:**
```
✅ Conectado a la base de datos
📍 Insertando 16 ciudades...
  → London
  → Tokyo
  → Paris
  → New York
  ... (12 más)
📅 Creando eventos para 2024...
📊 Generando métricas...
✅ ¡Datos generados exitosamente!
```

### Paso 5: ¡Listo! 🎉

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000

---

## ✅ Verificar que Funciona

### Test Rápido en el Navegador

**1. Abre el Globo 3D:**
```
http://localhost:3000
```
Deberías ver un globo terráqueo girando con 16 pins rojos. ¡Haz click en cualquier ciudad!

**2. Prueba la API:**
```
http://localhost:8000/api/v1/docs
```
Deberías ver la documentación interactiva de Swagger.

### Test desde la Terminal

```bash
# 1. Salud del sistema
curl http://localhost:8000/health

# 2. Listar ciudades (deberías ver 16)
curl http://localhost:8000/api/v1/cities | jq

# 3. Ver eventos
curl http://localhost:8000/api/v1/events | jq

# 4. Dashboard KPIs
curl http://localhost:8000/api/v1/analytics/dashboard/kpis | jq
```

**Si todo responde → ¡ÉXITO! 🎉**

---

## 🌍 Explorar la Aplicación

### 1. Landing Page - Globo 3D Interactivo 🌎
```
http://localhost:3000
```

**Qué verás:**
- Globo terráqueo 3D girando automáticamente
- 16 pins rojos en ciudades globales
- Stats impactantes: $12.4B analizado, 847K empleos, 420% ROI
- Click en cualquier ciudad para ver detalles

**Prueba esto:**
- Haz click en **Rio de Janeiro** 🇧🇷
- Verás: población, turistas, hoteles, precios
- Click en "View Events in Rio de Janeiro"

### 2. Dashboard Analítico 📊
```
http://localhost:3000/dashboard
```

**Qué verás:**
- KPIs principales
- Gráficos de tendencias
- Lista de eventos recientes
- Impacto económico total

### 3. Explorar Eventos 🎪
```
http://localhost:3000/events
```

**Qué verás:**
- Lista de todos los eventos disponibles
- Filtros por ciudad, tipo, año
- Click en cualquier evento para ver análisis detallado

### 4. Comparar Ciudades/Eventos 🔍
```
http://localhost:3000/compare
```

**Prueba esto:**
- Selecciona "London" vs "Paris"
- O "Carnival" vs "Fashion Week"
- Verás gráficos comparativos lado a lado

### 5. Simulador What-If 🔮
```
http://localhost:3000/simulator
```

**Prueba esto:**
- Selecciona un evento (ej: Rio Carnival)
- Cambia: "¿Qué pasa si aumenta la asistencia 50%?"
- Verás proyecciones de impacto económico

### 6. Sobre Nosotros 📄
```
http://localhost:3000/about
```
- Misión y visión
- Público objetivo
- Stats de impacto

### 7. Metodología 🧪
```
http://localhost:3000/methodology
```
- Proceso Design Thinking
- Pipeline ETL visualizado
- Cómo calculamos el impacto

### 8. Casos de Éxito 📚
```
http://localhost:3000/case-studies
```
- **Rio Carnival 2024**: $1.2B impacto, 520% ROI
- **Paris Fashion Week**: $685M impacto, 380% ROI
- **Tokyo Game Show**: $428M impacto, 340% ROI

---

## 🚀 BONUS: Deploy en Producción (GRATIS)

¿Quieres tenerlo online para mostrarlo a otros?

### Arquitectura Recomendada:

```
Frontend (Vercel) → Backend (Railway) → Database (Supabase)
     GRATIS              $5 crédito           GRATIS
```

### Paso 1: Deploy de Base de Datos (Supabase)

1. **Crea cuenta en Supabase:**
   - Ve a https://supabase.com
   - Click en "Start your project" → Sign Up
   - Verifica tu email

2. **Crea un proyecto:**
   - Click en "New Project"
   - Nombre: `evently-prod`
   - Database Password: `TuPasswordSegura123!` (guárdala)
   - Region: Elige la más cercana
   - Click en "Create new project" (tarda ~2 min)

3. **Obtén la URL de conexión:**
   - Ve a "Settings" (⚙️) → "Database"
   - Copia la "Connection string" (modo: URI)
   - Se ve así: `postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres`
   - Guárdala, la necesitarás después

4. **Opcional: Carga los datos iniciales:**
   ```bash
   # Desde tu máquina local
   export DATABASE_URL="postgresql://postgres:TuPassword@db.xxx.supabase.co:5432/postgres"

   # Genera los datos
   cd Evently/backend
   source venv/bin/activate
   python ../data/scripts/generate_sample_data.py
   ```

### Paso 2: Deploy del Backend (Railway)

1. **Crea cuenta en Railway:**
   - Ve a https://railway.app
   - Click en "Login" → GitHub (más fácil)
   - Autoriza Railway

2. **Crea nuevo proyecto:**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Busca y selecciona tu repositorio `Evently`
   - Railway detectará automáticamente que es Python

3. **Configura variables de entorno:**
   - Click en tu servicio → "Variables"
   - Añade estas variables:
   ```
   DATABASE_URL=postgresql://postgres:TuPassword@db.xxx.supabase.co:5432/postgres
   PYTHONPATH=/app/backend
   PORT=8000
   ```

4. **Configura el build:**
   - Ve a "Settings" → "Build"
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Deploy:**
   - Click en "Deploy"
   - Espera ~3-5 minutos
   - Obtendrás una URL como: `https://evently-backend.up.railway.app`

6. **Verifica que funciona:**
   ```bash
   curl https://tu-backend.up.railway.app/health
   ```

### Paso 3: Deploy del Frontend (Vercel)

1. **Crea cuenta en Vercel:**
   - Ve a https://vercel.com
   - Click en "Sign Up" → GitHub
   - Autoriza Vercel

2. **Importa proyecto:**
   - Click en "Add New..." → "Project"
   - Busca tu repo `Evently`
   - Click en "Import"

3. **Configura el build:**
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Configura variables de entorno:**
   - En "Environment Variables" añade:
   ```
   VITE_API_URL=https://tu-backend.up.railway.app
   ```

5. **Deploy:**
   - Click en "Deploy"
   - Espera ~2 minutos
   - ¡Listo! Tendrás una URL como: `https://evently.vercel.app`

### Paso 4: ¡Comparte tu App! 🎉

```
Tu app está ONLINE en:
https://evently.vercel.app

¡Compártela con quien quieras!
```

**Costos:**
- Frontend (Vercel): **GRATIS** (100 GB bandwidth/mes)
- Database (Supabase): **GRATIS** (500 MB, 2 GB bandwidth)
- Backend (Railway): **$5 crédito gratis**, luego ~$5-10/mes

---

## 🛠️ Comandos Útiles

### Con Docker

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Reiniciar todo
docker-compose restart

# Detener todo
docker-compose down

# Limpiar y empezar de cero (CUIDADO: borra la BD)
docker-compose down -v
./start.sh

# Regenerar datos
docker-compose exec backend python /data/scripts/generate_sample_data.py

# Entrar a la base de datos
docker-compose exec db psql -U evently

# Ver tablas
docker-compose exec db psql -U evently -c "\dt"
```

### Sin Docker

```bash
# Backend (Terminal 1)
cd Evently/backend
source venv/bin/activate
uvicorn app.main:app --reload

# Frontend (Terminal 2)
cd Evently/frontend
npm run dev

# Regenerar datos (Terminal 3)
cd Evently/backend
source venv/bin/activate
python ../data/scripts/generate_sample_data.py

# Ver logs del backend
# Los verás en la Terminal 1 en tiempo real

# Limpiar base de datos
psql -U evently -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
python ../data/scripts/generate_sample_data.py
```

---

## ❌ Troubleshooting

### Problema: "Puerto ya en uso"

```bash
# Ver qué está usando el puerto
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL

# Matar el proceso
kill -9 <PID>

# O usa otros puertos editando docker-compose.yml o package.json
```

### Problema: "Docker no se inicia"

```bash
# Reinicia Docker Desktop
# Cierra y abre Docker Desktop

# En Linux, reinicia el servicio:
sudo systemctl restart docker
```

### Problema: "Base de datos vacía"

```bash
# Con Docker:
docker-compose exec backend python /data/scripts/generate_sample_data.py

# Sin Docker:
cd backend
source venv/bin/activate
python ../data/scripts/generate_sample_data.py
```

### Problema: "Frontend muestra error de conexión"

```bash
# Verifica que el backend esté corriendo:
curl http://localhost:8000/health

# Si no responde, revisa logs:
docker-compose logs backend  # Con Docker
# O mira la Terminal 1 (sin Docker)
```

### Problema: "npm install falla"

```bash
# Limpia caché y reinstala:
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Problema: "Python no encuentra módulos"

```bash
# Asegúrate de estar en el venv:
cd backend
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstala dependencias:
pip install --upgrade pip
pip install -r requirements.txt
```

### Problema: "El globo 3D no carga"

```bash
# Revisa la consola del navegador (F12)
# Usualmente es un problema de red

# Solución: Recarga la página (Ctrl+R)
# O limpia caché del navegador (Ctrl+Shift+R)
```

---

## 📚 Documentación Adicional

- **README.md** - Visión general y features
- **QUICKSTART.md** - Inicio rápido (5 min)
- **SIN_DOCKER.md** - Guía detallada sin Docker
- **DEPLOYMENT.md** - Deploy en producción completo
- **docs/FILE_UPLOADS.md** - Cómo importar tus propios datos (CSV/XLSX)

---

## 🎓 Próximos Pasos

1. ✅ **Explora todas las páginas** - Globo, Dashboard, Events, Compare, About, Cases
2. 📊 **Prueba el simulador What-If** - Cambia variables y ve el impacto
3. 📁 **Importa tus datos** (opcional) - Sube CSV/XLSX con tus propios eventos
4. 🎨 **Personaliza** - Cambia colores, añade ciudades, modifica stats
5. 🚀 **Despliega** - Compártelo en Vercel + Supabase
6. 🌟 **Contribuye** - Abre issues o PRs en GitHub

---

## 💡 Tips Finales

- **Primera carga:** Tarda ~30 segundos en cargar todo
- **Datos:** Incluye 16 ciudades con eventos de 2024
- **API Docs:** Usa `/api/v1/docs` para probar endpoints interactivamente
- **Hot Reload:** Los cambios en el código se reflejan automáticamente
- **Logs:** Siempre revisa logs si algo falla (`docker-compose logs -f`)

---

## 🤝 ¿Necesitas Ayuda?

- 📧 Email: contacto@evently-project.com
- 🐛 Issues: https://github.com/aperlon/Evently/issues
- 📖 Docs: Ver carpeta `docs/` del proyecto

---

**¡Disfruta analizando el impacto económico de eventos urbanos! 🎉🌍📊**

**Made with ❤️ for city planners, event organizers, and urban economists**
