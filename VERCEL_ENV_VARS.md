# Variables de Entorno para Vercel

## Frontend (Vercel) - OBLIGATORIA

### `VITE_API_URL`
- **Descripción**: URL base del backend API
- **Ejemplo**: `https://tu-backend.railway.app/api/v1` o `https://tu-backend.vercel.app/api/v1`
- **Obligatoria**: ✅ SÍ
- **Entornos**: Production, Preview, Development

## Backend (si se despliega en Vercel como Serverless Functions)

### `DATABASE_URL` (Opcional)
- **Descripción**: URL de conexión a PostgreSQL
- **Ejemplo**: `postgresql://user:password@host:5432/database`
- **Obligatoria**: ❌ NO (solo si usas base de datos)
- **Entornos**: Production, Preview, Development

### `SECRET_KEY` (Recomendado)
- **Descripción**: Clave secreta para JWT y seguridad
- **Ejemplo**: Genera una clave aleatoria segura (mínimo 32 caracteres)
- **Obligatoria**: ⚠️ RECOMENDADO
- **Entornos**: Production, Preview, Development
- **Cómo generar**: 
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

### `AIRROI_API_KEY` (Opcional)
- **Descripción**: API key para AirROI (solo si usas esta integración)
- **Ejemplo**: `tu-api-key-aqui`
- **Obligatoria**: ❌ NO
- **Entornos**: Production, Preview, Development

## Configuración en Vercel

1. Ve a tu proyecto en Vercel Dashboard
2. Click en **Settings** → **Environment Variables**
3. Añade cada variable:
   - **Key**: Nombre de la variable (ej: `VITE_API_URL`)
   - **Value**: Valor de la variable
   - **Environments**: Selecciona Production, Preview, Development según necesites
4. Click en **Save**
5. Vuelve a desplegar para que los cambios surtan efecto

## Ejemplo de Configuración Mínima

Para un despliegue básico del frontend en Vercel:

```
VITE_API_URL=https://tu-backend.railway.app/api/v1
```

## Notas Importantes

- Las variables que empiezan con `VITE_` son accesibles en el frontend
- Las variables sin `VITE_` son solo para el backend
- Si cambias variables de entorno, necesitas hacer un nuevo deploy
- Para desarrollo local, crea un archivo `.env` en `frontend/` con estas variables

