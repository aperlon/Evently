# 📚 Documentación Completa del Backend de Predicciones - Evently

Este documento explica **todos los archivos** relacionados con la generación de predicciones en el backend, cómo funcionan y cómo se relacionan entre sí.

---

## 📁 Estructura de Archivos

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints.py          # Endpoints de la API (incluye /predict)
│   │   └── schemas.py            # Esquemas de validación (Pydantic)
│   ├── ml/
│   │   ├── economic_impact_model.py  # ⭐ MODELO PRINCIPAL DE ML
│   │   └── __init__.py           # Exportaciones del módulo ML
│   └── main.py                   # Aplicación FastAPI principal
│
data/examples/
├── cities.csv                    # Datos de ciudades
├── events.csv                    # Datos de eventos históricos
├── event_impacts.csv            # Impactos económicos históricos (TARGET)
├── tourism_metrics.csv          # ⭐ Métricas diarias de turismo (time-series)
├── hotel_metrics.csv            # ⭐ Métricas diarias de hoteles (time-series)
├── economic_metrics.csv         # ⭐ Métricas diarias económicas (time-series)
└── mobility_metrics.csv         # ⭐ Métricas diarias de movilidad (time-series)
```

---

## 🎯 Flujo General del Sistema

```
1. Usuario hace request → POST /api/v1/predict
2. FastAPI recibe request → endpoints.py
3. Valida datos → schemas.py (PredictionInput)
4. Obtiene modelo ML → get_ml_model() (singleton)
5. Modelo busca eventos similares → predict_simple()
6. Modelo genera predicción → predict()
7. Calcula KPIs adicionales → breakdown, estimates, baseline
8. Retorna respuesta → schemas.py (PredictionResponse)
```

---

## 📄 ARCHIVO 1: `backend/app/api/endpoints.py`

**Propósito**: Define todos los endpoints de la API REST, incluyendo el endpoint de predicción.

### Sección Clave: Inicialización del Modelo ML

```python
# Líneas 19-50: Singleton del modelo ML
_ml_model = None  # Variable global para mantener una sola instancia

def get_ml_model() -> EconomicImpactModel:
    """
    Patrón Singleton: Solo crea UNA instancia del modelo en toda la aplicación.
    Esto es importante porque:
    - El modelo es pesado (tiene que cargar datos CSV)
    - Entrenar el modelo toma tiempo
    - Queremos reutilizar el modelo entrenado
    """
    global _ml_model
    if _ml_model is None:
        # Primera vez: crear instancia
        _ml_model = EconomicImpactModel()
        try:
            # Intentar cargar modelo pre-entrenado
            _ml_model.load()
            if _ml_model.best_model is None:
                raise FileNotFoundError("Model file exists but is invalid")
        except (FileNotFoundError, Exception) as e:
            # Si no existe o está corrupto, entrenar desde cero
            print(f"⚠️  Model not found or invalid: {e}")
            print("🔄 Training model from CSV data...")
            try:
                _ml_model.load_data()  # Cargar CSVs
                _ml_model.train()      # Entrenar modelos
                _ml_model.save()       # Guardar para próxima vez
                print("✅ Model trained and saved successfully")
            except Exception as train_error:
                print(f"❌ Error training model: {train_error}")
                raise ValueError(f"Could not train model: {train_error}")
    
    # Verificar que el modelo está listo
    if _ml_model.best_model is None:
        raise ValueError("Model is not trained...")
    
    return _ml_model
```

### Endpoint Principal: `/predict`

```python
# Líneas 514-555: Endpoint de predicción
@router.post("/predict", response_model=schemas.PredictionResponse)
def predict_event_impact(input_data: schemas.PredictionInput):
    """
    Endpoint principal para hacer predicciones.
    
    Input mínimo requerido:
    - event_type: "sports", "music", "festival", "culture"
    - city: "London", "Tokyo", etc. (debe existir en cities.csv)
    - duration_days: 1-365 días
    - attendance: OPCIONAL (se estima si no se proporciona)
    
    Proceso:
    1. Obtiene el modelo ML (singleton)
    2. Verifica que esté entrenado
    3. Llama a predict_simple() que:
       - Busca eventos históricos similares
       - Estima parámetros faltantes
       - Genera predicción
       - Calcula baseline comparison
    4. Retorna resultado completo
    """
    try:
        model = get_ml_model()  # Obtener modelo (singleton)
        
        # Verificar que el modelo esté listo
        if model.best_model is None:
            # Si no está entrenado, entrenarlo ahora
            print("⚠️  Model not ready, attempting to train...")
            model.load_data()
            model.train()
            model.save()
        
        # Hacer predicción usando método "simple" (auto-estima parámetros)
        result = model.predict_simple(
            event_type=input_data.event_type,
            city=input_data.city,
            duration_days=input_data.duration_days,
            attendance=input_data.attendance  # Puede ser None
        )
        return result
    except ValueError as e:
        # Error de validación (ciudad no encontrada, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Error interno del servidor
        raise HTTPException(status_code=500, detail=f"Error making prediction: {str(e)}")
