# 🚀 EVENTLY - Inicio Rápido (5 minutos)

> **📚 ¿Primera vez?** Lee el [TUTORIAL_COMPLETO.md](TUTORIAL_COMPLETO.md) para instrucciones detalladas desde cero

## ⚡ Opción 1: Script Automático (MÁS FÁCIL)

```bash
# 1. Ve al directorio del proyecto
cd Evently

# 2. Ejecuta el script de inicio
./start.sh

# 3. ¡Listo! Abre tu navegador en http://localhost:3000
```

**Eso es todo!** El script hace todo automáticamente:
- ✅ Verifica Docker
- ✅ Inicia todos los servicios
- ✅ Genera datos de muestra
- ✅ Verifica que todo funcione

---

## 📦 Opción 2: Docker Compose Manual

```bash
# 1. Inicia los servicios
docker-compose up -d

# 2. Espera 30 segundos para que todo esté listo
sleep 30

# 3. Genera los datos de muestra
docker-compose exec backend python /app/../data/scripts/generate_sample_data.py

# 4. Abre tu navegador
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/api/v1/docs
```

---

## 🔍 Verificar que Funciona

**Test rápido de la API:**
```bash
# Salud del sistema
curl http://localhost:8000/health

# Obtener ciudades
curl http://localhost:8000/api/v1/cities

# Obtener eventos
curl http://localhost:8000/api/v1/events

# Ver dashboard KPIs
curl http://localhost:8000/api/v1/analytics/dashboard/kpis
```

**Debería responder:**
```json
{
  "total_events_analyzed": 20+,
  "total_cities": 16,
  "avg_economic_impact_per_event_usd": 450000000,
  "avg_visitor_increase_pct": 35.2,
  ...
}
```

---

## 📊 ¿Datos Reales o Sintéticos?

### Estado Actual: Datos SINTÉTICOS 🎭

La aplicación actualmente usa **datos simulados realistas** porque:
- ❌ No tengo acceso a AIRROI sin API key
- ✅ Los datos simulados siguen patrones reales
- ✅ Sirven perfectamente para demostración

### 16 Ciudades Globales (con datos 2024):

**Europa 🇪🇺:**
1. **Londres** 🇬🇧 - Wimbledon, Marathon, NFL London
2. **París** 🇫🇷 - Roland Garros, Fashion Week
3. **Madrid** 🇪🇸 - Champions League, festivales
4. **Berlín** 🇩🇪 - Marathon, tech fairs
5. **Barcelona** 🇪🇸 - Mobile World Congress
6. **Amsterdam** 🇳🇱 - Dance events

**América 🌎:**
7. **Nueva York** 🇺🇸 - NYC Marathon, US Open
8. **Los Angeles** 🇺🇸 - Oscars, Grammy, Super Bowl
9. **Chicago** 🇺🇸 - Lollapalooza, Marathon
10. **Miami** 🇺🇸 - Art Basel, Ultra Music Festival
11. **Rio de Janeiro** 🇧🇷 - Carnaval, Rock in Rio
12. **São Paulo** 🇧🇷 - Formula 1, Fashion Week

**Asia-Pacífico 🌏:**
13. **Tokio** 🇯🇵 - Game Show, Marathon
14. **Singapur** 🇸🇬 - Formula 1, festivals
15. **Dubai** 🇦🇪 - Dubai Expo, events
16. **Sydney** 🇦🇺 - Sydney Festival, Mardi Gras

### Usar Datos Reales

**Para integrar AIRROI:**

1. Obtén tu API key en https://www.airroi.com/data-portal/

2. Configúrala en `.env`:
```bash
cd backend
echo "AIRROI_API_KEY=tu-api-key-aqui" >> .env
```

3. Ejecuta el importador:
```bash
python data/scripts/import_real_data.py
```

**Otras fuentes de datos disponibles:**
- 🇪🇺 Eurostat (turismo europeo)
- 🌍 World Bank (turismo global)
- 📱 Google Mobility (movilidad urbana)
- ✈️ FlightRadar24 (llegadas aéreas)

Ver `data/scripts/import_real_data.py` para más detalles.

---

## 🎯 Qué Puedes Hacer en la App

### 1. **Landing - Globo 3D** (http://localhost:3000)
- Visualización 3D del planeta con 16 pins
- Click en cualquier ciudad para ver detalles
- Stats: $12.4B impacto, 847K empleos, 420% ROI

### 2. **Dashboard** (http://localhost:3000/dashboard)
- Ver KPIs globales
- Gráficos de tendencias
- Impacto económico total
- Empleos creados

