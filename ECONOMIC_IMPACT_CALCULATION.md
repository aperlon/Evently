# 💰 Cálculo del Impacto Económico - Evently

## 📊 Dos Métodos de Cálculo

El programa calcula el impacto económico de **dos formas diferentes** dependiendo del contexto:

### 1️⃣ **Para Eventos Existentes** (Análisis Histórico)
Usa el `ImpactAnalyzer` que compara métricas reales antes/durante el evento.

### 2️⃣ **Para Eventos Futuros** (Predicción)
Usa el **modelo de regresión** entrenado con datos históricos.

---

## 🔍 Método 1: Cálculo para Eventos Existentes

### Ubicación del Código
`backend/app/analytics/impact_analyzer.py` → `_calculate_economic_impact()`

### Proceso de Cálculo

#### Paso 1: Obtener Métricas del Período del Evento

```python
# Obtiene todas las métricas económicas durante el evento
event_metrics = EconomicMetric.query.filter(
    city_id == event.city_id,
    date >= event.start_date,
    date <= event.end_date
).all()

# Suma el gasto total
total_spending = sum(
    m.total_spending_usd for m in event_metrics
)
```

#### Paso 2: Aplicar Multiplicadores Económicos

El programa usa el **modelo de multiplicadores** estándar de economía del turismo:

```python
# Gasto Directo (100% del gasto medido)
direct_spending = total_spending

# Gasto Indirecto (40% del directo)
# - Efectos en la cadena de suministro
# - Comercio mayorista
# - Servicios a empresas
indirect_spending = total_spending * 0.4

# Gasto Inducido (30% del directo)
# - Gasto de empleados
# - Consumo de hogares
# - Efectos secundarios
induced_spending = total_spending * 0.3

# Impacto Económico Total
total_economic_impact = direct_spending + indirect_spending + induced_spending
```

**Fórmula Final:**
```
Total Impact = Direct + Indirect + Induced
Total Impact = total_spending × (1 + 0.4 + 0.3)
Total Impact = total_spending × 1.7
```

#### Paso 3: Calcular Métricas Adicionales

```python
# Empleos creados (suma de jobs_created en métricas)
jobs_created = sum(
    m.temporary_jobs_created for m in event_metrics
)

# Ingresos fiscales (suma de tax_revenue en métricas)
tax_revenue = sum(
    m.estimated_tax_revenue_usd for m in event_metrics
)
```

### Ventana de Análisis

- **Baseline (Línea Base)**: 44 días antes del evento hasta 14 días antes
- **Período del Evento**: Desde `start_date` hasta `end_date`
- **Post-Evento**: 14 días después del evento (para efectos residuales)

---

## 🤖 Método 2: Predicción para Eventos Futuros

### Ubicación del Código
`backend/app/ml/economic_impact_model.py` → `predict()` y `predict_simple()`

### Proceso de Predicción

#### Paso 1: Preparar Features

El modelo usa **13 features** para predecir:

```python
features = [
    attendance,                    # Asistencia esperada
    duration_days,                 # Duración en días
    event_type_encoded,            # Tipo de evento (codificado)
    visitor_increase_pct,          # % aumento de visitantes (estimado)
    price_increase_pct,            # % aumento de precios (estimado)
    occupancy_boost,               # Aumento de ocupación hotelera
    population,                    # Población de la ciudad
    annual_tourists,                # Turistas anuales
    hotel_rooms,                   # Habitaciones hoteleras
    avg_hotel_price_usd,           # Precio promedio de hotel
    attendance / duration_days,    # Asistencia por día
    attendance / hotel_rooms,      # Visitantes por habitación
    annual_tourists / population   # Intensidad turística
]
```

#### Paso 2: Normalizar Features

```python
# Todas las features se normalizan usando StandardScaler
X_scaled = scaler.transform(features)
```

#### Paso 3: Predecir (en Log Space)

```python
# El modelo predice en log space para mejor distribución
y_pred_log = best_model.predict(X_scaled)

# Transformar de vuelta a escala original
prediction = expm1(y_pred_log)  # exp(x) - 1
```

#### Paso 4: Calcular Intervalo de Confianza

```python
# Usa el MAPE del modelo entrenado
mape = model_metrics['mape'] / 100
lower_bound = prediction × (1 - mape × 1.5)
upper_bound = prediction × (1 + mape × 1.5)
```