```

### Endpoint Alternativo: `/predict/detailed`

```python
# Líneas 558-605: Endpoint con parámetros avanzados
@router.post("/predict/detailed")
def predict_event_impact_detailed(...):
    """
    Endpoint avanzado que permite sobrescribir parámetros estimados.
    
    Útil cuando el usuario tiene datos específicos sobre:
    - visitor_increase_pct: Incremento de visitantes conocido
    - price_increase_pct: Incremento de precios conocido
    - occupancy_boost: Boost de ocupación conocido
    
    Si se proporcionan estos parámetros, usa predict() directamente.
    Si no, usa predict_simple() que los estima.
    """
```

---

## 📄 ARCHIVO 2: `backend/app/api/schemas.py`

**Propósito**: Define los esquemas de validación Pydantic para requests y responses.

### Esquema de Input: `PredictionInput`

```python
# Líneas 304-309: Input del usuario
class PredictionInput(BaseModel):
    """
    Esquema que valida los datos que envía el frontend.
    
    Campos:
    - event_type: str (debe ser uno de los tipos válidos)
    - city: str (debe existir en cities.csv)
    - duration_days: int (1-365, validado con ge=1, le=365)
    - attendance: Optional[int] (opcional, >= 0)
    
    Pydantic valida automáticamente:
    - Tipos de datos
    - Rangos (ge=greater or equal, le=less or equal)
    - Campos requeridos vs opcionales
    """
    event_type: str = Field(..., description="Type: sports, music, festival, culture")
    city: str = Field(..., description="City name from available cities")
    duration_days: int = Field(..., ge=1, le=365, description="Event duration in days")
    attendance: Optional[int] = Field(None, ge=0, description="Expected attendance (optional)")
```

### Esquema de Output: `PredictionResponse`

```python
# Líneas 358-366: Respuesta completa
class PredictionResponse(BaseModel):
    """
    Estructura de la respuesta que se envía al frontend.
    
    Contiene:
    - prediction: Resultado principal (impacto, límites, confianza)
    - breakdown: Desglose económico (directo, indirecto, inducido)
    - estimates: Estimaciones adicionales (empleos, ROI, costo)
    - baseline_comparison: Comparación con semana normal
    - model_info: Información del modelo (R², MAPE, algoritmo usado)
    - input_summary: Resumen de inputs usados
    """
    prediction: PredictionResult
    breakdown: PredictionBreakdown
    estimates: PredictionEstimates
    historical_reference: Optional[HistoricalReference] = None
    baseline_comparison: Optional[BaselineComparison] = None
    model_info: Dict[str, Any]
    input_summary: Dict[str, Any]
```

---

## 📄 ARCHIVO 3: `backend/app/ml/economic_impact_model.py` ⭐ **ARCHIVO PRINCIPAL**

**Propósito**: Contiene toda la lógica del modelo de Machine Learning.

### Clase Principal: `EconomicImpactModel`

```python
# Líneas 23-85: Inicialización
class EconomicImpactModel:
    """
    Modelo de regresión para predecir impacto económico de eventos.
    
    Características:
    - Lee datos desde archivos CSV (fácil de actualizar)
    - Entrena múltiples algoritmos y selecciona el mejor
    - Guarda el modelo entrenado para reutilización
    - Auto-estima parámetros faltantes usando eventos históricos similares
    """
    
    def __init__(self, data_dir: str = None):
        """
        Inicializa el modelo.
        
        Busca el directorio de datos en varios lugares posibles:
        1. data/examples/ (relativo al proyecto)
        2. /data/examples/ (Docker)
        3. /home/user/Evently/data/examples/ (producción)
        
        Inicializa:
        - DataFrames para almacenar CSVs
        - Diccionario de modelos (para probar varios algoritmos)
        - Scaler (para normalizar features)
        - Label encoders (para codificar tipos de eventos)
        - Feature columns (lista de variables que usa el modelo)
        """