### 3. **Explorar Eventos** (http://localhost:3000/events)
- Navegar 20+ eventos principales
- Ver detalles de cada evento
- Analizar impacto individual

### 4. **About, Methodology, Case Studies** (http://localhost:3000/about)
- Misión y visión del proyecto
- Pipeline ETL y Design Thinking
- Casos reales: Rio Carnival, Paris Fashion Week, Tokyo Game Show

### 3. **Analizar Impacto** (API)
```bash
# Impacto del London Marathon
curl http://localhost:8000/api/v1/events/1/impact

# Comparar eventos
curl -X POST http://localhost:8000/api/v1/analytics/compare/events \
  -H "Content-Type: application/json" \
  -d '[1, 2, 3]'

# Comparar ciudades
curl -X POST http://localhost:8000/api/v1/analytics/compare/cities \
  -H "Content-Type: application/json" \
  -d '[1, 2, 3]'
```

### 4. **Simulador What-If** (http://localhost:3000/simulator)
```bash
# ¿Qué pasa si aumenta la asistencia 25%?
curl -X POST http://localhost:8000/api/v1/analytics/whatif/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "attendance_change_pct": 25,
    "price_elasticity": 0.3,
    "spending_multiplier": 1.1
  }'

# Proyección de crecimiento a 5 años
curl "http://localhost:8000/api/v1/analytics/whatif/growth/1?years=5&annual_growth_pct=10"
```

---

## 🔧 Comandos Útiles

**Ver logs en tiempo real:**
```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

**Reiniciar todo:**
```bash
docker-compose restart
```

**Detener todo:**
```bash
docker-compose down
```

**Limpiar y empezar de cero:**
```bash
# Detiene y elimina TODO (incluyendo la base de datos)
docker-compose down -v

# Vuelve a empezar
./start.sh
```

**Regenerar datos:**
```bash
docker-compose exec backend python /app/../data/scripts/generate_sample_data.py
```

---

## 📱 URLs Importantes

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:3000 | Dashboard interactivo |
| **API** | http://localhost:8000 | API REST |
| **API Docs (Swagger)** | http://localhost:8000/api/v1/docs | Documentación interactiva |
| **API Docs (ReDoc)** | http://localhost:8000/api/v1/redoc | Documentación alternativa |
| **Database** | localhost:5432 | PostgreSQL (evently/evently123) |

---

## ❓ Troubleshooting

### Puerto ya en uso
```bash
# Si el puerto 3000, 8000 o 5432 está ocupado:

# Ver qué está usando el puerto
lsof -i :3000
lsof -i :8000
lsof -i :5432

# Detener Docker y cambiar puertos en docker-compose.yml
docker-compose down
# Edita docker-compose.yml y cambia los puertos
docker-compose up -d
```

### Base de datos vacía
```bash
# Regenera los datos
docker-compose exec backend python /app/../data/scripts/generate_sample_data.py
```

### Frontend no carga
```bash
# Revisa logs
docker-compose logs frontend

# Reconstruye
docker-compose down
docker-compose up -d --build
```

### API no responde
```bash
# Revisa logs
docker-compose logs backend

# Verifica que la DB esté lista
docker-compose exec db psql -U evently -c "SELECT 1"

# Reinicia backend
docker-compose restart backend
```

---

## 📚 Documentación Completa

- **README.md** - Visión general del proyecto
- **SETUP.md** - Guía de instalación detallada
- **docs/TECHNICAL_DOCUMENTATION.md** - Arquitectura técnica

---

## 🎓 Próximos Pasos

1. ✅ **Explora la aplicación** - Prueba todas las funcionalidades
2. 📊 **Integra datos reales** - Conecta AIRROI u otras fuentes
3. 🎨 **Personaliza** - Añade tus propias ciudades y eventos
4. 🚀 **Despliega** - Lleva a producción con tu configuración

---

## 💡 Tips

- **Performance**: La primera carga puede tardar ~30 segundos
- **Datos**: Los datos de 2024 cubren todo el año (365 días × **16 ciudades**)
- **API**: Usa `/docs` para probar endpoints interactivamente
- **Desarrollo**: Modifica el código y se recarga automáticamente
- **Globo 3D**: Usa mouse para rotar, scroll para zoom, click en pins para info

---

**¿Problemas?** Abre un issue en GitHub o revisa los logs con `docker-compose logs -f`

**¡Disfruta analizando el impacto de eventos urbanos! 🎉**
