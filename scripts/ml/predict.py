#!/usr/bin/env python3
"""
Evently - Predictor Interactivo de Impacto Económico
Uso: python predict.py
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "backend"))
from app.ml.economic_impact_model import EconomicImpactModel

def main():
    print("\n" + "="*60)
    print("   EVENTLY - Predictor de Impacto Económico")
    print("="*60)

    # Cargar modelo
    model = EconomicImpactModel()
    model.load()

    event_types = model.get_event_types()
    cities = [c['name'] for c in model.get_cities()]

    while True:
        print("\n" + "-"*60)
        print("NUEVA PREDICCIÓN (escribe 'salir' para terminar)")
        print("-"*60)

        # Tipo de evento
        print(f"\nTipos disponibles: {', '.join(event_types)}")
        event_type = input("Tipo de evento: ").strip().lower()
        if event_type == 'salir':
            break
        if event_type not in event_types:
            print(f"❌ Tipo no válido. Usa: {event_types}")
            continue

        # Ciudad
        print(f"\nCiudades: {', '.join(cities)}")
        city = input("Ciudad: ").strip()
        # Capitalizar primera letra de cada palabra
        city = ' '.join(word.capitalize() for word in city.split())
        if city not in cities:
            print(f"❌ Ciudad no encontrada. Ciudades válidas: {cities}")
            continue

        # Duración
        try:
            days = int(input("Duración (días): ").strip())
            if days < 1 or days > 365:
                print("❌ Duración debe ser entre 1 y 365 días")
                continue
        except ValueError:
            print("❌ Ingresa un número válido")
            continue

        # Asistencia (opcional)
        attendance_str = input("Asistencia esperada (Enter para auto-estimar): ").strip()
        attendance = int(attendance_str) if attendance_str else None

        # Hacer predicción
        print("\n⏳ Calculando predicción...")
        result = model.predict_simple(event_type, city, days, attendance)

        # Mostrar resultados
        print("\n" + "="*60)
        print(f"   RESULTADO: {event_type.upper()} en {city} ({days} días)")
        print("="*60)

        print(f"\n💰 IMPACTO ECONÓMICO TOTAL: ${result['prediction']['total_economic_impact_usd']:,.0f}")
        print(f"\n📊 Intervalo de confianza (90%):")
        print(f"   ${result['prediction']['lower_bound_usd']:,.0f} - ${result['prediction']['upper_bound_usd']:,.0f}")

        print(f"\n📈 Desglose:")
        print(f"   Directo:   ${result['breakdown']['direct_spending_usd']:,.0f}")
        print(f"   Indirecto: ${result['breakdown']['indirect_spending_usd']:,.0f}")
        print(f"   Inducido:  ${result['breakdown']['induced_spending_usd']:,.0f}")

        print(f"\n👥 Estimaciones:")
        print(f"   Empleos creados: {result['estimates']['jobs_created']:,}")
        print(f"   ROI: {result['estimates']['roi_ratio']}x")

        ref = result['historical_reference']
        print(f"\n📚 Basado en: {ref['reference_scope']}")
        if ref['similar_events']:
            print(f"   Eventos similares: {', '.join(ref['similar_events'][:3])}")

    print("\n¡Hasta pronto!\n")

if __name__ == "__main__":
    main()
