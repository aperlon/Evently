import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { apiService } from '../services/api'
import { format } from 'date-fns'
import { getEventImage } from '../config/eventImages'

function EventsList() {
  const { data: events, isLoading, error } = useQuery({
    queryKey: ['events'],
    queryFn: () => apiService.getEvents(),
  })

  if (isLoading) {
    return <div className="text-center py-12">Loading events...</div>
  }

  if (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    const isNetworkError = errorMessage.includes('Network Error') || errorMessage.includes('Failed to fetch')
    
    return (
      <div className="card bg-red-50 border border-red-200">
        <div className="space-y-2">
          <p className="text-red-800 font-semibold">Error loading events</p>
          <p className="text-red-600 text-sm">
            {isNetworkError 
              ? 'Cannot connect to backend API. Please check:'
              : `Error: ${errorMessage}`}
          </p>
          {isNetworkError && (
            <ul className="text-red-600 text-sm list-disc list-inside mt-2 space-y-1">
              <li>Is the backend server running? (http://localhost:8000)</li>
              <li>Check browser console (F12) for more details</li>
              <li>Verify API URL in .env file: VITE_API_URL</li>
            </ul>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-display">Events Catalog</h2>
        <p className="text-gray-600 mt-2 font-mono">
          Browse all analyzed events across major cities
        </p>
      </div>

      <div className="grid gap-6">
        {events?.map((event) => (
          <Link
            key={event.id}
            to={`/events/${event.id}`}
            className="card hover:shadow-xl transition-all overflow-hidden group"
          >
            <div className="flex gap-4">
              {/* Event Image */}
              <div className="w-48 h-32 flex-shrink-0 overflow-hidden rounded-lg">
                <img
                  src={getEventImage(event.event_type)}
                  alt={event.name}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                />
              </div>

              {/* Event Info */}
              <div className="flex-1 flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-xl font-display text-gray-900">{event.name}</h3>
                  <div className="mt-2 flex items-center gap-4 text-sm text-gray-600 font-mono">
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
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-mono font-medium bg-mellow-cream text-gray-800 border border-mellow-peach">
                    {event.event_type}
                  </span>
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default EventsList