```

### Método 1: `load_data()` - Cargar Datos CSV

```python
# Líneas 86-133: Cargar CSVs
def load_data(self) -> pd.DataFrame:
    """
    Carga los 7 archivos CSV (3 básicos + 4 de métricas time-series):
    
    CSVs BÁSICOS:
    1. events.csv: Información de eventos históricos
       - event_name, city, event_type, start_date, end_date, etc.
    
    2. cities.csv: Información de ciudades
       - name, country, population, annual_tourists, hotel_rooms, etc.
    
    3. event_impacts.csv: ⭐ TARGET VARIABLE (lo que queremos predecir)
       - event_name, city, total_economic_impact_usd, etc.
    
    CSVs DE MÉTRICAS TIME-SERIES (⭐ NUEVOS):
    4. tourism_metrics.csv: Datos diarios de turismo
       - city, date, total_visitors, avg_spending_per_visitor_usd, etc.
       - Miles de registros diarios por ciudad
    
    5. hotel_metrics.csv: Datos diarios de hoteles
       - city, date, occupancy_rate_pct, avg_price_usd, etc.
       - Datos diarios de ocupación y precios
    
    6. economic_metrics.csv: Datos diarios de gasto económico
       - city, date, total_spending_usd, accommodation_spending_usd, etc.
       - Desglose diario de gasto por categoría
    
    7. mobility_metrics.csv: Datos diarios de movilidad
       - city, date, airport_arrivals, public_transport_usage, etc.
       - Métricas de transporte y movilidad
    
    Luego llama a _prepare_training_data() que:
    - Hace merge de los CSVs básicos
    - Enriquece cada evento con métricas de los CSVs time-series
    - Crea features derivadas (promedios, diferencias, ratios)
    - Limpia datos faltantes
    """
    # Load basic CSVs
    self.df_events = pd.read_csv(self.data_dir / "events.csv")
    self.df_cities = pd.read_csv(self.data_dir / "cities.csv")
    self.df_impacts = pd.read_csv(self.data_dir / "event_impacts.csv")
    
    # Load time-series metrics CSVs
    self.df_tourism_metrics = pd.read_csv(self.data_dir / "tourism_metrics.csv")
    self.df_hotel_metrics = pd.read_csv(self.data_dir / "hotel_metrics.csv")
    self.df_economic_metrics = pd.read_csv(self.data_dir / "economic_metrics.csv")
    self.df_mobility_metrics = pd.read_csv(self.data_dir / "mobility_metrics.csv")
    
    # Convert date columns to datetime
    self.df_tourism_metrics['date'] = pd.to_datetime(self.df_tourism_metrics['date'])
    self.df_hotel_metrics['date'] = pd.to_datetime(self.df_hotel_metrics['date'])
    self.df_economic_metrics['date'] = pd.to_datetime(self.df_economic_metrics['date'])
    self.df_mobility_metrics['date'] = pd.to_datetime(self.df_mobility_metrics['date'])
    
    # Preparar datos para entrenamiento
    self.df_training = self._prepare_training_data()
    return self.df_training
```

### Método 2: `_prepare_training_data()` - Preparar Datos

```python
# Líneas 135-470: Preparación de datos
def _prepare_training_data(self) -> pd.DataFrame:
    """
    ⭐ MÉTODO CRÍTICO: Prepara los datos para entrenar el modelo.
    
    Pasos:
    
    1. MERGE DE DATOS BÁSICOS:
       - Une event_impacts con cities (para obtener características de ciudad)
       - Une con events (para obtener tipo de evento, duración)
    
    2. ⭐ ENRIQUECER CON MÉTRICAS TIME-SERIES (_enrich_with_metrics):
       Para cada evento histórico:
       a) Obtiene fechas del evento (start_date, end_date)
       b) Calcula período baseline (30 días antes del evento)
       c) Extrae métricas del período del evento desde los 4 CSVs
       d) Extrae métricas del período baseline
       e) Calcula diferencias y ratios:
          - visitor_increase_actual (desde tourism_metrics)
          - spending_increase_pct (desde tourism_metrics)
          - occupancy_boost_actual (desde hotel_metrics)
          - hotel_price_increase_actual (desde hotel_metrics)
          - daily_spending_increase_pct (desde economic_metrics)
          - airport_arrivals_increase_pct (desde mobility_metrics)
       f) Agrega ~30 nuevas features derivadas de los CSVs
    
    3. CALCULAR FEATURES FALTANTES (si no están en los CSVs):
       - Si falta attendance: estima desde annual_tourists
       - Si falta visitor_increase_pct: usa visitor_increase_actual o calcula
       - Si falta price_increase_pct: usa hotel_price_increase_actual o estima
       - Si falta occupancy_boost: usa occupancy_boost_actual o estima
    
    4. CREAR FEATURES DERIVADAS:
       - attendance_per_day = attendance / duration_days
       - visitors_per_hotel_room = attendance / hotel_rooms
       - city_tourism_intensity = annual_tourists / population
    
    5. ENCODING:
       - event_type → event_type_encoded (LabelEncoder)
       - Convierte texto a número para que el modelo lo entienda
    
    6. DEFINIR FEATURES FINALES (ahora ~45 variables en lugar de 13):
       Event characteristics (6):
       - attendance, duration_days, event_type_encoded
       - visitor_increase_pct, price_increase_pct, occupancy_boost
       
       City characteristics (4):
       - population, annual_tourists, hotel_rooms, avg_hotel_price_usd
       
       Derived features (3):
       - attendance_per_day, visitors_per_hotel_room, city_tourism_intensity
       
       ⭐ Tourism metrics (7):
       - event_avg_total_visitors, baseline_avg_total_visitors
       - visitor_increase_actual, event_avg_spending_per_visitor
       - baseline_avg_spending_per_visitor, spending_increase_pct
       - event_avg_stay_duration
       
       ⭐ Hotel metrics (7):
       - event_avg_occupancy_pct, baseline_avg_occupancy_pct
       - occupancy_boost_actual, event_avg_hotel_price
       - baseline_avg_hotel_price, hotel_price_increase_actual
       - event_max_hotel_price
       
       ⭐ Economic metrics (6):
       - event_avg_daily_spending, baseline_avg_daily_spending
       - daily_spending_increase_pct, event_avg_accommodation_spending
       - event_avg_food_spending, event_avg_retail_spending
       
       ⭐ Mobility metrics (7):
       - event_avg_airport_arrivals, baseline_avg_airport_arrivals
       - airport_arrivals_increase_pct, event_avg_international_flights
       - event_avg_public_transport, event_avg_traffic_congestion
       - baseline_avg_traffic_congestion
    
    7. LIMPIEZA:
       - Elimina filas sin target variable (total_economic_impact_usd)
       - Rellena valores faltantes con medianas o 0
       - Asegura que todas las features existan
    """
