# 🚀 Deployment en Producción

Guía completa para desplegar Evently en producción usando servicios modernos (gratis o económicos).

---

## 🏗️ Arquitectura Recomendada

```
Frontend (Vercel)  →  Backend (Railway)  →  Database (Supabase)
     React              FastAPI              PostgreSQL
     GRATIS             $5/mes*              GRATIS
```

*Railway tiene tier gratuito con $5 crédito mensual

---

## 📦 **Opción 1: Stack Moderno (RECOMENDADO)**

### **Frontend: Vercel ⭐**

**¿Por qué Vercel?**
- ✅ Gratis para proyectos personales
- ✅ Deploy automático desde Git
- ✅ CDN global (rápido en todo el mundo)
- ✅ HTTPS automático
- ✅ Preview deploys (cada PR = URL única)
- ✅ Zero config para React/Next.js

**Pasos:**

1. **Crear cuenta en Vercel:**
   - https://vercel.com/signup

2. **Importar desde GitHub:**
   ```
   New Project → Import Git Repository → aperlon/Evently
   ```

3. **Configurar:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

4. **Variables de entorno:**
   ```
   VITE_API_URL=https://tu-backend.railway.app/api/v1
   ```

5. **Deploy:**
   - Click "Deploy"
   - ¡Listo en 2 minutos!

**URL final:** `https://evently-tu-usuario.vercel.app`

---

### **Database: Supabase ⭐**

**¿Por qué Supabase?**
- ✅ PostgreSQL gratis (500MB)
- ✅ Backups automáticos
- ✅ Dashboard visual
- ✅ Connection pooling
- ✅ SSL incluido

**Pasos:**

1. **Crear proyecto:**
   - https://supabase.com/dashboard
   - New Project → "evently"
   - Región: Elige la más cercana

2. **Obtener credenciales:**
   ```
   Settings → Database → Connection String (URI)

   Ejemplo:
   postgresql://postgres:tu-password@db.xxxxx.supabase.co:5432/postgres
   ```

3. **Crear las tablas:**
   ```bash
   # Opción A: Desde tu local
   cd backend
   source venv/bin/activate

   # Actualiza DATABASE_URL en .env con la de Supabase
   DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres

   # Genera las tablas
   python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

   # Carga datos
   python ../data/scripts/generate_sample_data.py
   ```

   ```bash
   # Opción B: Desde SQL Editor en Supabase
   # Copia y pega el schema de data/schemas/schema.sql (crear este archivo)
   ```

**Notas:**
- La DB es PostgreSQL normal, 100% compatible
- Puedes usar TablePlus/pgAdmin para conectarte
- Revisa límites gratis: 500MB storage, 2GB transferencia

---

### **Backend: Railway ⭐**

**¿Por qué Railway?**
- ✅ $5 gratis mensuales (suficiente para empezar)
- ✅ Deploy desde Git
- ✅ Python/FastAPI soportado
- ✅ Variables de entorno fáciles
- ✅ Logs en tiempo real
- ✅ Custom domain gratis

**Alternativas:**
- **Render** (gratis pero duerme después 15 min inactividad)
- **Fly.io** (gratis con límites)
- **Heroku** (ya no tiene tier gratis)

**Pasos:**

1. **Crear cuenta:**
   - https://railway.app/
   - Login with GitHub

2. **Nuevo proyecto:**
   ```
   New Project → Deploy from GitHub repo → Evently
   ```

3. **Configurar:**
   ```
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Variables de entorno:**
   ```
   DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
   SECRET_KEY=tu-secret-key-super-seguro-cambiar-esto
   AIRROI_API_KEY=tu-api-key-si-tienes
   BACKEND_CORS_ORIGINS=["https://evently-tu-usuario.vercel.app"]
   ```

5. **Deploy:**
   - Railway auto-detecta Python
   - Deploy automático
   - Te da una URL: `https://evently-production.up.railway.app`

6. **Generar datos (solo primera vez):**
   ```bash
   # Desde Railway CLI (instalar: npm i -g @railway/cli)
   railway login
   railway link
   railway run python ../data/scripts/generate_sample_data.py
   ```

**Costo estimado:** $0-5/mes (gratis con créditos)

---

## 📦 **Opción 2: Todo en un Solo Servicio**

### **Render (Backend + DB + Frontend)**

**Ventajas:**
- ✅ Todo en un lugar
- ✅ Tier gratis disponible

**Desventajas:**
- ⚠️ Free tier "duerme" después 15 min inactividad
- ⚠️ Primera request tarda ~30 segundos en despertar

**Pasos:**

1. **Database (PostgreSQL):**
   ```
   New → PostgreSQL
   Name: evently-db
   Plan: Free
   ```

2. **Backend:**
   ```
   New → Web Service
   Repo: aperlon/Evently
   Root Directory: backend
   Build: pip install -r requirements.txt
   Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT

   Environment:
   DATABASE_URL=[la de arriba]
   ```

3. **Frontend:**
   ```
   New → Static Site
   Root Directory: frontend
   Build: npm install && npm run build
   Publish: dist
   ```

**Costo:** Gratis (con limitación de sleep)

---

## 📦 **Opción 3: Serverless (Avanzado)**

### **Vercel + Serverless Functions + Supabase**

**Solo si quieres experimentar:**
- Frontend en Vercel
- Backend como Serverless Functions en Vercel
- DB en Supabase

**Limitaciones:**
- ⚠️ Serverless functions tienen timeout (10 seg en free)
- ⚠️ Analytics complejos pueden tardar más
- ⚠️ No ideal para este proyecto (mejor Railway)

