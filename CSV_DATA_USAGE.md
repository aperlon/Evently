# 📊 Uso de Datos CSV Históricos

## ✅ Cambios Implementados

El programa ahora **NO genera datos dinámicamente** al ejecutarse. En su lugar, utiliza **CSVs históricos fijos** con datos random pero realistas, y el **modelo de regresión** para hacer predicciones.

## 📁 Archivos CSV Generados

Los CSVs se encuentran en `data/examples/`:

- **cities.csv** - 16 ciudades con información completa
- **events.csv** - 12 eventos principales del año 2024
- **tourism_metrics.csv** - Métricas de turismo diarias (5,856 registros)
- **hotel_metrics.csv** - Métricas hoteleras diarias (5,856 registros)
- **economic_metrics.csv** - Métricas económicas diarias (5,856 registros)
- **mobility_metrics.csv** - Métricas de movilidad diarias (5,856 registros)
- **event_impacts.csv** - Impactos económicos de eventos (para entrenar modelo)

## 🔄 Flujo de Datos

### 1. Generación de CSVs (Una sola vez)

```bash
python data/scripts/generate_historical_csvs.py
```

Este script genera todos los CSVs con datos históricos realistas para todo el año 2024.

### 2. Carga de Datos a Base de Datos

```bash
python data/scripts/load_from_csvs.py
```

Este script:
- Carga ciudades desde `cities.csv`
- Carga eventos desde `events.csv`
- Carga todas las métricas desde los CSVs
- **Entrena automáticamente el modelo de regresión** usando `event_impacts.csv`

### 3. Uso del Modelo de Regresión

El modelo de regresión (`EconomicImpactModel`) se usa automáticamente en:

- **Endpoint `/api/v1/predict`** - Predicción de impacto económico
- **Endpoint `/api/v1/predict/detailed`** - Predicción detallada con parámetros

El modelo:
- Lee datos de `data/examples/event_impacts.csv`
- Se entrena automáticamente al cargar datos
- Guarda el modelo entrenado en `backend/app/ml/saved_models/`
- Usa múltiples algoritmos (Linear Regression, Random Forest, Gradient Boosting) y selecciona el mejor

## 🚀 Scripts de Inicio Actualizados

### `start.sh` (Docker)

Ahora:
1. Verifica si existen CSVs en `data/examples/`
2. Si no existen, los genera automáticamente
3. Carga datos desde CSVs en lugar de generar dinámicamente
4. Entrena el modelo de regresión automáticamente

### `dev.sh` (Sin Docker)

Ahora:
1. Verifica si existen CSVs en `data/examples/`
2. Si no existen, los genera automáticamente
3. Carga datos desde CSVs en lugar de generar dinámicamente
4. Entrena el modelo de regresión automáticamente

## 📊 Modelo de Regresión

### Características

- **Entrenamiento automático**: Se entrena al cargar datos desde CSVs
- **Múltiples algoritmos**: Prueba Linear Regression, Ridge, Lasso, Random Forest, Gradient Boosting
- **Selección automática**: Elige el modelo con mejor R²
- **Predicciones con intervalos de confianza**: Proporciona límites superior e inferior
- **Desglose económico**: Direct, indirect, induced spending
- **Estimaciones**: Jobs created, ROI ratio

### Uso en API

```python
# El modelo se inicializa automáticamente en endpoints.py
model = get_ml_model()  # Singleton pattern

# Predicción simple
result = model.predict_simple(
    event_type="sports",
    city="London",
    duration_days=7,
    attendance=50000
)

# Predicción con parámetros personalizados
result = model.predict({
    'event_type': 'sports',
    'city': 'London',
    'attendance': 50000,
    'duration_days': 7,
    'visitor_increase_pct': 25.0,
    'price_increase_pct': 15.0
})
```

## 🔧 Mantenimiento

### Regenerar CSVs

Si necesitas regenerar los CSVs con nuevos datos:

```bash
python data/scripts/generate_historical_csvs.py
python data/scripts/load_from_csvs.py
```

### Actualizar Datos Reales

Para usar datos reales en lugar de sintéticos:

1. Reemplaza los CSVs en `data/examples/` con tus datos reales
2. Asegúrate de mantener el mismo formato
3. Ejecuta `load_from_csvs.py` para recargar y reentrenar el modelo

### Reentrenar Modelo

El modelo se reentrena automáticamente al cargar datos, pero puedes reentrenarlo manualmente:

```bash
python data/scripts/train_models.py
```

O desde Python:

```python
from app.ml.economic_impact_model import EconomicImpactModel

model = EconomicImpactModel()
model.load_data()
model.train()
model.save()
```

## ✅ Ventajas de Este Enfoque

1. **No genera datos al ejecutar**: Los CSVs están pre-generados
2. **Datos consistentes**: Mismos datos cada vez que ejecutas
3. **Modelo de regresión integrado**: Usa datos históricos para predicciones
4. **Fácil actualización**: Solo reemplaza CSVs para usar datos reales
5. **Rápido**: No hay generación dinámica, solo carga desde archivos

## 📝 Notas

- Los CSVs se generan con datos random pero realistas usando patrones estacionales
- El modelo de regresión se entrena automáticamente al cargar datos
- Los datos cubren todo el año 2024 para 16 ciudades
- Los eventos tienen impactos aplicados en sus períodos correspondientes

