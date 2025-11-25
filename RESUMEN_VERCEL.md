# ✅ Backend FastAPI en Vercel - Configuración Completa

## 🎯 Respuesta: SÍ, puedes desplegar el backend FastAPI en Vercel

He configurado todo para que puedas desplegar **frontend + backend** en Vercel usando serverless functions.

---

## 📁 Archivos Creados/Modificados

### ✅ Nuevos archivos:
1. **`api/index.py`** - Punto de entrada para serverless functions de Vercel
2. **`VERCEL_BACKEND_SETUP.md`** - Guía detallada
3. **`RESUMEN_VERCEL.md`** - Este archivo

### ✅ Archivos modificados:
1. **`vercel.json`** - Configurado para frontend + backend
2. **`frontend/src/services/api.ts`** - Usa rutas relativas en producción
3. **`backend/app/core/config.py`** - CORS actualizado para Vercel

---

## 🚀 Cómo Desplegar

### Paso 1: En Vercel Dashboard

1. Ve a https://vercel.com
2. Click en "Add New..." → "Project"
3. Selecciona tu repositorio `Evently`
4. **Configuración:**
   - **Framework Preset**: Deja en blanco o "Other"
   - **Root Directory**: `.` (raíz del proyecto)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `cd frontend && npm install`

5. **Variables de entorno:**
   - **NO necesitas** `VITE_API_URL` (usa rutas relativas)
   - Opcional: `SECRET_KEY` si quieres cambiar la clave por defecto

6. **Deploy:**
   - Click en "Deploy"
   - Espera ~3-5 minutos

### Paso 2: Verificar

1. **Backend**: `https://tu-proyecto.vercel.app/api/v1/health`
   - Debe responder: `{"status":"healthy","service":"evently-api"}`

2. **Frontend**: `https://tu-proyecto.vercel.app`
   - Debe cargar la aplicación

3. **Probar predicción:**
   - Ve a la página de predicción
   - Haz una predicción de prueba

---

## ⚠️ Limitaciones Importantes

### Timeout (Plan Gratuito):
- **10 segundos máximo** por request
- Si tu modelo ML tarda más en cargar, puede fallar
- **Solución**: Considera Railway para el backend si tienes problemas

### Cold Starts:
- La primera request después de inactividad puede tardar varios segundos
- El modelo ML se carga en memoria cada vez

### Tamaño de Archivos:
- Límite de 50MB por función
- Tu modelo `.pkl` y CSVs deben caber (deberían estar bien)

---

## 🔧 Si Tienes Problemas

### Error: "Function timeout"
- El modelo ML tarda más de 10 segundos
- **Solución**: Usa Railway para el backend en su lugar

### Error: "Module not found"
- Verifica que `requirements.txt` esté en `backend/`
- Vercel instalará las dependencias automáticamente

### Error: "CSV files not found"
- Los CSVs deben estar en `data/examples/`
- Verifica que estén en el repositorio

---

## 🆚 Comparación: Vercel vs Railway

| Aspecto | Vercel (Serverless) | Railway (Servidor) |
|---------|---------------------|-------------------|
| **Timeout** | 10s (free) | Sin límite |
| **Cold Start** | Sí (lento) | No |
| **Costo** | Gratis | $5/mes crédito |
| **Simplicidad** | ⭐⭐⭐⭐⭐ Todo en un lugar | ⭐⭐⭐ Dos servicios |
| **Para ML** | ⚠️ Puede ser lento | ✅ Mejor opción |

---

## 💡 Recomendación

**Para empezar rápido**: Prueba Vercel primero
- Si funciona bien → Perfecto, todo en un lugar
- Si tienes problemas de timeout → Cambia a Railway para el backend

---

## ✅ Checklist

- [x] `api/index.py` creado
- [x] `vercel.json` configurado
- [x] Frontend usa rutas relativas
- [x] CORS actualizado
- [ ] Desplegar en Vercel
- [ ] Probar `/api/v1/health`
- [ ] Probar predicción

---

## 🎉 ¡Listo!

Todo está configurado. Solo necesitas desplegar en Vercel y probar. Si tienes problemas, puedes cambiar a Railway para el backend (más confiable para ML).

¿Quieres que te ayude con el despliegue o tienes alguna pregunta?

