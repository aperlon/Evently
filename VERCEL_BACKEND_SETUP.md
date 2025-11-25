# 🚀 Desplegar Backend FastAPI en Vercel

## ✅ Sí, puedes desplegar el backend en Vercel

Vercel soporta FastAPI mediante **serverless functions**. Aquí te explico cómo configurarlo.

---

## ⚠️ Consideraciones Importantes

### Limitaciones de Vercel Serverless:

1. **Timeout**: 
   - Free tier: 10 segundos máximo por request
   - Pro tier: 60 segundos
   - ⚠️ **Tu modelo ML puede tardar más de 10 segundos en cargar la primera vez**

2. **Tamaño de archivos**:
   - Límite de 50MB por función
   - Tu modelo `.pkl` y CSVs deben caber

3. **Cold starts**:
   - La primera request después de inactividad puede tardar varios segundos
   - El modelo ML se carga en memoria cada vez (puede ser lento)

### ✅ Ventajas:

- Todo en un solo lugar (frontend + backend)
- Deploy automático desde Git
- HTTPS automático
- CDN global

---

## 📋 Configuración Paso a Paso

### Paso 1: Estructura de Archivos

Ya he creado:
- `api/index.py` - Punto de entrada para serverless functions
- `vercel.json` actualizado - Configuración para frontend + backend

### Paso 2: Configurar en Vercel

1. **Ve a Vercel Dashboard:**
   - https://vercel.com/dashboard

2. **Importa tu proyecto:**
   - Click en "Add New..." → "Project"
   - Selecciona tu repo `Evently`

3. **Configuración del Build:**
   - **Framework Preset**: Deja en blanco o "Other"
   - **Root Directory**: `.` (raíz del proyecto)
   - **Build Command**: 
     ```bash
     cd frontend && npm install && npm run build
     ```
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `cd frontend && npm install`

4. **Variables de entorno:**
   - **NO necesitas** `VITE_API_URL` porque el backend está en el mismo dominio
   - El frontend usará: `/api/v1/...` (relativo)
   - Si quieres usar absoluto, añade:
     ```
     VITE_API_URL=https://tu-proyecto.vercel.app/api/v1
     ```

5. **Deploy:**
   - Click en "Deploy"
   - Espera ~3-5 minutos

---

## 🔧 Ajustes Necesarios en el Código

### 1. Actualizar `frontend/src/services/api.ts`

Cambia la URL base para que use rutas relativas:

```typescript
// Cambiar de:
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// A:
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'
```

### 2. Actualizar CORS en Backend

En `backend/app/core/config.py`, asegúrate de que CORS permita tu dominio de Vercel:

```python
BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://*.vercel.app",  # Añade esto
]
```

---

## 🧪 Probar Localmente con Vercel CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy de prueba
vercel

# Deploy a producción
vercel --prod
```

---

## ⚡ Alternativa: Usar Vercel Edge Functions (Más Rápido)

Si el timeout de 10 segundos es un problema, puedes:

1. **Pre-cargar el modelo** en una función separada que se ejecute al deploy
2. **Usar Vercel KV** o **Vercel Blob** para cachear el modelo
3. **Optimizar el modelo** para que cargue más rápido

---

## 🆚 Comparación: Vercel vs Railway

| Característica | Vercel (Serverless) | Railway (Servidor) |
|----------------|---------------------|-------------------|
| **Timeout** | 10s (free) / 60s (pro) | Sin límite |
| **Cold Start** | Sí (lento primera vez) | No |
| **Costo** | Gratis (con límites) | $5/mes crédito |
| **Modelo ML** | Puede ser lento | Carga una vez |
| **Simplicidad** | Todo en un lugar | Dos servicios |

---

## 💡 Recomendación

**Para tu caso (modelo ML que puede tardar):**

1. **Opción A (Recomendada)**: Railway para backend + Vercel para frontend
   - Más confiable para ML
   - Sin límites de timeout
   - Modelo carga una vez y queda en memoria

2. **Opción B**: Todo en Vercel
   - Más simple (un solo servicio)
   - Puede ser lento en la primera request
   - Necesitarás optimizar el modelo

---

## 🚀 ¿Quieres probar Vercel?

Si quieres intentarlo, los archivos ya están configurados. Solo necesitas:

1. Actualizar `frontend/src/services/api.ts` (cambiar URL a `/api/v1`)
2. Desplegar en Vercel
3. Probar si el modelo carga en menos de 10 segundos

¿Quieres que actualice el código del frontend para usar rutas relativas?