```

### Método 3: `train()` - Entrenar Modelos

```python
# Líneas 241-350: Entrenamiento
def train(self, test_size: float = 0.2, random_state: int = 42) -> Dict:
    """
    ⭐ MÉTODO PRINCIPAL: Entrena múltiples algoritmos y selecciona el mejor.
    
    Proceso:
    
    1. PREPARAR DATOS:
       - X = features (13 columnas)
       - y = target (total_economic_impact_usd)
       - Transformación logarítmica: y_log = log(1 + y)
         * Por qué? El impacto económico tiene distribución sesgada
         * Log transform hace la distribución más normal
         * Mejora el rendimiento del modelo
    
    2. SPLIT:
       - 80% entrenamiento, 20% testing
       - random_state=42 para reproducibilidad
    
    3. SCALING:
       - Normaliza features con StandardScaler
       - Importante para algoritmos sensibles a escala (Ridge, Lasso)
    
    4. ENTRENAR 5 ALGORITMOS:
       a) Linear Regression: Modelo simple, rápido
       b) Ridge Regression: Linear con regularización L2
       c) Lasso Regression: Linear con regularización L1
       d) Random Forest: Ensemble de árboles (suele ser el mejor)
       e) Gradient Boosting: Boosting de árboles
    
    5. EVALUAR CADA MODELO:
       - R² Score: Bondad de ajuste (0-1, más alto mejor)
       - MAE: Error absoluto promedio
       - RMSE: Error cuadrático medio
       - MAPE: Error porcentual promedio
       - Cross-validation: 5-fold CV para validar robustez
    
    6. SELECCIONAR MEJOR:
       - Elige el modelo con mayor R² Score
       - Guarda como self.best_model
    
    7. FEATURE IMPORTANCE:
       - Si es modelo de árboles, muestra qué features son más importantes
    """
    
    # Transformación logarítmica del target
    y_log = np.log1p(y)  # log(1 + y) para manejar ceros
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_log, test_size=0.2, random_state=42
    )
    
    # Normalizar features
    X_train_scaled = self.scaler.fit_transform(X_train)
    X_test_scaled = self.scaler.transform(X_test)
    
    # Probar 5 algoritmos
    model_configs = {
        'linear_regression': LinearRegression(),
        'ridge_regression': Ridge(alpha=1.0),
        'lasso_regression': Lasso(alpha=0.1),
        'random_forest': RandomForestRegressor(...),
        'gradient_boosting': GradientBoostingRegressor(...),
    }
    
    # Entrenar y evaluar cada uno
    for name, model in model_configs.items():
        model.fit(X_train_scaled, y_train)
        y_pred_log = model.predict(X_test_scaled)
        
        # Transformar de vuelta a escala original
        y_pred = np.expm1(y_pred_log)  # exp(y) - 1
        y_test_original = np.expm1(y_test)
        
        # Calcular métricas
        metrics = {
            'r2': r2_score(y_test_original, y_pred),
            'mape': mean_absolute_percentage_error(...),
            ...
        }
        
        # Guardar mejor modelo
        if metrics['r2'] > best_r2:
            self.best_model = model
            self.best_model_name = name
```

### Método 4: `predict()` - Predicción Directa

```python
# Líneas 364-490: Predicción con parámetros completos
def predict(self, event_data: Dict) -> Dict:
    """
    Predice impacto económico cuando tienes TODOS los parámetros.
    
    Input esperado:
    {
        'event_type': 'sports',
        'city': 'London',
        'attendance': 50000,
        'duration_days': 7,
        'visitor_increase_pct': 50.0,  # Opcional
        'price_increase_pct': 40.0,    # Opcional
        'occupancy_boost': 15.0         # Opcional
    }
    
    Proceso:
    
    1. OBTENER DATOS DE CIUDAD:
       - Busca ciudad en df_cities
       - Extrae: population, annual_tourists, hotel_rooms, avg_hotel_price_usd
    
    2. ENCODING:
       - Convierte event_type a número usando LabelEncoder
    
    3. ESTIMAR PARÁMETROS FALTANTES (si no se proporcionan):
       - visitor_increase_pct: min(100, attendance / baseline_daily * 100)
       - price_increase_pct: min(150, visitor_increase * 0.8)
       - occupancy_boost: min(25, visitor_increase * 0.3)
    
    4. CONSTRUIR FEATURE VECTOR (13 valores):
       features = [
           attendance,
           duration_days,
           event_type_encoded,
           visitor_increase_pct,
           price_increase_pct,
           occupancy_boost,
           population,
           annual_tourists,
           hotel_rooms,
           avg_hotel_price_usd,
           attendance / duration_days,           # attendance_per_day
           attendance / hotel_rooms,            # visitors_per_hotel_room
           annual_tourists / population,        # city_tourism_intensity
       ]
    
    5. PREDECIR:
       - Normalizar features con scaler
       - Predecir en escala logarítmica
       - Transformar de vuelta: prediction = exp(pred_log) - 1
    
    6. CALCULAR INTERVALO DE CONFIANZA:
       - lower_bound = prediction * (1 - MAPE * 1.5)
       - upper_bound = prediction * (1 + MAPE * 1.5)
       - Factor 1.5 para intervalo al 90%
    
    7. CALCULAR KPIs:
       - Breakdown: 64% directo, 25% indirecto, 11% inducido
       - Jobs: prediction / 40000
       - ROI: asume 4:1 típico
       - Cost: prediction / 4.0
    """
