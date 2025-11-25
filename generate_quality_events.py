"""
Generar eventos de alta calidad basados en los CSVs de métricas reales
Objetivo: crear datos más realistas y consistentes
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random

# Cargar datos
data_dir = Path("data/examples")
impacts_df = pd.read_csv(data_dir / "event_impacts.csv")
cities_df = pd.read_csv(data_dir / "cities.csv")
tourism_df = pd.read_csv(data_dir / "tourism_metrics.csv")
hotel_df = pd.read_csv(data_dir / "hotel_metrics.csv")
economic_df = pd.read_csv(data_dir / "economic_metrics.csv")

# Convertir fechas
tourism_df['date'] = pd.to_datetime(tourism_df['date'])
hotel_df['date'] = pd.to_datetime(hotel_df['date'])
economic_df['date'] = pd.to_datetime(economic_df['date'])

print("=" * 80)
print("📊 GENERANDO EVENTOS DE ALTA CALIDAD")
print("=" * 80)
print(f"Eventos actuales: {len(impacts_df)}")
print()

# Obtener eventos existentes
existing_events = set(impacts_df['event_name'].tolist())

# Analizar eventos reales para entender patrones
real_events = impacts_df.head(12)  # Los 12 originales
avg_impact_per_attendance = (real_events['total_economic_impact_usd'] / real_events['attendance']).mean()
print(f"💰 Impacto promedio por asistente (eventos reales): ${avg_impact_per_attendance:.2f}")
print()

new_impacts = []
event_types = ['sports', 'music', 'festival', 'culture', 'conference', 'expo']
cities = cities_df['name'].tolist()

# Factores de impacto por tipo de evento (basados en eventos reales)
impact_factors = {
    'sports': 200,  # USD por asistente
    'music': 180,
    'festival': 150,
    'culture': 220,
    'conference': 250,
    'expo': 190
}

# Generar eventos más realistas
for city in cities:
    for event_type in event_types:
        # Generar 3-5 eventos por ciudad/tipo distribuidos a lo largo del año
        num_events = random.randint(3, 5)
        
        for i in range(num_events):
            # Distribuir eventos a lo largo del año
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            start_date = datetime(2024, month, day)
            
            # Duración realista según tipo
            if event_type in ['sports']:
                duration = random.choice([1, 2, 3, 7, 14])
            elif event_type in ['music', 'festival']:
                duration = random.choice([1, 2, 3, 4, 5])
            elif event_type == 'conference':
                duration = random.choice([2, 3, 4, 5])
            else:
                duration = random.choice([1, 2, 3, 4])
            
            end_date = start_date + timedelta(days=int(duration) - 1)
            
            # Obtener métricas reales del período
            event_tourism = tourism_df[
                (tourism_df['city'] == city) &
                (tourism_df['date'] >= start_date) &
                (tourism_df['date'] <= end_date)
            ]
            
            event_economic = economic_df[
                (economic_df['city'] == city) &
                (economic_df['date'] >= start_date) &
                (economic_df['date'] <= end_date)
            ]
            
            baseline_start = start_date - timedelta(days=30)
            baseline_end = start_date - timedelta(days=1)
            
            baseline_tourism = tourism_df[
                (tourism_df['city'] == city) &
                (tourism_df['date'] >= baseline_start) &
                (tourism_df['date'] <= baseline_end)
            ]
            
            baseline_economic = economic_df[
                (economic_df['city'] == city) &
                (economic_df['date'] >= baseline_start) &
                (economic_df['date'] <= baseline_end)
            ]
            
            if len(event_tourism) == 0 or len(baseline_tourism) == 0:
                continue
            
            # Calcular métricas reales
            event_avg_visitors = event_tourism['total_visitors'].mean()
            baseline_avg_visitors = baseline_tourism['total_visitors'].mean()
            visitor_increase_pct = ((event_avg_visitors / max(baseline_avg_visitors, 1)) - 1) * 100
            
            # Estimar attendance de forma más realista
            # Basado en el aumento de visitantes durante el evento
            if visitor_increase_pct > 10:  # Hay un evento significativo
                attendance = int(event_avg_visitors * duration * 1.3)
            else:
                # Evento pequeño
                attendance = int(baseline_avg_visitors * duration * 1.1)
            
            # Asegurar attendance mínimo y máximo realista
            attendance = max(5000, min(attendance, 2000000))
            
            # Calcular impacto económico de forma más precisa
            if len(event_economic) > 0 and len(baseline_economic) > 0:
                event_avg_spending = event_economic['total_spending_usd'].mean()
                baseline_avg_spending = baseline_economic['total_spending_usd'].mean()
                
                # Gasto adicional durante el evento
                additional_daily_spending = max(0, event_avg_spending - baseline_avg_spending)
                additional_total_spending = additional_daily_spending * duration
                
                # Si hay gasto adicional significativo, usarlo
                if additional_total_spending > 1000000:
                    total_impact = additional_total_spending * 1.7  # Multiplicador económico
                else:
                    # Calcular desde attendance y factor por tipo
                    base_impact = attendance * impact_factors.get(event_type, 200)
                    total_impact = base_impact * 1.7
            else:
                # Calcular desde attendance
                base_impact = attendance * impact_factors.get(event_type, 200)
                total_impact = base_impact * 1.7
            
            # Asegurar impacto mínimo y máximo realista
            total_impact = max(1000000, min(total_impact, 5000000000))
            
            # Jobs y ROI
            jobs_created = int(total_impact / 40000)
            roi_ratio = random.uniform(3.5, 5.5)
            
            # Nombre del evento
            event_name = f"{city} {event_type.capitalize()} {start_date.strftime('%B %Y')}"
            
            # Evitar duplicados
            if event_name in existing_events:
                # Añadir número de edición
                event_name = f"{city} {event_type.capitalize()} {start_date.strftime('%B %Y')} #{i+1}"
                if event_name in existing_events:
                    continue
            
            new_impacts.append({
                'event_name': event_name,
                'city': city,
                'event_type': event_type,
                'year': 2024,
                'attendance': attendance,
                'duration_days': duration,
                'total_economic_impact_usd': int(total_impact),
                'jobs_created': jobs_created,
                'roi_ratio': round(roi_ratio, 2)
            })
            
            existing_events.add(event_name)

print(f"✅ Generados {len(new_impacts)} nuevos eventos de alta calidad")
print()

# Combinar con existentes
new_impacts_df = pd.DataFrame(new_impacts)
combined_impacts = pd.concat([impacts_df, new_impacts_df], ignore_index=True)

# Guardar
output_path = data_dir / "event_impacts.csv"
combined_impacts.to_csv(output_path, index=False)

print(f"💾 Guardado en: {output_path}")
print(f"   Total eventos: {len(combined_impacts)}")
print(f"   Nuevos eventos: {len(new_impacts)}")
print()

# Estadísticas
print("=" * 80)
print("📊 ESTADÍSTICAS")
print("=" * 80)
print(f"   Impacto promedio: ${combined_impacts['total_economic_impact_usd'].mean():,.0f}")
print(f"   Impacto mediano: ${combined_impacts['total_economic_impact_usd'].median():,.0f}")
print(f"   Impacto mínimo: ${combined_impacts['total_economic_impact_usd'].min():,.0f}")
print(f"   Impacto máximo: ${combined_impacts['total_economic_impact_usd'].max():,.0f}")
print(f"   Attendance promedio: {combined_impacts['attendance'].mean():,.0f}")
print(f"   Duración promedio: {combined_impacts['duration_days'].mean():.1f} días")
print()

print("=" * 80)
print("✅ COMPLETADO")
print("=" * 80)

