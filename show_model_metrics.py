python backend/train_model.py
"""
Script para mostrar métricas del modelo guardado sin necesidad de entrenar
Usa pickle para cargar el modelo y mostrar sus métricas
"""
import pickle
import sys
from pathlib import Path

model_path = Path("backend/app/ml/saved_models/economic_impact_model.pkl")

if not model_path.exists():
    print("❌ No se encontró modelo guardado.")
    print("   El modelo se entrenará automáticamente la primera vez que se use.")
    print("   O ejecuta: python backend/train_model.py (después de instalar dependencias)")
    sys.exit(1)

print("=" * 80)
print("📊 MÉTRICAS DEL MODELO GUARDADO")
print("=" * 80)
print()

try:
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    print(f"🏆 Mejor Modelo: {model_data.get('best_model_name', 'Unknown').upper().replace('_', ' ')}")
    print(f"📅 Entrenado: {model_data.get('trained_at', 'Unknown')}")
    print()
    
    if 'metrics' in model_data:
        print("=" * 80)
        print("📈 MÉTRICAS POR MODELO")
        print("=" * 80)
        print()
        
        for model_name, metrics in model_data['metrics'].items():
            print(f"📊 {model_name.upper().replace('_', ' ')}")
            print(f"   R² Score:        {metrics.get('r2', 0):.4f}")
            print(f"   MAE:              ${metrics.get('mae', 0):,.2f}")
            print(f"   RMSE:             ${metrics.get('rmse', 0):,.2f}")
            print(f"   MAPE:             {metrics.get('mape', 0):.2f}%")
            if 'cv_r2_mean' in metrics:
                print(f"   CV R² (5-fold):   {metrics['cv_r2_mean']:.4f} ± {metrics.get('cv_r2_std', 0):.4f}")
            print()
        
        # Mostrar mejor modelo
        best_name = model_data.get('best_model_name', '')
        if best_name and best_name in model_data['metrics']:
            best_metrics = model_data['metrics'][best_name]
            print("=" * 80)
            print(f"🏆 RESUMEN DEL MEJOR MODELO: {best_name.upper().replace('_', ' ')}")
            print("=" * 80)
            print(f"   R² Score:        {best_metrics.get('r2', 0):.4f}")
            print(f"   MAE:              ${best_metrics.get('mae', 0):,.2f}")
            print(f"   RMSE:             ${best_metrics.get('rmse', 0):,.2f}")
            print(f"   MAPE:             {best_metrics.get('mape', 0):.2f}%")
            if 'cv_r2_mean' in best_metrics:
                print(f"   CV R² (5-fold):   {best_metrics['cv_r2_mean']:.4f} ± {best_metrics.get('cv_r2_std', 0):.4f}")
            print()
    else:
        print("⚠️  No se encontraron métricas en el modelo guardado.")
        print("   El modelo necesita ser reentrenado con los nuevos CSVs.")
    
    if 'feature_columns' in model_data:
        print("=" * 80)
        print("📋 FEATURES DEL MODELO")
        print("=" * 80)
        print(f"   Total de features: {len(model_data['feature_columns'])}")
        print(f"   Features: {', '.join(model_data['feature_columns'][:10])}...")
        print()
    
except Exception as e:
    print(f"❌ Error leyendo modelo: {e}")
    import traceback
    traceback.print_exc()

print("=" * 80)
print("💡 NOTA: Este modelo fue entrenado ANTES de agregar los 4 CSVs adicionales")
print("   Para ver las nuevas métricas, necesitas reentrenar el modelo.")
print("   Instala dependencias: pip install scikit-learn pandas numpy")
print("   Luego ejecuta: python backend/train_model.py")
print("=" * 80)