```

### Método 5: `predict_simple()` - Predicción Inteligente ⭐ **MÉTODO MÁS IMPORTANTE**

```python
# Líneas 492-704: Predicción con auto-estimación
def predict_simple(self, event_type: str, city: str, duration_days: int,
                   attendance: int = None) -> Dict:
    """
    ⭐ MÉTODO PRINCIPAL USADO POR EL FRONTEND
    
    Solo requiere inputs mínimos, el resto lo estima automáticamente
    usando eventos históricos similares.
    
    Proceso detallado:
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 1: OBTENER DATOS DE CIUDAD                             │
    └─────────────────────────────────────────────────────────────┘
    - Busca ciudad en cities.csv
    - Extrae: continent, country, population, annual_tourists, etc.
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 2: BUSCAR EVENTOS SIMILARES                             │
    └─────────────────────────────────────────────────────────────┘
    - Filtra eventos del mismo tipo (event_type)
    - Filtra eventos del mismo continente (mejor match)
    - Si hay < 2 eventos del mismo continente, usa todos globalmente
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 3: CALCULAR PROMEDIOS HISTÓRICOS                        │
    └─────────────────────────────────────────────────────────────┘
    De los eventos similares, calcula promedios de:
    
    a) avg_attendance_per_day:
       - attendance / duration_days para cada evento histórico
       - Promedio de todos
    
    b) avg_visitor_increase_pct:
       - visitor_increase_pct de eventos históricos
       - O calcula desde: (attendance_per_day / baseline_daily) - 1
    
    c) avg_price_increase_pct:
       - price_increase_pct de eventos históricos
       - O estima como: visitor_increase * 0.8
    
    d) avg_occupancy_boost:
       - occupancy_boost de eventos históricos
       - O estima como: visitor_increase * 0.3
    
    e) avg_impact_per_day:
       - total_impact / duration_days para cada evento
       - Promedio de todos
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 4: ESTIMAR ATTENDANCE (si no se proporciona)           │
    └─────────────────────────────────────────────────────────────┘
    if attendance is None:
        attendance = avg_attendance_per_day * duration_days
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 5: CONSTRUIR PARÁMETROS PARA PREDICCIÓN                 │
    └─────────────────────────────────────────────────────────────┘
    prediction_params = {
        'event_type': event_type,
        'city': city,
        'attendance': attendance,  # Estimado o proporcionado
        'duration_days': duration_days,
        'visitor_increase_pct': avg_visitor_increase,  # De históricos
        'price_increase_pct': avg_price_increase,      # De históricos
        'occupancy_boost': avg_occupancy_boost,       # De históricos
        
        # ⭐ NUEVAS MÉTRICAS desde los 4 CSVs adicionales:
        'event_avg_total_visitors': avg_metrics['event_avg_total_visitors'],
        'baseline_avg_total_visitors': avg_metrics['baseline_avg_total_visitors'],
        'visitor_increase_actual': avg_metrics['visitor_increase_actual'],
        'event_avg_spending_per_visitor': avg_metrics['event_avg_spending_per_visitor'],
        'baseline_avg_spending_per_visitor': avg_metrics['baseline_avg_spending_per_visitor'],
        'spending_increase_pct': avg_metrics['spending_increase_pct'],
        'event_avg_occupancy_pct': avg_metrics['event_avg_occupancy_pct'],
        'baseline_avg_occupancy_pct': avg_metrics['baseline_avg_occupancy_pct'],
        'occupancy_boost_actual': avg_metrics['occupancy_boost_actual'],
        'event_avg_hotel_price': avg_metrics['event_avg_hotel_price'],
        'baseline_avg_hotel_price': avg_metrics['baseline_avg_hotel_price'],
        'hotel_price_increase_actual': avg_metrics['hotel_price_increase_actual'],
        'event_max_hotel_price': avg_metrics['event_max_hotel_price'],
        'event_avg_daily_spending': avg_metrics['event_avg_daily_spending'],
        'baseline_avg_daily_spending': avg_metrics['baseline_avg_daily_spending'],
        'daily_spending_increase_pct': avg_metrics['daily_spending_increase_pct'],
        'event_avg_airport_arrivals': avg_metrics['event_avg_airport_arrivals'],
        'baseline_avg_airport_arrivals': avg_metrics['baseline_avg_airport_arrivals'],
        'airport_arrivals_increase_pct': avg_metrics['airport_arrivals_increase_pct'],
        # ... y más métricas
    }
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 6: LLAMAR A predict() CON PARÁMETROS                   │
    └─────────────────────────────────────────────────────────────┘
    result = self.predict(prediction_params)
    # predict() ahora construye un feature vector con ~45 features
    # (13 originales + ~32 nuevas de los CSVs de métricas)
    # Esto genera: prediction, breakdown, estimates, model_info
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 7: CALCULAR BASELINE (semana normal sin evento)         │
    └─────────────────────────────────────────────────────────────┘
    baseline_daily_visitors = annual_tourists / 365
    baseline_daily_spending_per_visitor = 150  # USD (conservador)
    baseline_daily_spending = baseline_daily_visitors * 150
    baseline_period_spending = baseline_daily_spending * duration_days
    baseline_period_impact = baseline_period_spending * 1.7  # Multiplicador
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 8: CALCULAR COMPARACIÓN CON BASELINE                    │
    └─────────────────────────────────────────────────────────────┘
    event_impact = result['prediction']['total_economic_impact_usd']
    additional_impact = event_impact - baseline_period_impact
    impact_multiplier = event_impact / baseline_period_impact
    impact_increase_pct = ((event_impact / baseline_period_impact) - 1) * 100
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 9: AGREGAR CONTEXTO HISTÓRICO                          │
    └─────────────────────────────────────────────────────────────┘
    result['historical_reference'] = {
        'reference_scope': "Europe (5 eventos)" o "Global (12 eventos)",
        'events_analyzed': len(reference_data),
        'avg_visitor_increase_pct': avg_visitor_increase,
        'avg_price_increase_pct': avg_price_increase,
        'avg_occupancy_boost_pct': avg_occupancy_boost,
        'avg_attendance_per_day': avg_attendance_per_day,
        'avg_impact_per_day_usd': avg_impact_per_day,
        'similar_events': ['London Marathon 2024', 'Wimbledon 2024', ...],
    }
    
    ┌─────────────────────────────────────────────────────────────┐
    │ PASO 10: AGREGAR BASELINE COMPARISON                         │
    └─────────────────────────────────────────────────────────────┘
    result['baseline_comparison'] = {
        'baseline_weekly_impact_usd': baseline_period_impact,
        'event_impact_usd': event_impact,
        'additional_impact_usd': additional_impact,
        'impact_multiplier': impact_multiplier,
        'impact_increase_pct': impact_increase_pct,
        'baseline_daily_visitors': baseline_daily_visitors,
        'baseline_daily_spending_usd': baseline_daily_spending,
        'duration_days': duration_days,
    }
    
    return result  # Retorna diccionario completo
    """
