# Modelo de Impacto Económico de Evently

## 1. Qué datos usa y cómo los preparamos
- Se alimenta de los 7 CSV principales ubicados en `data/examples/`: `events.csv`, `cities.csv`, `event_impacts.csv` y las series de métricas (`tourism_metrics.csv`, `hotel_metrics.csv`, `economic_metrics.csv`, `mobility_metrics.csv`).
- El script `backend/train_model.py` (y `scripts/ml/train_and_evaluate_model.py`) invoca `EconomicImpactModel.load_data()`, que combina `event_impacts` con información de ciudades y enriquece cada registro con métricas históricas (turismo, hotelería, economía y movilidad) calculadas sobre los 30 días previos y el periodo del evento.
- A partir de esas fuentes se generan derivadas con impacto comprobado: `attendance_per_day`, `visitors_per_hotel_room`, `city_tourism_intensity`, tasas de incremento y ocupación, precios máximos/medios de hotelería y datos de movilidad.

## 2. Cómo lo entrenamos (el "3-train")
El pipeline se articula en tres fases clave que explican cómo se entrena el modelo:

1. **Preparación de datos y features**: se filtran registros con el target (`total_economic_impact_usd`), se rellenan valores faltantes, se codifica `event_type` y se elige un conjunto reducido de columnas (eventos, ciudad y métricas no redundantes). Este paso asegura calidad antes de entrenar.
2. **Entrenamiento/validación**: `train()` divide el dataset en 80% train / 20% test tras aplicar `log1p` al target. Luego entrena cinco modelos (Linear, Ridge, Lasso, Random Forest y Gradient Boosting) sobre los datos escalados. Cada modelo se evalúa tanto en el test final como con validación cruzada (5-fold) para estimar estabilidad.
3. **Selección y evaluación final**: se escoge el modelo con mayor R² sobre el conjunto de prueba. Si el modelo dispone de importancias (como el árbol), se imprimen los features más influyentes. Finalmente se guarda el mejor predictor en `backend/app/ml/saved_models/economic_impact_model.pkl` y ese objeto se reutiliza para las APIs y el predictor CLI.

## 3. Métricas principales (R², MAP, etc.)
Durante el entrenamiento se muestran por cada modelo las métricas clave:

- **R² Score**: explica qué proporción de la varianza del impacto económico se explica. Se registra sobre el conjunto de test con el target destransformado (aplicando `expm1`).
- **MAE (Error absoluto medio)** y **RMSE**: cuantifican el error promedio, útiles para entender desviaciones monetarias.
- **MAPE** (el "map" que mencionaste): se calcula como la media porcentual del error absoluto relativo, evitando divisiones por cero. El informe también muestra un intervalo de confianza basado en ese MAPE para cada predicción.
- **CV R² (5-fold)**: cada modelo reporta la media y desviación estándar de R² obtenida en validación cruzada, lo cual da visibilidad sobre la consistencia general del entrenamiento.

El resumen final resalta: el mejor modelo (habitualmente `gradient_boosting`), su R², su MAPE y la ruta donde se guarda el pickle.

## 4. Qué más aporta el modelo
- **Predicciones en la API**: `EconomicImpactModel.predict()` reconstruye el feature vector, vuelve a escalarlo y devuelve predicciones con bounds (90% de confianza), desglose directo/indirecto/inducido, estimación de empleo y ROI. Los ratios de jobs se ajustan por ciudad y duración usando referencias históricas (1.102 eventos).
- **Análisis de features**: `scripts/ml/analyze_and_reduce_features.py` explora correlaciones y guarda recomendaciones en `data/outputs/feature_recommendations.json` para decidir qué conservar/eliminar. También calcula un top 25 por importancia combinada (Gradient Boosting + SelectKBest).
- **Scripts auxiliares**: `scripts/ml/show_model_metrics.py` lee el pickle para mostrar métricas sin reentrenar; `scripts/ml/predict.py` y `server_simple.py` permiten obtener predicciones desde consola o un servidor FastAPI sencillo cuando no se quiere cargar toda la base de datos.

## 5. Cómo interpretar métricas clave
| Métrica | Qué indica | Nota útil |
|--------|------------|-----------|
| R² | Qué % de la varianza explica el modelo | +Cercano a 1 mejor; se usa para elegir el modelo principal en el `train()` y para contextualizar la confianza de la predicción final.
| MAPE | Error porcentual medio | Se usa como base para calcular el intervalo de confianza (`±1.5×MAPE`).
| MAE / RMSE | Error monetario promedio | Máximo valor esperado en dólares. Útil para comunicar sesgo frente a decisiones reales.
| CV R² | Estabilidad entre folds | Ayuda a detectar overfitting; si la desviación es alta, hay que volver a analizar features o regularización.

## 6. Referencias internas
- El entrenamiento principal ocurre en `backend/train_model.py`, pero el mismo flujo está replicado en `scripts/ml/train_and_evaluate_model.py` para uso fuera de la carpeta `backend`.
- El entorno CLI de predicción (`scripts/ml/predict.py`) y el servidor simple (`scripts/ml/server_simple.py`) usan el modelo guardado y las mismas codificaciones guardadas en el objeto `EconomicImpactModel`.
- Si se actualizan los CSVs de métricas, es suficiente correr los generadores de `scripts/data/` (por ejemplo `generate_quality_events.py`, `generate_final_events.py`, `generate_more_event_impacts.py`, `update_events_csv.py` y `fix_and_retrain.py`) y luego reentrenar para reflejar los nuevos patrones.
