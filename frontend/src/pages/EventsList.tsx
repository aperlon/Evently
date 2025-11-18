import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { apiService, Event } from '../services/api'
import { format } from 'date-fns'

function EventsList() {
  const { data: events, isLoading, error } = useQuery({
    queryKey: ['events'],
    queryFn: apiService.getEvents,
  })

  if (isLoading) {
    return <div className="text-center py-12">Loading events...</div>
  }

  if (error) {
    return (
      <div className="card bg-red-50">
        <p className="text-red-600">Error loading events</p>
      </div>
    )
  }

  const groupedByCity = events?.reduce((acc, event) => {
    const cityId = event.city_id
    if (!acc[cityId]) {
      acc[cityId] = []
    }
    acc[cityId].push(event)
    return acc
  }, {} as Record<number, Event[]>)

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold">Events Catalog</h2>
        <p className="text-gray-600 mt-2">
          Browse all analyzed events across major cities
        </p>
      </div>

      <div className="grid gap-6">
        {events?.map((event) => (
          <Link
            key={event.id}
            to={`/events/${event.id}`}
            className="card hover:shadow-lg transition-shadow"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="text-xl font-semibold text-gray-900">{event.name}</h3>
                <div className="mt-2 flex items-center gap-4 text-sm text-gray-600">
                  <span className="flex items-center">
                    <svg
                      className="w-4 h-4 mr-1"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    {format(new Date(event.start_date), 'MMM dd, yyyy')}
                    {event.start_date !== event.end_date &&
                      ` - ${format(new Date(event.end_date), 'MMM dd, yyyy')}`}
                  </span>
                  <span className="flex items-center">
                    <svg
                      className="w-4 h-4 mr-1"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                      />
                    </svg>
                    {(event.actual_attendance || event.expected_attendance)?.toLocaleString()}{' '}
                    attendees
                  </span>
                </div>
              </div>
              <div>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800">
                  {event.event_type}
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default EventsList
