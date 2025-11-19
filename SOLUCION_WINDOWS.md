# 🔧 Solución para Problemas en Windows - EVENTLY

## ✅ Problemas Resueltos

He solucionado **2 problemas críticos** que estabas experimentando:

### 1. ❌ Frontend no iniciaba (Three.js)
**Error:** `Missing "./webgpu" specifier in "three" package`

**Causa:** El globo 3D (`react-globe.gl`) necesita una versión más nueva de Three.js

**Solución:** ✅ Actualizado `three.js` de v0.160.0 → v0.171.0 en `frontend/package.json`

### 2. ❌ Script de datos no se encontraba
**Error:** `No such file or directory: /app/../data/scripts/generate_sample_data.py`

**Causa:** El folder `data/` no estaba montado en el contenedor Docker

**Solución:** ✅ Agregado `- ./data:/data` en `docker-compose.yml`

---

## 🚀 Cómo Continuar (Windows PowerShell)

### Paso 1: Obtener los cambios

```powershell
# Ir a la carpeta del proyecto
cd Evently

# Descargar los cambios
git pull origin claude/event-impact-analyzer-01HGJEXfLFwTFRrCv7jZkvwV
```

### Paso 2: Reconstruir los contenedores

```powershell
# Detener todo
docker-compose down

# Reconstruir con los cambios
docker-compose up -d --build
```

**⏳ Esto tardará 2-3 minutos** mientras:
- Reinstala las dependencias del frontend con Three.js v0.171.0
- Monta el folder data/ correctamente

### Paso 3: Generar datos (con la nueva ruta)

```powershell
# Espera 30 segundos para que todo esté listo
Start-Sleep -Seconds 30

# Genera los datos (NUEVA RUTA CORRECTA)
docker-compose exec backend python /data/scripts/generate_sample_data.py
```

Deberías ver:
```
✅ Successfully generated sample data!
Cities: 16
Events: 12
```

### Paso 4: Verificar que funciona

```powershell
# Ver los contenedores (deben ser 3: db, backend, frontend)
docker ps

# Ver logs del frontend (NO debe haber errores de Three.js)
docker-compose logs frontend --tail 20
```

**Deberías ver algo como:**
```
evently-frontend  | VITE v5.0.11 ready in 1234 ms
evently-frontend  | ➜  Local:   http://localhost:3000/
evently-frontend  | ➜  Network: http://172.18.0.4:3000/
```

### Paso 5: ¡Abrir en el navegador!

Abre: **http://localhost:3000**

Deberías ver:
- 🌍 Globo 3D rotando
- 📍 16 pins rojos en las ciudades
- 📊 Stats: $12.4B impacto, 847K empleos, 420% ROI

---

## 📋 Checklist Rápido

- [ ] Ejecuté `git pull` para descargar los cambios
- [ ] Ejecuté `docker-compose down`
- [ ] Ejecuté `docker-compose up -d --build`
- [ ] Esperé 30 segundos
- [ ] Ejecuté el script de datos con la NUEVA ruta `/data/scripts/...`
- [ ] Vi 3 contenedores con `docker ps`
- [ ] Los logs del frontend NO muestran errores
- [ ] Abrí http://localhost:3000 y veo el globo 3D

---

## 🆘 Si Aún Tienes Problemas

### Frontend sigue sin funcionar

```powershell
# Ver logs detallados
docker-compose logs frontend --tail 50

# Si hay errores de dependencias, entra al contenedor y actualiza manualmente:
docker-compose exec frontend sh
npm install three@latest
exit
docker-compose restart frontend
```

### Base de datos vacía

```powershell
# Regenerar datos
docker-compose exec backend python /data/scripts/generate_sample_data.py
```

### Puerto 3000 ocupado

```powershell
# Ver qué está usando el puerto
netstat -ano | findstr :3000

# Detener Docker y cambiar puerto en docker-compose.yml (línea 46)
# Cambia "3000:3000" por "3001:3000"
docker-compose down
docker-compose up -d --build
# Luego abre http://localhost:3001
```

---

## 🎯 Comandos Útiles Windows

```powershell
# Ver todos los contenedores
docker ps -a

# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar todo
docker-compose restart

# Limpiar y empezar de cero
docker-compose down -v
docker-compose up -d --build
```

---

## 📞 Lo Que Hice (Resumen Técnico)

1. **frontend/package.json**: `"three": "^0.171.0"`
2. **docker-compose.yml**: Agregué `- ./data:/data` en backend volumes
3. **Todos los .md y scripts**: Cambié `/app/../data/scripts/` → `/data/scripts/`

Archivos modificados:
- `frontend/package.json`
- `docker-compose.yml`
- `QUICKSTART.md`
- `TUTORIAL_COMPLETO.md`
- `README.md`
- `SETUP.md`
- `start.sh`

---

**¡Ahora todo debería funcionar perfectamente! 🎉**

Si sigues teniendo problemas, copia y pega el error exacto y te ayudo.