```

### Métodos Auxiliares: `save()` y `load()`

```python
# Líneas 718-776: Persistencia del modelo
def save(self, filename: str = "economic_impact_model.pkl"):
    """
    Guarda el modelo entrenado en disco.
    
    Guarda:
    - best_model: El modelo seleccionado (Random Forest, etc.)
    - best_model_name: Nombre del algoritmo
    - all_models: Todos los modelos entrenados
    - scaler: Para normalizar features nuevas
    - label_encoders: Para codificar event_type
    - feature_columns: Lista de features usadas
    - metrics: Métricas de todos los modelos
    - trained_at: Timestamp de cuándo se entrenó
    
    Ubicación: backend/app/ml/saved_models/economic_impact_model.pkl
    """

def load(self, filename: str = "economic_impact_model.pkl"):
    """
    Carga modelo pre-entrenado desde disco.
    
    Si el archivo existe y es válido, carga todo.
    Si no existe, lanza FileNotFoundError (el sistema lo entrena automáticamente).
    """
```

---

## 📄 ARCHIVO 4: `backend/app/main.py`

**Propósito**: Punto de entrada principal de la aplicación FastAPI.

```python
# Líneas 1-51: Configuración de FastAPI
"""
Aplicación principal FastAPI.

Configura:
- CORS: Permite requests desde el frontend
- Routers: Incluye endpoints.py y upload.py
- Documentación: Swagger UI en /docs
"""

app = FastAPI(
    title="Evently API",
    version="1.0.0",
    description="Event Impact Analyzer API"
)

# CORS para permitir frontend
app.add_middleware(CORSMiddleware, ...)

