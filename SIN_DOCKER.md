# 🚀 Ejecutar Evently SIN DOCKER

**¿Por qué sin Docker?** Docker puede ser lento/pesado. Si solo quieres desarrollar, esto es más rápido.

---

## ⚡ Opción 1: Script Automático (Recomendado)

```bash
cd Evently
./dev.sh
```

**Listo!** El script:
- ✅ Instala dependencias automáticamente
- ✅ Genera datos de muestra
- ✅ Inicia Backend + Frontend
- ✅ Muestra los logs

**Accede a:**
- Frontend: http://localhost:3000
- API: http://localhost:8000/api/v1/docs

---

## 📝 Opción 2: Manual (Paso a Paso)

Si prefieres hacerlo manualmente o entender qué pasa:

### **Paso 0: Instalar Prerequisitos**

```bash
# Python 3.11+
python3 --version

# Node.js 18+
node --version

# PostgreSQL 15
psql --version
```

**¿No tienes algo?**
- **Python**: https://www.python.org/downloads/
- **Node**: https://nodejs.org/
- **PostgreSQL**: https://www.postgresql.org/download/

---

### **Paso 1: Base de Datos**

**Opción A: PostgreSQL Local**
```bash
# Crear base de datos
createdb evently

# Crear usuario (si es necesario)
psql -c "CREATE USER evently WITH PASSWORD 'evently123';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE evently TO evently;"
```

**Opción B: PostgreSQL con Docker (solo DB)**
```bash
# Si no quieres instalar PostgreSQL, usa Docker solo para esto
docker run -d \
  --name evently-db \
  -p 5432:5432 \
  -e POSTGRES_USER=evently \
  -e POSTGRES_PASSWORD=evently123 \
  -e POSTGRES_DB=evently \
  postgres:15-alpine
```

---

### **Paso 2: Backend**

**Terminal 1:**
```bash
cd backend

# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# O en Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar si es necesario (ya está configurado por defecto)

# 5. Generar datos de muestra (solo primera vez)
cd ..
python data/scripts/generate_sample_data.py

# 6. Iniciar API
cd backend
uvicorn app.main:app --reload

# ✅ Backend corriendo en http://localhost:8000
```

**Ver si funciona:**
```bash
# En otra terminal:
curl http://localhost:8000/health
# Debería responder: {"status":"healthy"}
```

---

### **Paso 3: Frontend**

**Terminal 2 (nueva terminal):**
```bash
cd frontend

# 1. Instalar dependencias (solo primera vez)
npm install

# 2. Configurar .env
cp .env.example .env

# 3. Iniciar desarrollo
npm run dev

# ✅ Frontend corriendo en http://localhost:3000
```

---

### **Paso 4: ¡Abre tu Navegador!**

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/v1/docs

---

## 🔄 Rutina Diaria de Desarrollo

### **Primera vez (setup completo):**
```bash
./dev.sh
```

### **Días siguientes (ya está todo instalado):**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## 🆚 Comparación: Docker vs Sin Docker

| Aspecto | Con Docker | Sin Docker |
|---------|-----------|------------|
| **Setup inicial** | 1 comando | 3 pasos (Python, Node, PostgreSQL) |
| **Velocidad** | ⚠️ Más lento | ✅ Más rápido |
| **Recursos** | 🔴 Usa más RAM | 🟢 Usa menos |
| **Hot Reload** | ⚠️ A veces lento | ✅ Instantáneo |
| **Compatibilidad** | ✅ Igual en todos lados | ⚠️ Depende del OS |
| **Ideal para** | Producción, CI/CD | Desarrollo local |

---

## 💡 Tips para Desarrollo

### **Hot Reload Automático:**

Ambos (Backend y Frontend) tienen hot reload:
- **Backend**: Guarda un `.py` → API se recarga automáticamente
- **Frontend**: Guarda un `.tsx` → Navegador se actualiza solo

### **Ver Logs en Tiempo Real:**

```bash
# Si usas dev.sh:
tail -f backend.log
tail -f frontend.log

# Si lo haces manual:
# Los logs ya están en las terminales
```

### **Debugger:**

**Backend (Python):**
```python
# En cualquier archivo .py
import pdb; pdb.set_trace()  # Breakpoint
```

**Frontend (React):**
```typescript
// En cualquier archivo .tsx
console.log('Debug:', variable)
debugger;  // Breakpoint en DevTools
```

---

## ❓ Troubleshooting

### **"Puerto ya en uso"**

```bash
# Ver qué está usando el puerto
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Matar proceso
kill -9 <PID>
```

### **"Cannot connect to database"**

```bash
# Verificar que PostgreSQL esté corriendo
psql -U evently -d evently -c "SELECT 1;"

# Si usas Docker para DB:
docker ps | grep evently-db
```

### **"ModuleNotFoundError" (Backend)**

```bash
# Asegúrate de activar el venv
cd backend
source venv/bin/activate  # IMPORTANTE!
pip install -r requirements.txt
```

### **"Module not found" (Frontend)**

```bash
cd frontend
rm -rf node_modules
npm install
```

### **Regenerar datos:**

```bash
cd backend
source venv/bin/activate
cd ..
python data/scripts/generate_sample_data.py
```

---

## 🎓 Siguiente Nivel

### **Agregar nueva ciudad:**

```bash
curl -X POST http://localhost:8000/api/v1/cities \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Barcelona",
    "country": "Spain",
    "country_code": "ESP",
    "continent": "Europe",
    "latitude": 41.3874,
    "longitude": 2.1686,
    "timezone": "Europe/Madrid",
    "population": 1620000,
    "annual_tourists": 9000000,
    "hotel_rooms": 70000,
    "avg_hotel_price_usd": 150
  }'
```

### **Agregar nuevo evento:**

```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "city_id": 1,
    "name": "Primavera Sound 2024",
    "event_type": "music",
    "start_date": "2024-05-30",
    "end_date": "2024-06-01",
    "expected_attendance": 200000
  }'
```

### **Importar datos reales:**

```bash
python data/scripts/import_real_data.py
```

---

## 🚀 Producción

Cuando quieras desplegar:

**Entonces SÍ usa Docker:**
```bash
docker-compose up -d
```

O despliega en:
- **Backend**: Railway, Render, Heroku
- **Frontend**: Vercel, Netlify, Cloudflare Pages
- **Database**: Supabase, Railway, AWS RDS

---

## 📚 Resumen

**Desarrollo Local (Rápido):**
```bash
./dev.sh
```

**O manual:**
1. Terminal 1: `cd backend && source venv/bin/activate && uvicorn app.main:app --reload`
2. Terminal 2: `cd frontend && npm run dev`
3. Navega a http://localhost:3000

**¡Eso es todo! No necesitas Docker para desarrollar.**

---

**¿Preguntas?** Lee QUICKSTART.md o SETUP.md