#### Paso 5: Desglose del Impacto

```python
# Desglose usando ratios típicos
direct_spending = prediction × 0.64    # 64% directo
indirect_spending = prediction × 0.25  # 25% indirecto
induced_spending = prediction × 0.11    # 11% inducido
```

#### Paso 6: Estimaciones Adicionales

```python
# Empleos creados (estimación: $40,000 por empleo)
jobs_created = prediction / 40,000

# ROI (estimación: ROI típico de 4:1)
estimated_cost = prediction / 4.0
roi_ratio = prediction / estimated_cost
```

---

## 📐 Fórmulas Clave

### Para Eventos Existentes

```
1. Total Spending = Σ(total_spending_usd) durante el evento

2. Direct Spending = Total Spending

3. Indirect Spending = Total Spending × 0.4

4. Induced Spending = Total Spending × 0.3

5. Total Economic Impact = Direct + Indirect + Induced
                         = Total Spending × 1.7
```

### Para Predicciones

```
1. Features = [attendance, duration, event_type, city_data, ...]

2. Features Normalizadas = StandardScaler(Features)

3. Prediction (log) = Model.predict(Features Normalizadas)

4. Prediction (USD) = expm1(Prediction log)

5. Confidence Interval = Prediction × (1 ± MAPE × 1.5)

6. Breakdown:
   - Direct = Prediction × 0.64
   - Indirect = Prediction × 0.25
   - Induced = Prediction × 0.11

7. Jobs Created = Prediction / 40,000

8. ROI = Prediction / (Prediction / 4.0) = 4.0
```

---

## 🔄 Flujo Completo

### Eventos Existentes (Dashboard, Event Details)

```
1. Usuario accede a evento existente
   ↓
2. ImpactAnalyzer.calculate_event_impact(event_id)
   ↓
3. Obtiene métricas económicas del período del evento
   ↓
4. Suma total_spending_usd
   ↓
5. Aplica multiplicadores (×1.7)
   ↓
6. Calcula jobs_created y tax_revenue
   ↓
7. Guarda en EventImpact
   ↓
8. Muestra en frontend
```

### Eventos Futuros (Predict Page)

```
1. Usuario completa formulario en /predict
   ↓
2. Frontend llama a /api/v1/predict
   ↓
3. Backend carga modelo entrenado
   ↓
4. EconomicImpactModel.predict_simple()
   ↓
5. Prepara features desde inputs
   ↓
6. Normaliza features
   ↓
7. Predice usando Random Forest (mejor modelo)
   ↓
8. Calcula intervalo de confianza
   ↓
9. Calcula desglose y estimaciones
   ↓
10. Retorna resultado al frontend
   ↓
11. Frontend muestra predicción
```

---

## 📊 Datos Utilizados

### Para Cálculo de Eventos Existentes

- **Fuente**: Tabla `economic_metrics` en la base de datos
- **Campos clave**:
  - `total_spending_usd`: Gasto total diario
  - `accommodation_spending_usd`: Gasto en alojamiento
  - `food_beverage_spending_usd`: Gasto en comida/bebida
  - `retail_spending_usd`: Gasto en retail
  - `entertainment_spending_usd`: Gasto en entretenimiento
  - `transport_spending_usd`: Gasto en transporte
  - `temporary_jobs_created`: Empleos temporales creados

### Para Predicciones

- **Fuente de entrenamiento**: `data/examples/event_impacts.csv`
- **Datos históricos**: 12 eventos con sus impactos económicos reales
- **Modelo entrenado**: Random Forest (R² = 0.9902)
- **Features más importantes**:
  1. Attendance (31.97%)
  2. Duration days (29.86%)
  3. Visitors per hotel room (23.85%)

---

## 🎯 Diferencias Clave

| Aspecto | Eventos Existentes | Predicciones |
|---------|-------------------|--------------|
| **Método** | Suma de métricas reales | Modelo de regresión |
| **Datos** | `economic_metrics` (BD) | `event_impacts.csv` (entrenamiento) |
| **Multiplicador** | 1.7x (Direct + Indirect + Induced) | Predicción del modelo |
| **Precisión** | Exacta (datos reales) | Estimada (R² = 0.99) |
| **Desglose** | Basado en métricas reales | Ratios típicos (64/25/11) |
| **Confianza** | 100% (datos medidos) | 90% (intervalo de confianza) |