---

## 🔧 **Configuración de CORS**

**En backend/.env o Railway:**
```bash
BACKEND_CORS_ORIGINS=["https://evently.vercel.app","https://evently-preview.vercel.app"]
```

**En backend/app/core/config.py** (ya está, solo verificar):
```python
BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "https://evently.vercel.app"  # Tu URL de Vercel
]
```

---

## 🌐 **Custom Domain (Opcional)**

### **Para Vercel (Frontend):**
1. Settings → Domains
2. Add: `evently.tudominio.com`
3. Configurar DNS (Vercel te dice cómo)

### **Para Railway (Backend):**
1. Settings → Networking → Custom Domain
2. Add: `api.tudominio.com`
3. Configurar DNS CNAME

---

## 📊 **Resumen de Costos**

| Servicio | Tier Gratis | Límites | Recomendado |
|----------|-------------|---------|-------------|
| **Vercel** (Frontend) | ✅ Sí | 100GB bandwidth/mes | ⭐ Mejor opción |
| **Supabase** (DB) | ✅ Sí | 500MB storage, 2GB transfer | ⭐ Mejor opción |
| **Railway** (Backend) | ✅ $5 crédito | ~500 horas/mes | ⭐ Mejor opción |
| **Render** (All-in-one) | ✅ Sí | Sleep después 15min | Alternativa |
| **Fly.io** (Backend) | ✅ Sí | 3 VM pequeñas | Alternativa |

**Total: GRATIS** (o ~$5/mes si pasas los límites)

---

## 🚀 **Deployment Rápido (5 minutos)**

```bash
# 1. Database (Supabase)
1. Crear proyecto en supabase.com
2. Copiar DATABASE_URL

# 2. Backend (Railway)
1. railway.app → New Project → From GitHub
2. Configurar variables de entorno (DATABASE_URL)
3. Deploy automático
4. Copiar URL del backend

# 3. Frontend (Vercel)
1. vercel.com → New Project → From GitHub
2. Root: frontend
3. Agregar VITE_API_URL=[URL de Railway]
4. Deploy automático

# ¡Listo!
```

---

## 🔒 **Seguridad**

**Antes de ir a producción:**

1. **Cambiar SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **HTTPS everywhere:**
   - Vercel y Railway lo dan gratis

3. **Variables de entorno:**
   - Nunca commits secrets en Git
   - Usa .env.example como template

4. **Rate limiting:**
   ```python
   # backend/app/main.py
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

5. **CORS específico:**
   ```python
   BACKEND_CORS_ORIGINS = [
       "https://evently.vercel.app"  # Solo tu dominio
   ]
   ```

---

## 📈 **Monitoreo**

**Railway:**
- Logs en tiempo real en dashboard
- Métricas de CPU/RAM

**Vercel:**
- Analytics en dashboard
- Web Vitals

**Supabase:**
- Database usage
- Query performance

---

## 🔄 **CI/CD Automático**

**¡Ya está configurado!**

```
Push a GitHub → Vercel auto-deploys frontend
                Railway auto-deploys backend
```

**Workflow:**
1. Haces cambios localmente
2. Git push
3. Vercel + Railway detectan cambios
4. Deploy automático en ~2 minutos
5. ¡Live en producción!

---

## 🧪 **Preview Deployments**

**Vercel (Frontend):**
- Cada Pull Request = URL única
- Perfecto para testing

**Railway (Backend):**
- Branches también se pueden deployar
- Settings → Environments

---

## 📊 **Scaling (Futuro)**

Cuando crezcas:

| Usuarios/Día | Stack | Costo/Mes |
|--------------|-------|-----------|
| < 1,000 | Vercel + Railway + Supabase Free | $0 |
| 1,000 - 10,000 | Same + Railway Pro | $5-20 |
| 10,000 - 100,000 | Vercel Pro + Railway + Supabase Pro | $50-200 |
| > 100,000 | AWS/GCP + CDN + Load balancer | $500+ |

---

## 🎯 **Recomendación Final**

**Para empezar HOY (mejor opción):**

```
Frontend: Vercel (gratis, 2 min setup)
Backend: Railway (gratis $5 crédito)
Database: Supabase (gratis 500MB)

Total: GRATIS
Setup: 10 minutos
```

**¿Por qué esta combinación?**
- ✅ Todo gratis para empezar
- ✅ Fácil de configurar
- ✅ Escalable cuando crezcas
- ✅ Deploy automático
- ✅ Usado por miles de startups

---

## 📚 **Próximos Pasos**

1. Lee la guía de tu servicio elegido
2. Deploy frontend a Vercel (más fácil)
3. Crea DB en Supabase
4. Deploy backend a Railway
5. Conecta todo
6. ¡Comparte tu URL!

---

## 🆘 **Troubleshooting**

**Error de CORS:**
```python
# Asegúrate de agregar tu URL de Vercel a BACKEND_CORS_ORIGINS
```

**Database connection timeout:**
```python
# Supabase tiene connection pooling
# Usa la URL con pooler: ...pooler.supabase.co
```

**Build fails en Vercel:**
```bash
# Verifica que package.json esté correcto
# Build command: npm run build (no "npm start")
```

**Railway out of memory:**
```bash
# Upgrade a plan con más RAM
# O optimiza queries (añade índices)
```

---

**¿Preguntas?** Abre un issue o lee la documentación de cada servicio.

**¡Tu app estará live en 10 minutos! 🚀**
