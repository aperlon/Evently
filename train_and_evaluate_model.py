"""
Script para entrenar el modelo y mostrar todas las métricas relevantes
"""
import sys
import os

# Añadir el directorio backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ml.economic_impact_model import EconomicImpactModel
import json

print("=" * 80)
print("🚀 ENTRENANDO MODELO DE IMPACTO ECONÓMICO CON 7 CSVs")
print("=" * 80)
print()

# Crear instancia del modelo
model = EconomicImpactModel()

# Cargar datos (ahora incluye los 4 CSVs adicionales)
print("📂 Cargando datos...")
df_training = model.load_data()
print(f"   ✓ Dataset de entrenamiento: {len(df_training)} muestras")
print(f"   ✓ Features: {len(model.feature_columns)} columnas")
print()

# Entrenar el modelo
print("🎯 Entrenando modelos...")
print()
metrics = model.train()

print()
print("=" * 80)
print("📊 RESUMEN DE MÉTRICAS POR MODELO")
print("=" * 80)
print()

# Mostrar métricas de todos los modelos
for model_name, model_metrics in metrics.items():
    print(f"📈 {model_name.upper().replace('_', ' ')}")
    print(f"   R² Score:        {model_metrics['r2']:.4f}")
    print(f"   MAE:              ${model_metrics['mae']:,.2f}")
    print(f"   RMSE:             ${model_metrics['rmse']:,.2f}")
    print(f"   MAPE:             {model_metrics['mape']:.2f}%")
    print(f"   CV R² (5-fold):   {model_metrics['cv_r2_mean']:.4f} ± {model_metrics['cv_r2_std']:.4f}")
    print()

print("=" * 80)
print(f"🏆 MEJOR MODELO: {model.best_model_name.upper().replace('_', ' ')}")
print("=" * 80)
best_metrics = metrics[model.best_model_name]
print(f"   R² Score:        {best_metrics['r2']:.4f}")
print(f"   MAE:              ${best_metrics['mae']:,.2f}")
print(f"   RMSE:             ${best_metrics['rmse']:,.2f}")
print(f"   MAPE:             {best_metrics['mape']:.2f}%")
print(f"   CV R² (5-fold):   {best_metrics['cv_r2_mean']:.4f} ± {best_metrics['cv_r2_std']:.4f}")
print()

# Guardar el modelo
print("💾 Guardando modelo entrenado...")
model.save()
print(f"   ✓ Modelo guardado en: {model.model_dir}/economic_impact_model.pkl")
print()

# Mostrar información del dataset
print("=" * 80)
print("📋 INFORMACIÓN DEL DATASET")
print("=" * 80)
print(f"   Total de muestras: {len(df_training)}")
print(f"   Total de features: {len(model.feature_columns)}")
print(f"   Features básicas: 13")
print(f"   Features de métricas: {len(model.feature_columns) - 13}")
print()

# Mostrar algunas features importantes
print("🔍 Algunas features importantes:")
print(f"   - Event characteristics: attendance, duration_days, event_type_encoded, etc.")
print(f"   - City characteristics: population, annual_tourists, hotel_rooms, etc.")
print(f"   - Tourism metrics: event_avg_total_visitors, visitor_increase_actual, etc.")
print(f"   - Hotel metrics: event_avg_occupancy_pct, occupancy_boost_actual, etc.")
print(f"   - Economic metrics: event_avg_daily_spending, daily_spending_increase_pct, etc.")
print(f"   - Mobility metrics: event_avg_airport_arrivals, airport_arrivals_increase_pct, etc.")
print()

print("=" * 80)
print("✅ ENTRENAMIENTO COMPLETADO")
print("=" * 80)