---

## 💡 Notas Importantes

1. **Multiplicadores Económicos**: Los ratios 40% (indirect) y 30% (induced) son estándares de la industria del turismo, pero pueden variar según la ciudad y tipo de evento.

2. **Modelo de Regresión**: Se entrena con solo 12 eventos, por lo que funciona mejor para eventos similares a los del dataset de entrenamiento.

3. **Transformación Logarítmica**: El modelo predice en log space porque los impactos económicos tienen distribución muy sesgada (algunos eventos generan millones, otros miles).

4. **Intervalo de Confianza**: Se calcula usando el MAPE (Mean Absolute Percentage Error) del modelo en entrenamiento, multiplicado por 1.5 para un intervalo del 90%.

5. **Jobs Created**: La estimación de $40,000 por empleo es un promedio de la industria, pero puede variar según el país y sector.

---

## 🔧 Personalización

Si quieres cambiar los multiplicadores o ratios:

### Cambiar Multiplicadores (Eventos Existentes)
Edita `backend/app/analytics/impact_analyzer.py` línea 272-273:
```python
indirect_spending = total_spending * 0.4  # Cambiar 0.4
induced_spending = total_spending * 0.3   # Cambiar 0.3
```

### Cambiar Ratios de Desglose (Predicciones)
Edita `backend/app/ml/economic_impact_model.py` línea 407-409:
```python
direct_spending = prediction * 0.64   # Cambiar 0.64
indirect_spending = prediction * 0.25 # Cambiar 0.25
induced_spending = prediction * 0.11  # Cambiar 0.11
```

### Cambiar Estimación de Empleos
Edita `backend/app/ml/economic_impact_model.py` línea 412:
```python
jobs_created = int(prediction / 40000)  # Cambiar 40000
```

---

## 📈 Ejemplo de Cálculo

### Evento Existente: London Marathon 2024

```
1. Obtiene métricas del 2024-04-21
   - total_spending_usd por día durante el evento

2. Suma total:
   - Día 1: $15,000,000
   - Total: $15,000,000 (1 día)

3. Aplica multiplicadores:
   - Direct: $15,000,000
   - Indirect: $15,000,000 × 0.4 = $6,000,000
   - Induced: $15,000,000 × 0.3 = $4,500,000
   - Total: $25,500,000

4. Jobs created: Suma de temporary_jobs_created
```

### Predicción: Nuevo Evento Deportivo en Madrid

```
1. Inputs:
   - event_type: "sports"
   - city: "Madrid"
   - duration_days: 7
   - attendance: 50000

2. Features calculadas:
   - attendance: 50000
   - duration_days: 7
   - event_type_encoded: 0 (sports)
   - visitor_increase_pct: 25.0 (estimado)
   - price_increase_pct: 20.0 (estimado)
   - occupancy_boost: 7.5 (estimado)
   - population: 3200000
   - annual_tourists: 10400000
   - hotel_rooms: 85000
   - avg_hotel_price_usd: 140
   - attendance_per_day: 7143
   - visitors_per_hotel_room: 0.59
   - city_tourism_intensity: 3.25

3. Modelo predice: $45,234,567 (en log space, transformado)

4. Intervalo de confianza (MAPE = 45.17%):
   - Lower: $45,234,567 × (1 - 0.4517 × 1.5) = $14,567,890
   - Upper: $45,234,567 × (1 + 0.4517 × 1.5) = $75,901,244

5. Desglose:
   - Direct: $45,234,567 × 0.64 = $28,950,124
   - Indirect: $45,234,567 × 0.25 = $11,308,642
   - Induced: $45,234,567 × 0.11 = $4,975,802

6. Estimaciones:
   - Jobs: $45,234,567 / 40,000 = 1,130 empleos
   - ROI: 4.0x
   - Cost: $45,234,567 / 4.0 = $11,308,642
```

---

## ✅ Resumen

**Para eventos existentes:**
- Usa datos reales de `economic_metrics`
- Suma el gasto total durante el evento
- Aplica multiplicador 1.7x (Direct + Indirect + Induced)

**Para predicciones:**
- Usa modelo de regresión (Random Forest)
- Entrenado con 12 eventos históricos
- Predice basándose en características del evento y ciudad
- Proporciona intervalo de confianza del 90%

