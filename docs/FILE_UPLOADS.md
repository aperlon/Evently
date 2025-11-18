# 📁 File Uploads - Importar Datos desde CSV/XLSX

Guía completa para subir datos desde archivos CSV o Excel en lugar de usar APIs externas.

---

## 🎯 ¿Por Qué Usar File Uploads?

**Ventajas sobre APIs:**
- ✅ **No depende de APIs externas** (sin API keys, sin límites)
- ✅ **Datos propios**: Sube tus propios datasets
- ✅ **Datos históricos**: Importa años de datos de una vez
- ✅ **Flexible**: Cualquier fuente de datos (Excel, CSV)
- ✅ **Rápido**: Miles de registros en segundos
- ✅ **Offline**: No necesitas internet

---

## 📋 Tipos de Archivos Soportados

| Tipo | Extensión | Notas |
|------|-----------|-------|
| CSV | `.csv` | Separado por comas |
| Excel | `.xlsx` | Formato moderno de Excel |

---

## 🚀 Endpoints Disponibles

### 1. **Subir Ciudades**

**Endpoint:**
```
POST /api/v1/upload/cities
```

**Body:** `multipart/form-data` con archivo

**Columnas requeridas:**
- `name` - Nombre de la ciudad
- `country` - País
- `country_code` - Código ISO (ESP, FRA, USA, etc.)
- `continent` - Continente (Europe, Asia, etc.)
- `latitude` - Latitud
- `longitude` - Longitud
- `timezone` - Timezone (Europe/Madrid, etc.)

**Columnas opcionales:**
- `population` - Población
- `annual_tourists` - Turistas anuales
- `hotel_rooms` - Habitaciones de hotel
- `avg_hotel_price_usd` - Precio promedio hotel (USD)

**Ejemplo CSV:**
```csv
name,country,country_code,continent,latitude,longitude,timezone,population,annual_tourists,hotel_rooms,avg_hotel_price_usd
Barcelona,Spain,ESP,Europe,41.3874,2.1686,Europe/Madrid,1620000,9000000,70000,150
Amsterdam,Netherlands,NLD,Europe,52.3676,4.9041,Europe/Amsterdam,872680,8700000,35000,180
Dubai,UAE,ARE,Asia,25.2048,55.2708,Asia/Dubai,3400000,16700000,120000,200
```

**Con cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/upload/cities \
  -F "file=@cities.csv"
```

**Respuesta:**
```json
{
  "message": "Cities imported successfully",
  "cities_created": 3,
  "cities_skipped": 0,
  "total_rows": 3
}
```

---

### 2. **Subir Eventos**

**Endpoint:**
```
POST /api/v1/upload/events
```

**Columnas requeridas:**
- `name` - Nombre del evento
- `city_name` - Nombre de la ciudad (debe existir)
- `event_type` - Tipo: `sports`, `music`, `culture`, `business`, `fair`, `festival`
- `start_date` - Fecha inicio (YYYY-MM-DD)
- `end_date` - Fecha fin (YYYY-MM-DD)

**Columnas opcionales:**
- `expected_attendance` - Asistencia esperada
- `actual_attendance` - Asistencia real
- `venue_name` - Nombre del venue
- `description` - Descripción del evento
- `is_recurring` - Si es recurrente (true/false)

**Ejemplo CSV:**
```csv
name,city_name,event_type,start_date,end_date,expected_attendance,actual_attendance,venue_name,description
Formula 1 Barcelona,Barcelona,sports,2024-06-21,2024-06-23,200000,195000,Circuit de Barcelona-Catalunya,F1 Grand Prix
Primavera Sound,Barcelona,music,2024-05-30,2024-06-01,200000,220000,Parc del Fòrum,Music Festival
ADE Amsterdam,Amsterdam,music,2024-10-16,2024-10-20,400000,450000,Various venues,Amsterdam Dance Event
Dubai Shopping Festival,Dubai,fair,2024-01-12,2024-02-12,4000000,4500000,Various malls,Shopping and entertainment
```

**Con Python:**
```python
import requests

