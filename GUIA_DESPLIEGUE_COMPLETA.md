# 🚀 Guía Completa de Despliegue - Evently

## 📋 Resumen

Tu aplicación tiene:
- **Backend**: FastAPI (Python) en `backend/`
- **Frontend**: React/Vite en `frontend/`

Necesitas desplegar ambos para que funcione en producción.

---

## 🎯 Opción 1: Railway (Backend) + Vercel (Frontend) - RECOMENDADO

### Paso 1: Desplegar Backend en Railway

1. **Crear cuenta en Railway:**
   - Ve a https://railway.app
   - Click en "Login" → GitHub
   - Autoriza Railway

2. **Crear nuevo proyecto:**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Busca y selecciona tu repositorio `Evently`

3. **Configurar el servicio:**
   - Railway detectará automáticamente que es Python
   - **Root Directory**: `backend` (IMPORTANTE)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Variables de entorno (opcionales):**
   - Click en "Variables"
   - Añade si necesitas:
     ```
     SECRET_KEY=tu-clave-secreta-aqui
     ```
   - **NOTA**: El modelo ML no necesita base de datos, funciona con archivos CSV

5. **Desplegar:**
   - Click en "Deploy"
   - Espera ~3-5 minutos
   - Obtendrás una URL como: `https://evently-backend.up.railway.app`

6. **Verificar que funciona:**
   ```bash
   curl https://tu-backend.up.railway.app/health
   # Debería responder: {"status":"healthy","service":"evently-api"}
   ```

### Paso 2: Desplegar Frontend en Vercel

1. **Crear cuenta en Vercel:**
   - Ve a https://vercel.com
   - Click en "Sign Up" → GitHub
   - Autoriza Vercel

2. **Importar proyecto:**
   - Click en "Add New..." → "Project"
   - Busca tu repo `Evently`
   - Click en "Import"

3. **Configurar el build:**
   - **Framework Preset**: `Vite` (debería detectarlo automáticamente)
   - **Root Directory**: `frontend` (IMPORTANTE)
   - **Build Command**: `npm run build` (automático)
   - **Output Directory**: `dist` (automático)

4. **Variables de entorno (OBLIGATORIO):**
   - Click en "Environment Variables"
   - Añade:
     ```
     VITE_API_URL=https://tu-backend.up.railway.app/api/v1
     ```
   - Reemplaza `tu-backend.up.railway.app` con la URL real de tu backend de Railway
   - Selecciona: Production, Preview, Development

5. **Desplegar:**
   - Click en "Deploy"
   - Espera ~2 minutos
   - ¡Listo! Tendrás una URL como: `https://evently.vercel.app`

---

## 🎯 Opción 2: Render (Backend) + Vercel (Frontend)

### Paso 1: Desplegar Backend en Render

1. **Crear cuenta en Render:**
   - Ve a https://render.com
   - Click en "Get Started" → GitHub
   - Autoriza Render

2. **Crear nuevo Web Service:**
   - Click en "New" → "Web Service"
   - Conecta tu repositorio `Evently`

3. **Configurar:**
   - **Name**: `evently-backend`
   - **Environment**: `Python 3`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Variables de entorno:**
   - Click en "Environment Variables"
   - Añade si necesitas:
     ```
     SECRET_KEY=tu-clave-secreta-aqui
     ```

5. **Desplegar:**
   - Click en "Create Web Service"
   - Espera ~5 minutos
   - Obtendrás una URL como: `https://evently-backend.onrender.com`

### Paso 2: Desplegar Frontend en Vercel

Sigue los mismos pasos de la Opción 1, pero usa la URL de Render:
```
VITE_API_URL=https://evently-backend.onrender.com/api/v1
```

---

## ✅ Verificación Final

1. **Backend funcionando:**
   - Abre: `https://tu-backend.up.railway.app/health`
   - Debe responder: `{"status":"healthy","service":"evently-api"}`

2. **Frontend funcionando:**
   - Abre: `https://tu-frontend.vercel.app`
   - Debe cargar la aplicación
   - Prueba hacer una predicción

3. **Si hay errores de CORS:**
   - En Railway/Render, añade la variable:
     ```
     BACKEND_CORS_ORIGINS=["https://tu-frontend.vercel.app"]
     ```
   - O edita `backend/app/core/config.py` para incluir tu dominio

---

## 🔧 Solución de Problemas

### Error: "Cannot connect to API"
- Verifica que `VITE_API_URL` en Vercel apunta correctamente al backend
- Verifica que el backend está corriendo (prueba `/health`)

### Error: "Model not found"
- El modelo ML se carga desde `backend/app/ml/saved_models/economic_impact_model.pkl`
- Asegúrate de que este archivo está en el repositorio
- Si no está, entrénalo localmente y súbelo al repo

### Error: "CSV files not found"
- Los CSVs están en `data/examples/*.csv`
- Asegúrate de que estos archivos están en el repositorio
- El modelo los necesita para funcionar

---

## 📝 Checklist de Despliegue

- [ ] Backend desplegado en Railway/Render
- [ ] Backend responde en `/health`
- [ ] Frontend desplegado en Vercel
- [ ] Variable `VITE_API_URL` configurada en Vercel
- [ ] Frontend carga correctamente
- [ ] Predicción funciona en producción

---

## 💡 Notas Importantes

1. **Gratis**: Railway y Render tienen planes gratuitos (con limitaciones)
2. **Modelo ML**: Se carga automáticamente desde los archivos guardados
3. **Datos**: Los CSVs deben estar en el repositorio para que el modelo funcione
4. **CORS**: Si tienes problemas, ajusta `BACKEND_CORS_ORIGINS` en el backend

---

¿Necesitas ayuda con algún paso específico? 🚀

