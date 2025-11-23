# 📐 Fórmulas del Modelo de Regresión - Economic Impact Model

## 🎯 Objetivo del Modelo

Predecir el **impacto económico total** (`total_economic_impact_usd`) de un evento basándose en sus características y las de la ciudad donde se realiza.

---

## 📊 Variables de Entrada (Features)

### 1. Características del Evento

- **`attendance`**: Asistencia esperada al evento
- **`duration_days`**: Duración del evento en días
- **`event_type_encoded`**: Tipo de evento codificado (sports, music, culture, festival, business)
- **`visitor_increase_pct`**: Porcentaje de aumento de visitantes
- **`price_increase_pct`**: Porcentaje de aumento de precios hoteleros
- **`occupancy_boost`**: Aumento en ocupación hotelera (%)

### 2. Características de la Ciudad

- **`population`**: Población de la ciudad
- **`annual_tourists`**: Turistas anuales
- **`hotel_rooms`**: Número de habitaciones hoteleras
- **`avg_hotel_price_usd`**: Precio promedio de hotel (USD)

### 3. Features Derivadas (Calculadas)

#### Fórmula 1: Asistencia por Día
```
attendance_per_day = attendance / duration_days
```

#### Fórmula 2: Visitantes por Habitación
```
visitors_per_hotel_room = attendance / hotel_rooms
```

#### Fórmula 3: Intensidad Turística de la Ciudad
```
city_tourism_intensity = annual_tourists / population
```

#### Fórmula 4: Sensibilidad de Precio (no usada en modelo final)
```
price_sensitivity = price_increase_pct / visitor_increase_pct
```

---

## 🔄 Transformación de Datos

### Transformación Logarítmica del Target

El modelo usa **transformación logarítmica** para mejorar la distribución de los datos:

```
y_log = log(1 + total_economic_impact_usd)
```

**Razón**: Los impactos económicos tienen una distribución muy sesgada (algunos eventos generan millones, otros miles). La transformación logarítmica normaliza la distribución.

### Normalización de Features

Todas las features se normalizan usando **StandardScaler**:

```
X_scaled = (X - μ) / σ
```

Donde:
- `μ` = media de cada feature
- `σ` = desviación estándar de cada feature

**Razón**: Las features tienen escalas muy diferentes (población en millones, precios en cientos, etc.). La normalización asegura que todas tengan el mismo peso.

---

## 🤖 Algoritmos de Regresión Utilizados

### 1. Linear Regression (Regresión Lineal)

**Fórmula**:
```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε
```

Donde:
- `y` = impacto económico (en log space)
- `β₀` = intercepto
- `β₁, β₂, ..., βₙ` = coeficientes
- `x₁, x₂, ..., xₙ` = features
- `ε` = error

**Optimización**: Mínimos Cuadrados Ordinarios (OLS)
```
min Σ(yᵢ - ŷᵢ)²
```

### 2. Ridge Regression (Regresión con Regularización L2)

**Fórmula**:
```
y = β₀ + β₁x₁ + ... + βₙxₙ + λΣβᵢ²
```

Donde `λ` (alpha=1.0) es el parámetro de regularización que penaliza coeficientes grandes.

**Optimización**:
```
min [Σ(yᵢ - ŷᵢ)² + λΣβᵢ²]
```

### 3. Lasso Regression (Regresión con Regularización L1)

**Fórmula**:
```
y = β₀ + β₁x₁ + ... + βₙxₙ + λΣ|βᵢ|
```

Donde `λ` (alpha=0.1) penaliza la suma absoluta de coeficientes, promoviendo sparsity.

**Optimización**:
```
min [Σ(yᵢ - ŷᵢ)² + λΣ|βᵢ|]
```

### 4. Random Forest Regressor

**Fórmula**:
```
ŷ = (1/B) Σᵢ₌₁ᴮ Tᵢ(x)
```

Donde:
- `B` = número de árboles (100)
- `Tᵢ(x)` = predicción del árbol i-ésimo

**Criterio de división**: Varianza reducida
```
Var(Y) - (n_left/n)Var(Y_left) - (n_right/n)Var(Y_right)
```

### 5. Gradient Boosting Regressor