files = {'file': open('events.csv', 'rb')}
response = requests.post('http://localhost:8000/api/v1/upload/events', files=files)
print(response.json())
```

---

### 3. **Subir Métricas de Hoteles**

**Endpoint:**
```
POST /api/v1/upload/hotel-metrics
```

**Columnas requeridas:**
- `city_name` - Nombre de la ciudad
- `date` - Fecha (YYYY-MM-DD)

**Columnas opcionales:**
- `occupancy_rate_pct` - Tasa de ocupación (0-100)
- `avg_price_usd` - Precio promedio (USD)
- `median_price_usd` - Precio mediano (USD)
- `available_rooms` - Habitaciones disponibles
- `occupied_rooms` - Habitaciones ocupadas

**Ejemplo CSV:**
```csv
city_name,date,occupancy_rate_pct,avg_price_usd,median_price_usd,available_rooms,occupied_rooms
Barcelona,2024-06-21,95.5,280.00,250.00,70000,66850
Barcelona,2024-06-22,97.2,295.00,270.00,70000,68040
Barcelona,2024-06-23,92.8,275.00,245.00,70000,64960
Amsterdam,2024-10-16,89.3,220.00,200.00,35000,31255
Amsterdam,2024-10-17,91.5,235.00,215.00,35000,32025
```

**Con JavaScript:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/v1/upload/hotel-metrics', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 4. **Subir Métricas de Turismo**

**Endpoint:**
```
POST /api/v1/upload/tourism-metrics
```

**Columnas requeridas:**
- `city_name` - Nombre de la ciudad
- `date` - Fecha (YYYY-MM-DD)

**Columnas opcionales:**
- `total_visitors` - Total de visitantes
- `international_visitors` - Visitantes internacionales
- `domestic_visitors` - Visitantes domésticos
- `avg_spending_per_visitor_usd` - Gasto promedio por visitante

**Ejemplo CSV:**
```csv
city_name,date,total_visitors,international_visitors,domestic_visitors,avg_spending_per_visitor_usd
Barcelona,2024-06-21,180000,140000,40000,350.00
Barcelona,2024-06-22,195000,150000,45000,375.00
Barcelona,2024-06-23,170000,130000,40000,340.00
```

---

## 📥 Descargar Templates

**La API proporciona templates para facilitar el formato:**

### Template de Ciudades:
```bash
GET /api/v1/templates/cities
```

### Template de Eventos:
```bash
GET /api/v1/templates/events
```

### Template de Métricas Hoteleras:
```bash
GET /api/v1/templates/hotel-metrics
```

**Usar desde navegador:**
```
http://localhost:8000/api/v1/templates/cities
```

---

## 🔄 Workflow Completo

### **1. Preparar tus datos en Excel:**

Descarga datos de:
- **Booking.com** (exportar precios históricos)
- **Instituto Nacional de Estadística** (turismo)
- **Airbnb Data** (ocupación)
- **Tu propia base de datos**

### **2. Formatear según templates:**

```
1. Descarga template: GET /api/v1/templates/cities
2. Abre en Excel
3. Pega tus datos
4. Guarda como CSV o XLSX
```

### **3. Subir archivo:**

**Opción A: Desde Postman/Insomnia:**
```
POST /api/v1/upload/cities
Body: form-data
Key: file
Value: [seleccionar archivo]
```

**Opción B: Desde código:**
```python
import requests

files = {'file': open('mis_datos.csv', 'rb')}
response = requests.post(
    'http://localhost:8000/api/v1/upload/cities',
    files=files
)
print(response.json())
```

**Opción C: Desde frontend (React):**
```typescript
const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
  const file = event.target.files?.[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://localhost:8000/api/v1/upload/cities', {
    method: 'POST',
    body: formData,
  });

  const result = await response.json();
  console.log(result);
};
```

### **4. Verificar datos importados:**

```bash
# Ver ciudades importadas
curl http://localhost:8000/api/v1/cities

# Ver eventos importados
curl http://localhost:8000/api/v1/events

