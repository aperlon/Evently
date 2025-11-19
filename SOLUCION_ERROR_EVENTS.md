# 🔧 Solución: Error "Error loading events"

## ❌ Problema
El frontend muestra "Error loading events" porque el **backend no está corriendo**.

## ✅ Solución Paso a Paso

### **Paso 1: Instalar PostgreSQL**

```bash
# Instalar PostgreSQL
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Iniciar PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear base de datos y usuario
sudo -u postgres psql << EOF
CREATE DATABASE evently;
CREATE USER evently WITH PASSWORD 'evently123';
GRANT ALL PRIVILEGES ON DATABASE evently TO evently;
ALTER USER evently CREATEDB;
\q
EOF

echo "✅ PostgreSQL configurado!"
```

### **Paso 2: Configurar Backend**

```bash
cd /home/mateo/Evently/backend

# Crear entorno virtual (solo primera vez)
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# Crear archivo .env (si no existe)
cat > .env << EOF
DATABASE_URL=postgresql://evently:evently123@localhost:5432/evently
SECRET_KEY=dev-secret-key-change-in-production
EOF
```

### **Paso 3: Generar Datos de Muestra**

```bash
# Desde la raíz del proyecto
cd /home/mateo/Evently
cd backend
source venv/bin/activate
python ../data/scripts/generate_sample_data.py
```

### **Paso 4: Iniciar Backend**

**Terminal 1 (Backend):**
```bash
cd /home/mateo/Evently/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### **Paso 5: Verificar que Funciona**

En otra terminal:
```bash
curl http://localhost:8000/health
# Debería responder: {"status":"healthy","service":"evently-api"}

curl http://localhost:8000/api/v1/events
# Debería mostrar una lista de eventos en JSON
```

### **Paso 6: Iniciar Frontend (si no está corriendo)**

**Terminal 2 (Frontend):**
```bash
cd /home/mateo/Evently/frontend
npm install  # Solo primera vez
npm run dev
```

## 🚀 Método Rápido (Todo Automático)

Si prefieres que todo se configure automáticamente:

```bash
cd /home/mateo/Evently
./dev.sh
```

Este script:
- ✅ Verifica dependencias
- ✅ Configura backend
- ✅ Genera datos
- ✅ Inicia backend y frontend

## 🔍 Verificar que Todo Funciona

1. **Backend corriendo**: http://localhost:8000/health
2. **API Docs**: http://localhost:8000/api/v1/docs
3. **Frontend**: http://localhost:3000
4. **Lista de eventos**: http://localhost:3000/events

## ❓ Troubleshooting

### "Cannot connect to database"
```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql

# Probar conexión
psql -U evently -d evently -h localhost
# Password: evently123
```

### "Port 8000 already in use"
```bash
# Ver qué está usando el puerto
lsof -i :8000

# Matar proceso
kill -9 <PID>
```

### "ModuleNotFoundError"
```bash
cd backend
source venv/bin/activate  # IMPORTANTE!
pip install -r requirements.txt
```

## 📝 Resumen

**El error ocurre porque:**
- ❌ Backend no está corriendo
- ❌ PostgreSQL no está instalado/configurado

**Solución:**
1. Instalar PostgreSQL
2. Configurar backend
3. Generar datos
4. Iniciar backend en Terminal 1
5. Iniciar frontend en Terminal 2 (si no está corriendo)

**O simplemente ejecuta:**
```bash
./dev.sh
```

