"""
Actualizar events.csv con los nuevos eventos de event_impacts.csv
"""
import pandas as pd
from pathlib import Path

data_dir = Path("data/examples")
impacts_df = pd.read_csv(data_dir / "event_impacts.csv")
events_df = pd.read_csv(data_dir / "events.csv")

print("=" * 80)
print("📊 ACTUALIZANDO events.csv")
print("=" * 80)
print(f"Eventos en impacts: {len(impacts_df)}")
print(f"Eventos en events: {len(events_df)}")
print()

# Obtener eventos existentes
existing_event_names = set(events_df['event_name'].tolist())

# Generar nuevos eventos para los que no existen
new_events = []
for _, impact in impacts_df.iterrows():
    if impact['event_name'] not in existing_event_names:
        # Generar fechas basadas en el mes (distribuir a lo largo del año)
        import random
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        
        from datetime import datetime, timedelta
        start_date = datetime(2024, month, day)
        end_date = start_date + timedelta(days=int(impact['duration_days']) - 1)
        
        # Estimar attendance si no está
        attendance = impact.get('attendance', 50000)
        
        new_events.append({
            'event_name': impact['event_name'],
            'city': impact['city'],
            'event_type': impact['event_type'],
            'description': f"{impact['event_type'].capitalize()} event in {impact['city']}",
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'year': 2024,
            'expected_attendance': attendance,
            'actual_attendance': attendance,
            'venue_name': f"{impact['city']} City Center",
            'venue_capacity': '',
            'is_recurring': 0,
            'recurrence_pattern': '',
            'edition_number': ''
        })

if new_events:
    new_events_df = pd.DataFrame(new_events)
    combined_events = pd.concat([events_df, new_events_df], ignore_index=True)
    combined_events.to_csv(data_dir / "events.csv", index=False)
    
    print(f"✅ Añadidos {len(new_events)} nuevos eventos a events.csv")
    print(f"   Total eventos: {len(combined_events)}")
else:
    print("✅ Todos los eventos ya existen en events.csv")

print()
print("=" * 80)
print("✅ COMPLETADO")
print("=" * 80)

