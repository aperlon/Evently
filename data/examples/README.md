# 📊 CSV Examples - Evently Data Format

Este directorio contiene CSVs de ejemplo con el formato exacto que usa Evently para analizar eventos.

## 📁 Archivos Disponibles

### 1. `cities.csv` - Ciudades Base
**16 ciudades** con sus características base.

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `name` | Nombre de la ciudad | London |
| `country` | País | United Kingdom |
| `country_code` | Código ISO 3 | GBR |
| `continent` | Continente | Europe |
| `latitude` | Latitud | 51.5074 |
| `longitude` | Longitud | -0.1278 |
| `timezone` | Zona horaria | Europe/London |
| `population` | Población | 9000000 |
| `area_km2` | Área en km² | 1572 |
| `gdp_usd` | PIB en USD | 635000000000 |
| `annual_tourists` | Turistas anuales | 19600000 |
| `hotel_rooms` | Habitaciones hoteleras | 150000 |
| `avg_hotel_price_usd` | Precio promedio hotel (USD) | 180 |

---

### 2. `events.csv` - Eventos Principales
**34 eventos** de 2022-2024 con datos completos.

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `event_name` | Nombre del evento | Wimbledon 2024 |
| `city` | Ciudad sede | London |
| `event_type` | Tipo (sports/music/culture/festival/business/fair) | sports |
| `description` | Descripción | Tennis Grand Slam... |
| `start_date` | Fecha inicio (YYYY-MM-DD) | 2024-07-01 |
| `end_date` | Fecha fin | 2024-07-14 |
| `year` | Año | 2024 |
| `expected_attendance` | Asistencia esperada | 500000 |
| `actual_attendance` | Asistencia real | 526455 |
| `venue_name` | Nombre del venue | All England Club |
| `venue_capacity` | Capacidad | 42000 |
| `is_recurring` | ¿Recurrente? (1/0) | 1 |
| `recurrence_pattern` | Patrón (annual/biannual) | annual |
| `edition_number` | Número de edición | 137 |
| `economic_impact_usd` | Impacto económico (USD) | 499000000 |

**Eventos incluidos:**
- 🎾 Wimbledon (2022-2024)
- 🏃 London Marathon (2022-2024)
- 🎾 Roland Garros (2023-2024)
- 👗 Paris Fashion Week (2023-2024)
- 🎾 US Open (2023-2024)
- 🏃 NYC Marathon (2023-2024)
- ⚽ Champions League Finals (2022-2024)
- 🎵 Mad Cool Festival (2023-2024)
- 🏃 Berlin Marathon (2023-2024)
- 💡 Berlin Festival of Lights (2024)
- 🎭 Rio Carnival (2023-2024)
- 🏎️ São Paulo F1 (2023-2024)
- 🏎️ Singapore F1 (2024)
- 🏃 Tokyo Marathon (2024)
- 🎮 Tokyo Game Show (2024)
- 🌍 Dubai Expo (2024)
- 🎨 Sydney Festival (2024)
- 🎵 Amsterdam Dance Event (2024)
- 📱 MWC Barcelona (2024)

---

### 3. `tourism_metrics.csv` - Métricas de Turismo (Diarias)
**55 registros** - métricas diarias durante eventos.

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `city` | Ciudad | London |
| `date` | Fecha (YYYY-MM-DD) | 2024-07-01 |
| `total_visitors` | Visitantes totales | 85000 |
| `domestic_visitors` | Visitantes nacionales | 42500 |
| `international_visitors` | Visitantes internacionales | 42500 |
| `avg_stay_duration_days` | Duración media estancia | 4.5 |
| `avg_spending_per_visitor_usd` | Gasto medio por visitante | 380 |
| `event_visitors_pct` | % visitantes por el evento | 45 |
| `notes` | Notas | Wimbledon Day 1 |

---

### 4. `hotel_metrics.csv` - Métricas Hoteleras (Diarias)
**48 registros** - ocupación y precios durante eventos.

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `city` | Ciudad | London |
| `date` | Fecha | 2024-07-01 |
| `occupancy_rate_pct` | Tasa ocupación (%) | 89.5 |
| `avg_price_usd` | Precio promedio (USD) | 285 |
| `median_price_usd` | Precio mediana | 250 |
| `min_price_usd` | Precio mínimo | 120 |
| `max_price_usd` | Precio máximo | 850 |
| `revpar_usd` | Revenue Per Available Room | 255 |
| `available_rooms` | Habitaciones disponibles | 150000 |
| `occupied_rooms` | Habitaciones ocupadas | 134250 |
| `luxury_occupancy_pct` | Ocupación hoteles lujo | 95 |
| `midscale_occupancy_pct` | Ocupación hoteles medios | 88 |
| `budget_occupancy_pct` | Ocupación hoteles económicos | 85 |
| `notes` | Notas | Wimbledon Day 1 |

---