# Ver métricas
curl "http://localhost:8000/api/v1/analytics/timeseries/1?metric_type=hotel&start_date=2024-01-01&end_date=2024-12-31"
```

---

## 💡 Casos de Uso Reales

### **Caso 1: Datos de Booking.com**

Si tienes acceso a datos históricos de Booking.com:

```
1. Exporta datos de precios y ocupación → CSV
2. Formatea según template hotel-metrics
3. Sube: POST /api/v1/upload/hotel-metrics
4. ¡Listo! Ya tienes datos reales
```

### **Caso 2: Datos del INE (Instituto Nacional Estadística)**

```
1. Descarga datos de turismo del INE
2. Limpia y formatea en Excel
3. Guarda como CSV
4. Sube: POST /api/v1/upload/tourism-metrics
```

### **Caso 3: Datos de tu Cliente (Hotel)**

Si un hotel te da sus datos:

```csv
fecha,ocupacion,precio_promedio,habitaciones_totales
2024-06-21,95.5,280,150
2024-06-22,97.2,295,150
```

Transforma a formato Evently:
```csv
city_name,date,occupancy_rate_pct,avg_price_usd,available_rooms
Barcelona,2024-06-21,95.5,280,150
Barcelona,2024-06-22,97.2,295,150
```

Sube y analiza.

---

## ⚠️ Validaciones y Errores

### **Errores Comunes:**

**1. Ciudad no existe:**
```json
{
  "errors": ["Row 2: City 'Barcelonaa' not found"]
}
```
**Solución:** Sube primero las ciudades

**2. Formato de fecha incorrecto:**
```json
{
  "errors": ["Row 5: Invalid date format"]
}
```
**Solución:** Usa formato YYYY-MM-DD

**3. Columnas faltantes:**
```json
{
  "detail": "Missing required columns: latitude, longitude"
}
```
**Solución:** Revisa el template

**4. Tipo de evento inválido:**
```json
{
  "errors": ["Row 3: Invalid event_type 'concert'"]
}
```
**Solución:** Usa solo: sports, music, culture, business, fair, festival

---

## 🔍 Debugging

### **Ver qué se importó:**

```python
import pandas as pd
import requests

# Upload
files = {'file': open('events.csv', 'rb')}
response = requests.post('http://localhost:8000/api/v1/upload/events', files=files)
result = response.json()

print(f"Creados: {result['events_created']}")
print(f"Errores: {result.get('errors', [])}")

# Verificar
events = requests.get('http://localhost:8000/api/v1/events').json()
df = pd.DataFrame(events)
print(df.head())
```

---

## 📊 Después de Subir Datos

### **Analizar impacto:**

```bash
# 1. Sube ciudades
curl -X POST -F "file=@cities.csv" http://localhost:8000/api/v1/upload/cities

# 2. Sube eventos
curl -X POST -F "file=@events.csv" http://localhost:8000/api/v1/upload/events

# 3. Sube métricas hoteleras
curl -X POST -F "file=@hotel_metrics.csv" http://localhost:8000/api/v1/upload/hotel-metrics

# 4. Analiza impacto del primer evento
curl http://localhost:8000/api/v1/events/1/impact

# 5. Compara eventos
curl -X POST http://localhost:8000/api/v1/analytics/compare/events \
  -H "Content-Type: application/json" \
  -d '[1,2,3]'
```

---

## 🎨 Integración con Frontend

Crea un componente de upload:

```typescript
// UploadPage.tsx
import { useState } from 'react';

function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState(null);

  const handleUpload = async (type: string) => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(
      `http://localhost:8000/api/v1/upload/${type}`,
      {
        method: 'POST',
        body: formData,
      }
    );

    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="card">
      <h2>Subir Datos</h2>

      <input
        type="file"
        accept=".csv,.xlsx"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <div className="button-group">
        <button onClick={() => handleUpload('cities')}>
          Subir Ciudades
        </button>
        <button onClick={() => handleUpload('events')}>
          Subir Eventos
        </button>
        <button onClick={() => handleUpload('hotel-metrics')}>
          Subir Métricas Hoteleras
        </button>
      </div>

      {result && (
        <div className="result">
          <h3>Resultado:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

---

## 📈 Performance

**Benchmarks:**
- ✅ 1,000 registros: ~2 segundos
- ✅ 10,000 registros: ~15 segundos
- ✅ 100,000 registros: ~2 minutos

**Tips para archivos grandes:**
- Divide en múltiples archivos
- Usa CSV en lugar de XLSX (más rápido)
- Procesa en batch de 10,000 registros

---

## 🔐 Seguridad

**Validaciones incluidas:**
- ✅ Solo archivos CSV/XLSX
- ✅ Validación de columnas requeridas
- ✅ Validación de tipos de datos
- ✅ Validación de fechas
- ✅ Evita duplicados (ciudades por nombre)
- ✅ Rollback en caso de error

---

## 🎯 Siguiente Paso

**Crea tu primer upload:**

1. Descarga template:
   ```
   http://localhost:8000/api/v1/templates/cities
   ```

2. Edita con tus datos

3. Sube:
   ```bash
   curl -X POST -F "file=@mi_archivo.csv" \
     http://localhost:8000/api/v1/upload/cities
   ```

4. ¡Analiza!

---

**¿Preguntas?** Revisa los ejemplos o prueba los endpoints en `/api/v1/docs`
