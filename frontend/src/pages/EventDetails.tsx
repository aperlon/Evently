import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { apiService } from '../services/api'

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

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold">{event?.name}</h2>
        <p className="text-gray-600 mt-2">{event?.event_type}</p>
      </div>

      {impact && (
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
      )}
    </div>
  )
}

export default EventDetails
