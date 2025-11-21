# 🎯 Economic Impact Regression Model

## Descripción

El modelo de regresión predice el **impacto económico total** de eventos basándose en características del evento y de la ciudad sede.

## Métricas del Modelo Actual

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| **Modelo** | Random Forest | 100 árboles, profundidad 10 |
| **R² Score** | 0.6529 | 65% de varianza explicada |
| **MAPE** | 22.25% | Error porcentual promedio |
| **MAE** | $84M | Error absoluto promedio |
| **RMSE** | $95M | Raíz del error cuadrático medio |
| **Samples** | 27 eventos | Dataset de entrenamiento |

## Variables del Modelo

### Features de Entrada (13 variables)

**Características del Evento:**
```
attendance              # Asistencia total esperada
duration_days           # Duración en días
event_type_encoded      # Tipo: sports=1, music=2, culture=3, etc.
visitor_increase_pct    # % incremento visitantes vs baseline
price_increase_pct      # % incremento precio hoteles vs baseline
occupancy_boost         # Incremento ocupación hotelera (puntos %)
```

**Características de la Ciudad:**
```
population              # Población de la ciudad
annual_tourists         # Turistas anuales
hotel_rooms             # Habitaciones hoteleras disponibles
avg_hotel_price_usd     # Precio promedio hotel (baseline)
```

**Features Derivadas (calculadas automáticamente):**
```
attendance_per_day      # attendance / duration_days
visitors_per_hotel_room # attendance / hotel_rooms
city_tourism_intensity  # annual_tourists / population
```

### Variable de Salida (Target)
```
total_economic_impact_usd  # Impacto económico total en USD
```

### Feature Importance

| Rank | Feature | Importancia |
|------|---------|-------------|
| 1 | `price_increase_pct` | **33.2%** |
| 2 | `duration_days` | 16.3% |
| 3 | `attendance` | 10.3% |
| 4 | `attendance_per_day` | 9.4% |
| 5 | `visitors_per_hotel_room` | 8.5% |
| 6 | `avg_hotel_price_usd` | 5.5% |
| 7 | `event_type_encoded` | 5.2% |
| 8 | `city_tourism_intensity` | 3.3% |
| 9 | `visitor_increase_pct` | 3.1% |
| 10 | `occupancy_boost` | 2.4% |

## Uso del Modelo

### 1. Entrenar el Modelo

```bash
# Desde la raíz del proyecto
python data/scripts/train_economic_model.py
```

Esto:
1. Lee datos de `data/examples/*.csv`
2. Entrena 5 modelos diferentes
3. Selecciona el mejor (Random Forest)
4. Guarda en `backend/app/ml/saved_models/`

### 2. Usar el Modelo en Python

```python
from app.ml.economic_impact_model import EconomicImpactModel

# Cargar modelo entrenado
model = EconomicImpactModel()
model.load()

# Predecir para un nuevo evento
resultado = model.predict({
    'event_type': 'sports',
    'city': 'London',
    'attendance': 500000,
    'duration_days': 14,
})

print(f"Impacto: ${resultado['prediction']['total_economic_impact_usd']:,.0f}")
print(f"Intervalo: ${resultado['prediction']['lower_bound_usd']:,.0f} - ${resultado['prediction']['upper_bound_usd']:,.0f}")
print(f"Empleos: {resultado['estimates']['jobs_created']:,}")
print(f"ROI: {resultado['estimates']['roi_ratio']}x")
```

### 3. Ejemplo de Output

```python
{
    'prediction': {
        'total_economic_impact_usd': 356740485,
        'lower_bound_usd': 237692678,
        'upper_bound_usd': 475788292,
        'confidence_level': '90%'
    },
    'breakdown': {
        'direct_spending_usd': 228313910,
        'indirect_spending_usd': 89185121,
        'induced_spending_usd': 39241453
    },
    'estimates': {
        'jobs_created': 8918,
        'roi_ratio': 4.0,
        'estimated_event_cost_usd': 89185121
    },
    'model_info': {
        'model_used': 'random_forest',
        'model_r2': 0.6529,
        'model_mape': 22.25
    }
}
```

## Actualizar con Datos Reales

Cuando tengas datos reales, simplemente:

### 1. Reemplaza los CSVs
```bash
# Actualiza estos archivos con datos reales:
data/examples/events.csv
data/examples/cities.csv
data/examples/event_impacts.csv
```

### 2. Reentrena el modelo
```bash
python data/scripts/train_economic_model.py
```

### 3. Verifica las métricas
El script mostrará las nuevas métricas. Con más datos reales, esperamos:
- **R² > 0.80** (mejor con más datos)
- **MAPE < 15%** (menor error con datos reales)

## Limitaciones Actuales

1. **Dataset pequeño**: Solo 27 eventos de entrenamiento
2. **Datos sintéticos**: Basado en estimaciones, no datos reales
3. **Variabilidad alta**: MAPE del 22% (intervalo de confianza amplio)

## Mejoras Futuras

1. **Más datos**: Aumentar a 100+ eventos con datos reales
2. **Más features**:
   - Clima durante el evento
   - Competencia con otros eventos
   - Índices económicos de la ciudad
3. **Time series**: Incorporar estacionalidad
4. **Deep learning**: Probar redes neuronales con más datos

## Archivos Relacionados

```
backend/app/ml/
├── __init__.py
├── economic_impact_model.py   # Modelo principal
└── saved_models/
    └── economic_impact_model.pkl  # Modelo entrenado

data/
├── examples/
│   ├── events.csv             # Datos de eventos
│   ├── cities.csv             # Datos de ciudades
│   └── event_impacts.csv      # Impactos calculados
└── scripts/
    └── train_economic_model.py  # Script de entrenamiento
```

---

**Última actualización**: 2025-11-21
**Modelo**: Random Forest (scikit-learn)
**Training samples**: 27 eventos