**Fórmula** (aditivo):
```
Fₘ(x) = Fₘ₋₁(x) + αₘhₘ(x)
```

Donde:
- `Fₘ(x)` = modelo después de m iteraciones
- `αₘ` = learning rate (0.1)
- `hₘ(x)` = árbol débil en iteración m

**Pérdida**: Error cuadrado
```
L(y, F(x)) = (y - F(x))²
```

**Gradiente**:
```
-∂L/∂F = 2(y - F(x))
```

---

## 📈 Métricas de Evaluación

### 1. R² Score (Coeficiente de Determinación)

```
R² = 1 - (SS_res / SS_tot)
```

Donde:
- `SS_res = Σ(yᵢ - ŷᵢ)²` (Suma de cuadrados residual)
- `SS_tot = Σ(yᵢ - ȳ)²` (Suma de cuadrados total)
- `ȳ` = media de y

**Interpretación**: 
- R² = 1.0 → Predicción perfecta
- R² = 0.0 → Modelo no mejor que predecir la media
- R² < 0.0 → Modelo peor que predecir la media

### 2. MAE (Mean Absolute Error)

```
MAE = (1/n) Σ|yᵢ - ŷᵢ|
```

**Interpretación**: Error promedio en dólares.

### 3. RMSE (Root Mean Squared Error)

```
RMSE = √[(1/n) Σ(yᵢ - ŷᵢ)²]
```

**Interpretación**: Error promedio (penaliza más los errores grandes).

### 4. MAPE (Mean Absolute Percentage Error)

```
MAPE = (100/n) Σ|(yᵢ - ŷᵢ) / yᵢ|
```

**Interpretación**: Error porcentual promedio.

### 5. Cross-Validation R² (5-fold)

```
CV_R² = (1/k) Σᵢ₌₁ᵏ R²ᵢ
```

Donde `k=5` folds.

---

## 🔮 Predicción

### Paso 1: Preparar Features

```python
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
    attendance / hotel_rooms,              # visitors_per_hotel_room
    annual_tourists / population           # city_tourism_intensity
]
```

### Paso 2: Normalizar

```
X_scaled = scaler.transform(features)
```

### Paso 3: Predecir (en log space)

```
y_pred_log = best_model.predict(X_scaled)
```

### Paso 4: Transformar de vuelta

```
prediction = exp(y_pred_log) - 1
```

Usando `expm1` para mayor precisión numérica:
```
prediction = expm1(y_pred_log)
```

### Paso 5: Calcular Intervalo de Confianza

```
lower_bound = prediction × (1 - MAPE × 1.5)
upper_bound = prediction × (1 + MAPE × 1.5)
```

Donde `MAPE` es el MAPE del modelo en entrenamiento.

---

## 💰 Desglose del Impacto Económico

### Fórmulas de Desglose

```
direct_spending = total_impact × 0.64      # 64% gasto directo
indirect_spending = total_impact × 0.25    # 25% gasto indirecto
induced_spending = total_impact × 0.11     # 11% gasto inducido
```

### Estimación de Empleos

```
jobs_created = total_impact / 40,000
```

**Razón**: Estimación de $40,000 por empleo creado.

### Estimación de ROI

```
estimated_cost = total_impact / 4.0
roi_ratio = total_impact / estimated_cost
```

**Razón**: ROI típico de 4:1 (por cada $1 invertido, se generan $4).

---

## 🎯 Selección del Mejor Modelo

El modelo se selecciona basándose en el **mayor R² Score**:

```python
best_model = argmax(R²_score)
```

Si el mejor modelo es tree-based (Random Forest o Gradient Boosting), se calcula la **importancia de features**:

```
importance_i = (1/n_trees) Σᵢ₌₁ⁿᵗʳᵉᵉˢ importance_i_tree_j
```

---

## 📝 Notas Importantes

1. **Transformación Logarítmica**: El modelo predice en log space para manejar mejor la escala de los datos.

2. **Normalización**: Todas las features se normalizan para que tengan el mismo peso.

3. **Cross-Validation**: Se usa 5-fold CV para evaluar robustez del modelo.

4. **Regularización**: Ridge y Lasso usan regularización para evitar overfitting.

5. **Ensemble Methods**: Random Forest y Gradient Boosting combinan múltiples árboles para mejor predicción.

