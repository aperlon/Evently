# 📊 Cálculo del "Visitor Increase" (Aumento de Visitantes)

## 🔍 Fórmula

El **Visitor Increase** se calcula comparando el promedio de visitantes diarios durante el evento vs. el promedio de visitantes diarios en el período baseline (antes del evento).

```python
visitor_increase_pct = (
    ((event_avg_visitors - baseline_avg_visitors) / baseline_avg_visitors) * 100
    if baseline_avg_visitors > 0
    else 0
)
```

## 📅 Períodos de Análisis

### **Período Baseline (Dato Base)**
- **Inicio**: `event.start_date - 44 días` (14 días de ventana + 30 días adicionales)
- **Fin**: `event.start_date - 14 días`
- **Duración**: 30 días
- **Propósito**: Representa el nivel "normal" de visitantes antes del evento

### **Período del Evento**
- **Inicio**: `event.start_date`
- **Fin**: `event.end_date`
- **Duración**: Duración del evento
- **Propósito**: Representa el nivel de visitantes durante el evento

## 📈 Ejemplo Práctico

Supongamos un evento que ocurre del **1 al 5 de abril**:

### Timeline:
```
Baseline: 18 feb - 19 mar (30 días)    |    Gap: 20-31 mar (14 días)    |    Evento: 1-5 abr
```

### Cálculo:
1. **Baseline promedio diario**: Se promedian todos los `total_visitors` de la tabla `tourism_metrics` entre el 18 de febrero y el 19 de marzo
   - Ejemplo: 10,000 visitantes/día promedio

2. **Evento promedio diario**: Se promedian todos los `total_visitors` durante el evento (1-5 abril)
   - Ejemplo: 15,190 visitantes/día promedio

3. **Cálculo del aumento**:
   ```
   visitor_increase_pct = ((15,190 - 10,000) / 10,000) * 100
                        = (5,190 / 10,000) * 100
                        = 51.9%
   ```

## 🗄️ Fuente de Datos

Los datos provienen de la tabla `tourism_metrics` que contiene:
- `city_id`: ID de la ciudad
- `date`: Fecha de la métrica
- `total_visitors`: Número total de visitantes ese día

## 📝 Código Fuente

**Archivo**: `backend/app/analytics/impact_analyzer.py`

**Método**: `_calculate_tourism_impact()` (líneas 95-158)

```python
def _calculate_tourism_impact(
    self,
    city_id: int,
    baseline_start: date,  # event.start_date - 44 días
    baseline_end: date,    # event.start_date - 14 días
    event_start: date,     # event.start_date
    event_end: date,       # event.end_date
) -> Dict:
    # 1. Obtener métricas del baseline
    baseline_metrics = db.query(TourismMetric)
        .filter(city_id == city_id)
        .filter(date >= baseline_start, date <= baseline_end)
        .all()
    
    # 2. Obtener métricas del evento
    event_metrics = db.query(TourismMetric)
        .filter(city_id == city_id)
        .filter(date >= event_start, date <= event_end)
        .all()
    
    # 3. Calcular promedios
    baseline_avg_visitors = np.mean([m.total_visitors for m in baseline_metrics])
    event_avg_visitors = np.mean([m.total_visitors for m in event_metrics])
    
    # 4. Calcular porcentaje de aumento
    visitor_increase_pct = (
        ((event_avg_visitors - baseline_avg_visitors) / baseline_avg_visitors) * 100
        if baseline_avg_visitors > 0
        else 0
    )
    
    return {
        "baseline_daily_visitors": int(baseline_avg_visitors),
        "event_period_daily_visitors": int(event_avg_visitors),
        "visitor_increase_pct": round(visitor_increase_pct, 2),
        "additional_visitors": int((event_avg_visitors - baseline_avg_visitors) * len(event_metrics)),
    }
```

## ⚙️ Configuración

Los períodos se configuran en `backend/app/core/config.py`:

```python
EVENT_IMPACT_WINDOW_BEFORE_DAYS: int = 14  # Días antes del evento (gap)
EVENT_IMPACT_WINDOW_AFTER_DAYS: int = 14   # Días después del evento (análisis post)
```

El baseline usa: `window_before + 30 días` hacia atrás desde el inicio del evento.

## 🎯 Resumen

**Dato Base (Baseline)**:
- Promedio diario de visitantes en los **30 días** anteriores al período de ventana
- Período: desde `(inicio_evento - 44 días)` hasta `(inicio_evento - 14 días)`
- Representa el nivel "normal" de turismo sin el evento

**Cálculo**:
```
Visitor Increase % = ((Promedio durante evento - Promedio baseline) / Promedio baseline) × 100
```

**Ejemplo con +51.9%**:
- Baseline: 10,000 visitantes/día
- Durante evento: 15,190 visitantes/día
- Aumento: (15,190 - 10,000) / 10,000 = 51.9%