# Incluir routers
app.include_router(api_router, prefix="/api/v1")
```

---

## 📊 ARCHIVO 5: Estructura de Datos CSV

### `data/examples/cities.csv`

```csv
name,country,country_code,continent,latitude,longitude,timezone,population,area_km2,gdp_usd,annual_tourists,hotel_rooms,avg_hotel_price_usd
London,United Kingdom,GBR,Europe,51.5074,-0.1278,Europe/London,9000000,1572,635000000000,19600000,150000,180
```

**Columnas clave para predicciones:**
- `name`: Nombre de la ciudad (usado para buscar)
- `population`: Población (feature del modelo)
- `annual_tourists`: Turistas anuales (feature + cálculo baseline)
- `hotel_rooms`: Habitaciones disponibles (feature)
- `avg_hotel_price_usd`: Precio promedio (feature)
- `continent`: Usado para filtrar eventos similares

### `data/examples/events.csv`

```csv
event_name,city,event_type,description,start_date,end_date,year,expected_attendance,actual_attendance,venue_name,venue_capacity,is_recurring,recurrence_pattern,edition_number
London Marathon 2024,London,sports,Major sports event,2024-04-21,2024-04-21,2024,50000,48000,London City Center,,1,annual,
```

**Columnas clave:**
- `event_name`: Identificador único
- `city`: Ciudad donde ocurrió
- `event_type`: Tipo (sports, music, etc.) - usado para buscar similares
- `start_date`, `end_date`: Para calcular duration_days
- `actual_attendance`: Asistencia real (si está disponible)

### `data/examples/event_impacts.csv` ⭐ **TARGET VARIABLE**

```csv
event_name,city,event_type,year,attendance,duration_days,total_economic_impact_usd,jobs_created,roi_ratio
London Marathon 2024,London,sports,2024,48000,1,9840274,480,4.73
```

**Columnas clave:**
- `event_name`: Link con events.csv
- `total_economic_impact_usd`: ⭐ **ESTO ES LO QUE PREDECIMOS**
- `attendance`: Asistencia (puede estar aquí o en events.csv)
- `duration_days`: Duración (puede calcularse desde start/end_date)
- `jobs_created`, `roi_ratio`: Datos adicionales (no se usan para entrenar)

---

## 🔄 Flujo Completo de una Predicción

```
┌─────────────────────────────────────────────────────────────┐
│ 1. FRONTEND: Usuario llena formulario                        │
│    - event_type: "sports"                                    │
│    - city: "London"                                          │
│    - duration_days: 7                                        │
│    - attendance: null (opcional)                             │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. FRONTEND: POST /api/v1/predict                            │
│    {                                                          │
│      "event_type": "sports",                                 │
│      "city": "London",                                       │
│      "duration_days": 7,                                     │
│      "attendance": null                                      │
│    }                                                          │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. BACKEND: endpoints.py - predict_event_impact()            │
│    - Valida con schemas.PredictionInput                      │
│    - Llama get_ml_model() (singleton)                        │
│    - Verifica que modelo esté entrenado                      │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. BACKEND: economic_impact_model.py - predict_simple()      │
│                                                                
│    a) Busca ciudad en cities.csv                             │
│       → Encuentra: London, Europe, 9M pop, 19.6M tourists    │
│                                                                
│    b) Busca eventos similares:                               │
│       - Tipo: sports                                         │
│       - Continente: Europe                                   │
│       → Encuentra: London Marathon, Wimbledon, etc.          │
│                                                                
│    c) Calcula promedios históricos:                          │
│       - avg_attendance_per_day: 35,000                       │
│       - avg_visitor_increase_pct: 45%                        │
│       - avg_price_increase_pct: 36%                          │
│       - avg_occupancy_boost: 13.5%                          │
│                                                                
│    d) Estima attendance:                                     │
│       attendance = 35,000 * 7 = 245,000                      │
│                                                                
│    e) Construye feature vector (13 valores)                 │
│                                                                
│    f) Llama predict() con parámetros                         │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. BACKEND: economic_impact_model.py - predict()             │
│                                                                
│    a) Normaliza features con scaler                          │
│    b) Predice en escala log: pred_log = model.predict(X)     │
│    c) Transforma: prediction = exp(pred_log) - 1             │
│       → $50,000,000                                          │
│    d) Calcula intervalos:                                    │
│       lower = $50M * (1 - 0.45 * 1.5) = $16.25M             │
│       upper = $50M * (1 + 0.45 * 1.5) = $83.75M             │
│    e) Calcula breakdown:                                     │
│       direct = $50M * 0.64 = $32M                            │
│       indirect = $50M * 0.25 = $12.5M                        │
│       induced = $50M * 0.11 = $5.5M                          │
│    f) Calcula estimates:                                     │
│       jobs = $50M / $40K = 1,250                             │
│       cost = $50M / 4 = $12.5M                               │
│       roi = 4.0x                                              │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. BACKEND: predict_simple() - Baseline Comparison           │
│                                                                
│    a) Calcula baseline:                                      │
│       daily_visitors = 19.6M / 365 = 53,699                  │
│       daily_spending = 53,699 * $150 = $8,054,850            │
│       period_spending = $8M * 7 = $56.4M                     │
│       baseline_impact = $56.4M * 1.7 = $95.9M                │
│                                                                
│    b) Compara:                                                │
│       additional = $50M - $95.9M = -$45.9M (negativo!)       │
│       multiplier = $50M / $95.9M = 0.52x                     │
│       increase = -48%                                         │
│                                                                
│    c) Agrega contexto histórico                               │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. BACKEND: Retorna respuesta completa                       │
│    {                                                          │
│      "prediction": {                                          │
│        "total_economic_impact_usd": 50000000,                │
│        "lower_bound_usd": 16250000,                           │
│        "upper_bound_usd": 83750000,                           │
│        "confidence_level": "90%"                              │
│      },                                                       │
│      "breakdown": {...},                                     │
│      "estimates": {...},                                     │
│      "baseline_comparison": {...},                           │
│      "historical_reference": {...},                          │
│      "model_info": {...}                                     │
│    }                                                          │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. FRONTEND: Recibe y muestra resultados                     │
│    - Tarjeta principal con impacto total                     │
│    - Desglose económico                                      │
│    - Estimaciones (empleos, ROI)                             │
│    - Comparación con baseline                                │
│    - Información del modelo                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Puntos Clave para Entender

