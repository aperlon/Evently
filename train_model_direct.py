#!/usr/bin/env python3
"""
Script directo para entrenar el modelo de regresión y mostrar rendimiento
"""
import sys
import os
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    from app.ml.economic_impact_model import EconomicImpactModel
    
    print('=' * 70)
    print('🚀 ENTRENANDO MODELO DE REGRESIÓN')
    print('=' * 70)
    
    # Inicializar modelo
    model = EconomicImpactModel()
    
    # Cargar datos desde CSVs
    print('\n📂 Cargando datos desde CSVs...')
    model.load_data()
    
    # Entrenar modelo
    print('\n🤖 Entrenando modelos...')
    metrics = model.train()
    
    # Mostrar resumen
    print('\n' + '=' * 70)
    print('📊 RESUMEN DEL ENTRENAMIENTO')
    print('=' * 70)
    
    print(f'\n🏆 Mejor Modelo: {model.best_model_name}')
    print(f'   R² Score: {metrics[model.best_model_name]["r2"]:.4f}')
    print(f'   MAE: ${metrics[model.best_model_name]["mae"]:,.0f}')
    print(f'   RMSE: ${metrics[model.best_model_name]["rmse"]:,.0f}')
    print(f'   MAPE: {metrics[model.best_model_name]["mape"]:.2f}%')
    print(f'   CV R² (5-fold): {metrics[model.best_model_name]["cv_r2_mean"]:.4f} ± {metrics[model.best_model_name]["cv_r2_std"]:.4f}')
    
    print('\n📈 Comparación de Todos los Modelos:')
    print('-' * 70)
    print(f'{"Modelo":<25s} | {"R²":<8s} | {"MAPE":<8s} | {"RMSE":<20s} | {"MAE":<20s}')
    print('-' * 70)
    for name, m in metrics.items():
        print(f'{name:<25s} | {m["r2"]:>6.4f} | {m["mape"]:>6.2f}% | ${m["rmse"]:>18,.0f} | ${m["mae"]:>18,.0f}')
    
    # Guardar modelo
    model.save()
    print('\n✅ Modelo guardado en: backend/app/ml/saved_models/economic_impact_model.pkl')
    
    # Mostrar importancia de features si es tree-based
    if hasattr(model.best_model, 'feature_importances_'):
        print('\n📊 Importancia de Features (Top 10):')
        print('-' * 70)
        importance = model.best_model.feature_importances_
        indices = sorted(range(len(importance)), key=lambda i: importance[i], reverse=True)
        for i, idx in enumerate(indices[:10]):
            feature_name = model.feature_columns[idx]
            print(f'{i+1:2d}. {feature_name:30s} : {importance[idx]:.4f} ({importance[idx]*100:.2f}%)')
    
    # Mostrar ejemplo de predicción
    print('\n🧪 Ejemplo de Predicción:')
    print('-' * 70)
    test_event = {
        'event_type': 'sports',
        'city': 'London',
        'duration_days': 7,
        'attendance': 50000
    }
    result = model.predict_simple(**test_event)
    print(f"Evento: {test_event['event_type']} en {test_event['city']}")
    print(f"Duración: {test_event['duration_days']} días")
    print(f"Asistencia: {test_event['attendance']:,}")
    print(f"\n💰 Impacto Económico Predicho: ${result['prediction']['total_economic_impact_usd']:,.0f}")
    print(f"   Intervalo: ${result['prediction']['lower_bound_usd']:,.0f} - ${result['prediction']['upper_bound_usd']:,.0f}")
    print(f"   Empleos creados: {result['estimates']['jobs_created']:,}")
    print(f"   ROI: {result['estimates']['roi_ratio']:.2f}x")
    print(f"   Modelo usado: {result['model_info']['model_used']}")
    print(f"   R² del modelo: {result['model_info']['model_r2']:.4f}")
    
    print('\n' + '=' * 70)
    print('✅ Entrenamiento completado exitosamente!')
    print('=' * 70)
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n💡 Asegúrate de tener las dependencias instaladas:")
    print("   pip install scikit-learn pandas numpy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