### 5. `economic_metrics.csv` - Métricas Económicas (Diarias)
**30 registros** - gasto y empleo durante eventos.

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `city` | Ciudad | London |
| `date` | Fecha | 2024-07-01 |
| `total_spending_usd` | Gasto total (USD) | 32500000 |
| `accommodation_spending_usd` | Gasto en alojamiento | 13000000 |
| `food_beverage_spending_usd` | Gasto en comida/bebida | 8125000 |
| `retail_spending_usd` | Gasto en retail | 6500000 |
| `entertainment_spending_usd` | Gasto en entretenimiento | 3250000 |
| `transport_spending_usd` | Gasto en transporte | 1625000 |
| `temporary_jobs_created` | Empleos temporales | 850 |
| `estimated_tax_revenue_usd` | Recaudación fiscal | 3250000 |
| `notes` | Notas | Wimbledon Day 1 |

---

### 6. `mobility_metrics.csv` - Métricas de Movilidad (Diarias)
**32 registros** - transporte durante eventos.

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `city` | Ciudad | London |
| `date` | Fecha | 2024-07-01 |
| `airport_arrivals` | Llegadas aeropuerto | 52000 |
| `airport_departures` | Salidas aeropuerto | 38000 |
| `international_flights` | Vuelos internacionales | 285 |
| `domestic_flights` | Vuelos domésticos | 180 |
| `train_arrivals` | Llegadas en tren | 45000 |
| `public_transport_usage` | Uso transporte público | 3850000 |
| `taxi_rides` | Viajes en taxi | 95000 |
| `traffic_congestion_index` | Índice congestión (1-10) | 7.8 |
| `notes` | Notas | Wimbledon Day 1 |

---

### 7. `event_impacts.csv` - Impacto por Evento (Agregado) ⭐
**27 eventos** con análisis de impacto completo. **Este es el CSV más importante para ML.**

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `event_name` | Nombre del evento | Wimbledon 2024 |
| `year` | Año | 2024 |
| `city` | Ciudad | London |
| `baseline_daily_visitors` | Visitantes diarios baseline | 55000 |
| `event_daily_visitors` | Visitantes diarios durante evento | 98000 |
| `visitor_increase_pct` | % incremento visitantes | 78.2 |
| `additional_visitors` | Visitantes adicionales totales | 602000 |
| `baseline_occupancy_pct` | Ocupación baseline (%) | 72.5 |
| `event_occupancy_pct` | Ocupación durante evento | 94.8 |
| `occupancy_increase_pct` | % incremento ocupación | 30.8 |
| `baseline_avg_price_usd` | Precio hotel baseline | 180 |
| `event_avg_price_usd` | Precio hotel durante evento | 342 |
| `price_increase_pct` | % incremento precio | 90.0 |
| `total_economic_impact_usd` | Impacto económico TOTAL | 499000000 |
| `direct_spending_usd` | Gasto directo | 320000000 |
| `indirect_spending_usd` | Impacto indirecto (cadena suministro) | 128000000 |
| `induced_spending_usd` | Impacto inducido (empleados) | 51000000 |
| `jobs_created` | Empleos creados | 12500 |
| `tax_revenue_usd` | Recaudación fiscal | 45000000 |
| `roi_ratio` | ROI (Return on Investment) | 4.2 |
| `event_cost_usd` | Coste del evento | 119000000 |

---

## 🔄 Cómo Importar Tus Datos

### Opción 1: Reemplazar CSVs de ejemplo
```bash
# Copia tu CSV con el mismo nombre y columnas
cp tu_archivo.csv data/examples/events.csv

# Ejecuta la importación
python data/scripts/import_csv_to_db.py
```

### Opción 2: Agregar nuevos datos
```python
import pandas as pd

# Lee el CSV existente
df = pd.read_csv('data/examples/events.csv')

# Añade tus nuevos eventos
new_event = {
    'event_name': 'Tu Evento 2025',
    'city': 'Madrid',
    # ... demás columnas
}
df = df.append(new_event, ignore_index=True)

# Guarda
df.to_csv('data/examples/events.csv', index=False)
```

---

## 📈 Variables Clave para ML

**Para entrenar los modelos, las columnas más importantes son:**

### Tourism Predictor:
- `date`, `total_visitors`, `international_visitors`

### Hotel Price Predictor:
- `occupancy_rate_pct`, `avg_price_usd`, `event_visitors_pct`

### Impact Predictor:
- `actual_attendance`, `duration_days`, `event_type`
- `total_economic_impact_usd` (target)

---

## 📞 Soporte

Si tienes datos reales que quieres integrar, asegúrate de que:
1. ✅ Las fechas están en formato `YYYY-MM-DD`
2. ✅ Los valores monetarios están en USD
3. ✅ Los porcentajes son números (85.5 no "85.5%")
4. ✅ Los nombres de ciudades coinciden con `cities.csv`

---

**Última actualización:** 2025-11-21
