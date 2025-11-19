import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { apiService } from '../services/api'
import { format } from 'date-fns'

function EventDetails() {
  const { id } = useParams<{ id: string }>()
  const eventId = parseInt(id || '0')

  const { data: event, isLoading: eventLoading } = useQuery({
    queryKey: ['event', eventId],
    queryFn: () => apiService.getEvent(eventId),
  })

  const { data: impact, isLoading: impactLoading } = useQuery({
    queryKey: ['eventImpact', eventId],
    queryFn: () => apiService.getEventImpact(eventId),
  })

  if (eventLoading || impactLoading) {
    return <div className="text-center py-12">Loading event details...</div>
  }

  // Calcular períodos basados en las fechas del evento
  const getPeriods = () => {
    if (!event?.start_date) return null

    const eventStart = new Date(event.start_date)
    const eventEnd = new Date(event.end_date || event.start_date)
    
    // Baseline: 44 días antes hasta 14 días antes del evento (30 días)
    const baselineStart = new Date(eventStart)
    baselineStart.setDate(baselineStart.getDate() - 44)
    
    const baselineEnd = new Date(eventStart)
    baselineEnd.setDate(baselineEnd.getDate() - 14)

    return {
      baseline: {
        start: baselineStart,
        end: baselineEnd,
      },
      event: {
        start: eventStart,
        end: eventEnd,
      },
    }
  }

  const periods = getPeriods()

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold">{event?.name}</h2>
        <p className="text-gray-600 mt-2">{event?.event_type}</p>
      </div>

      {impact && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="card">
              <h4 className="text-sm text-gray-600">Economic Impact</h4>
              <p className="text-2xl font-bold text-green-600">
                ${(impact.total_economic_impact_usd || 0).toLocaleString()}
              </p>
            </div>
            <div className="card">
              <h4 className="text-sm text-gray-600">Visitor Increase</h4>
              <p className="text-2xl font-bold text-blue-600">
                +{(impact.visitor_increase_pct || 0).toFixed(1)}%
              </p>
            </div>
            <div className="card">
              <h4 className="text-sm text-gray-600">Jobs Created</h4>
              <p className="text-2xl font-bold text-purple-600">
                {(impact.jobs_created || 0).toLocaleString()}
              </p>
            </div>
          </div>

          {/* Nueva sección con promedios diarios */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="card">
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                Promedio Diario Baseline
              </h4>
              <p className="text-3xl font-bold text-gray-900 mb-2">
                {impact.baseline_daily_visitors?.toLocaleString() || 'N/A'}
              </p>
              <p className="text-xs text-gray-500">
                visitantes/día
              </p>
              {periods && (
                <p className="text-xs text-gray-400 mt-2">
                  Período: {format(periods.baseline.start, 'dd MMM yyyy')} - {format(periods.baseline.end, 'dd MMM yyyy')}
                </p>
              )}
            </div>

            <div className="card">
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                Promedio Diario Durante Evento
              </h4>
              <p className="text-3xl font-bold text-blue-600 mb-2">
                {impact.event_period_daily_visitors?.toLocaleString() || 'N/A'}
              </p>
              <p className="text-xs text-gray-500">
                visitantes/día
              </p>
              {periods && (
                <p className="text-xs text-gray-400 mt-2">
                  Período: {format(periods.event.start, 'dd MMM yyyy')} - {format(periods.event.end, 'dd MMM yyyy')}
                </p>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default EventDetails