### 1. **Por qué Log Transform?**
El impacto económico tiene distribución muy sesgada (algunos eventos generan $1M, otros $1B). La transformación logarítmica hace la distribución más normal, mejorando el rendimiento del modelo.

### 2. **Por qué Múltiples Algoritmos?**
Diferentes algoritmos funcionan mejor con diferentes tipos de datos:
- **Linear/Ridge/Lasso**: Rápidos, interpretables, buenos para relaciones lineales
- **Random Forest**: Mejor para relaciones no-lineales, maneja bien outliers
- **Gradient Boosting**: Muy potente, puede sobreajustar si no se controla

El sistema prueba todos y elige el mejor según R² Score.

### 3. **Por qué Auto-estimación?**
No todos los usuarios tienen todos los datos. El sistema es inteligente:
- Si falta `attendance`: busca eventos similares y promedia
- Si faltan `visitor_increase_pct`, etc.: usa promedios históricos

Esto hace el sistema más accesible.

### 4. **Por qué Baseline Comparison?**
Un evento puede generar $50M, pero si una semana normal genera $100M, el evento es peor que lo normal. La comparación con baseline da contexto real.

### 5. **Por qué Ratios Fijos (64/25/11)?**
Son estándares de la industria económica. En el futuro se podrían calcular dinámicamente, pero para MVP es suficiente.

---

## 🚀 Cómo Mejorar el Sistema

### 1. **Mejorar Datos** ✅ **MEJORADO**
- ✅ **COMPLETADO**: Ahora usa los 7 CSVs (3 básicos + 4 de métricas)
- Añadir más eventos históricos a los CSVs
- Asegurar que todos tengan `total_economic_impact_usd`
- Añadir más ciudades
- Expandir rango de fechas en los CSVs de métricas

### 2. **Mejorar Modelo** ✅ **MEJORADO**
- ✅ **COMPLETADO**: Ahora usa ~45 features en lugar de 13
- ✅ **COMPLETADO**: Features reales desde datos time-series
- Ajustar hiperparámetros de cada algoritmo
- Probar más algoritmos (XGBoost, Neural Networks)
- Feature engineering más avanzado (interacciones entre features)
- Validación cruzada más robusta
- **Esperado**: MAPE debería bajar significativamente (de ~45% a <20%)

### 3. **Mejorar Estimaciones**
- Calcular ratios 64/25/11 dinámicamente usando economic_metrics.csv
- Mejorar estimación de baseline usando datos reales de tourism_metrics.csv
- Ajustar $40K por empleo por región
- Calcular ROI real desde economic_metrics.csv

### 4. **Mejorar UX**
- Mostrar eventos similares usados en la predicción
- Explicar por qué se eligieron esos eventos
- Mostrar confianza por feature (cuáles son más inciertos)
- Mostrar qué métricas vienen de datos reales vs estimadas

---

## 📝 Resumen Ejecutivo

**Archivos Clave:**
1. `endpoints.py`: API REST, maneja requests
2. `schemas.py`: Validación de datos
3. `economic_impact_model.py`: ⭐ Lógica completa del ML
4. `main.py`: Configuración FastAPI
5. **CSVs (7 archivos)**:
   - 3 básicos: events.csv, cities.csv, event_impacts.csv
   - 4 de métricas: tourism_metrics.csv, hotel_metrics.csv, economic_metrics.csv, mobility_metrics.csv

**Flujo:**
1. Usuario → Frontend → POST /predict
2. FastAPI valida → Llama modelo ML
3. Modelo busca eventos similares → Estima parámetros
4. Modelo predice impacto → Calcula KPIs
5. Retorna respuesta completa → Frontend muestra

**Características Clave:**
- Auto-entrenamiento si no existe modelo
- Auto-estimación de parámetros faltantes
- Comparación con baseline
- Múltiples algoritmos, elige el mejor
- Persistencia del modelo entrenado
- ⭐ **NUEVO**: Usa 7 CSVs (3 básicos + 4 de métricas time-series)
- ⭐ **NUEVO**: ~45 features en lugar de 13 (mejor precisión esperada)
- ⭐ **NUEVO**: Features reales desde datos históricos diarios

---

¿Quieres que profundice en alguna parte específica o que explique cómo mejorar algún aspecto en particular?

