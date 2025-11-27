"""
Ajustar los datos generados para que sean más consistentes y reentrenar
Usar fórmulas más precisas basadas en los eventos reales
"""
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "examples"
impacts_df = pd.read_csv(DATA_DIR / "event_impacts.csv")

print("=" * 80)
print("🔧 AJUSTANDO DATOS PARA CONSISTENCIA")
print("=" * 80)
print(f"Eventos totales: {len(impacts_df)}")
print()

# Analizar los 12 eventos reales
real_events = impacts_df.head(12).copy()
real_events['impact_per_attendance'] = real_events['total_economic_impact_usd'] / real_events['attendance']
real_events['impact_per_day'] = real_events['total_economic_impact_usd'] / real_events['duration_days']

# Calcular factores más precisos por tipo
factors_by_type = {}
for event_type in real_events['event_type'].unique():
    type_events = real_events[real_events['event_type'] == event_type]
    if len(type_events) > 0:
        factors_by_type[event_type] = {
            'per_attendance': type_events['impact_per_attendance'].median(),
            'per_day': type_events['impact_per_day'].median()
        }

print("📊 Factores por tipo de evento (eventos reales):")
for event_type, factors in factors_by_type.items():
    print(f"   {event_type}: ${factors['per_attendance']:.2f} por asistente, ${factors['per_day']:,.0f} por día")
print()

# Ajustar eventos generados para mayor consistencia
generated_events = impacts_df.iloc[12:].copy()
print(f"📝 Ajustando {len(generated_events)} eventos generados...")

# Recalcular impactos de forma más consistente
for idx, row in generated_events.iterrows():
    event_type = row['event_type']
    attendance = row['attendance']
    duration = row['duration_days']
    
    # Usar factores reales si están disponibles
    if event_type in factors_by_type:
        factor = factors_by_type[event_type]['per_attendance']
        # Calcular impacto base
        base_impact = attendance * factor
        # Aplicar variación pequeña (±20%)
        variation = np.random.uniform(0.85, 1.15)
        total_impact = base_impact * variation * 1.7  # Multiplicador económico
    else:
        # Usar mediana general
        median_factor = real_events['impact_per_attendance'].median()
        base_impact = attendance * median_factor
        variation = np.random.uniform(0.9, 1.1)
        total_impact = base_impact * variation * 1.7
    
    # Asegurar rango realista
    total_impact = max(1000000, min(total_impact, 5000000000))
    
    # Actualizar
    impacts_df.at[idx, 'total_economic_impact_usd'] = int(total_impact)
    impacts_df.at[idx, 'jobs_created'] = int(total_impact / 40000)
    impacts_df.at[idx, 'roi_ratio'] = round(np.random.uniform(3.8, 5.2), 2)

# Guardar
output_path = DATA_DIR / "event_impacts.csv"
impacts_df.to_csv(output_path, index=False)

print(f"✅ Datos ajustados y guardados")
print()

# Estadísticas finales
print("=" * 80)
print("📊 ESTADÍSTICAS DESPUÉS DEL AJUSTE")
print("=" * 80)
print(f"   Total eventos: {len(impacts_df)}")
print(f"   Impacto promedio: ${impacts_df['total_economic_impact_usd'].mean():,.0f}")
print(f"   Impacto mediano: ${impacts_df['total_economic_impact_usd'].median():,.0f}")
print(f"   Desviación estándar: ${impacts_df['total_economic_impact_usd'].std():,.0f}")
print(f"   Coeficiente de variación: {(impacts_df['total_economic_impact_usd'].std() / impacts_df['total_economic_impact_usd'].mean() * 100):.1f}%")
print()

# Comparar eventos reales vs generados
print("📊 Comparación:")
real_impact = impacts_df.head(12)['total_economic_impact_usd']
gen_impact = impacts_df.iloc[12:]['total_economic_impact_usd']
print(f"   Real - Promedio: ${real_impact.mean():,.0f}, Mediano: ${real_impact.median():,.0f}")
print(f"   Generado - Promedio: ${gen_impact.mean():,.0f}, Mediano: ${gen_impact.median():,.0f}")
print()

print("=" * 80)
print("✅ COMPLETADO - Listo para reentrenar")
print("=" * 80)

