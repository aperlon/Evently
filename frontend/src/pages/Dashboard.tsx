import { useQuery } from '@tanstack/react-query'
import { apiService } from '../services/api'

function Dashboard() {
  const { data: kpis, isLoading, error } = useQuery({
    queryKey: ['dashboardKPIs'],
    queryFn: apiService.getDashboardKPIs,
  })

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">Loading dashboard...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card bg-red-50 border border-red-200">
        <h3 className="text-red-800 font-semibold">Error loading dashboard</h3>
        <p className="text-red-600 mt-2">
          {error instanceof Error ? error.message : 'Unknown error occurred'}
        </p>
        <p className="text-sm text-gray-600 mt-4">
          Make sure the backend is running and sample data has been generated.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Event Impact Dashboard</h2>
        <p className="mt-2 text-gray-600">
          Overview of economic and touristic impact across major urban events
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Total Events Analyzed</h3>
          <p className="text-4xl font-bold mt-2">{kpis?.total_events_analyzed || 0}</p>
          <p className="text-sm mt-2 opacity-75">Across {kpis?.total_cities || 0} cities</p>
        </div>

        <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Avg Economic Impact</h3>
          <p className="text-4xl font-bold mt-2">
            ${(kpis?.avg_economic_impact_per_event_usd || 0).toLocaleString('en-US', {
              maximumFractionDigits: 0,
            })}
          </p>
          <p className="text-sm mt-2 opacity-75">Per event</p>
        </div>

        <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Total Jobs Created</h3>
          <p className="text-4xl font-bold mt-2">
            {(kpis?.total_jobs_created || 0).toLocaleString()}
          </p>
          <p className="text-sm mt-2 opacity-75">From all events</p>
        </div>

        <div className="card bg-gradient-to-br from-orange-500 to-orange-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Avg Visitor Increase</h3>
          <p className="text-4xl font-bold mt-2">
            +{(kpis?.avg_visitor_increase_pct || 0).toFixed(1)}%
          </p>
          <p className="text-sm mt-2 opacity-75">During events</p>
        </div>

        <div className="card bg-gradient-to-br from-pink-500 to-pink-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Avg Hotel Price Increase</h3>
          <p className="text-4xl font-bold mt-2">
            +{(kpis?.avg_hotel_price_increase_pct || 0).toFixed(1)}%
          </p>
          <p className="text-sm mt-2 opacity-75">During events</p>
        </div>

        <div className="card bg-gradient-to-br from-indigo-500 to-indigo-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Cities</h3>
          <p className="text-4xl font-bold mt-2">{kpis?.total_cities || 0}</p>
          <p className="text-sm mt-2 opacity-75">Worldwide coverage</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a
            href="/events"
            className="p-4 border border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-md transition-all"
          >
            <h4 className="font-semibold text-gray-900">Browse Events</h4>
            <p className="text-sm text-gray-600 mt-1">
              Explore analyzed events across cities
            </p>
          </a>

          <a
            href="/compare"
            className="p-4 border border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-md transition-all"
          >
            <h4 className="font-semibold text-gray-900">Compare Cities</h4>
            <p className="text-sm text-gray-600 mt-1">
              Compare event impacts across different cities
            </p>
          </a>

          <a
            href="/simulator"
            className="p-4 border border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-md transition-all"
          >
            <h4 className="font-semibold text-gray-900">What-If Simulator</h4>
            <p className="text-sm text-gray-600 mt-1">
              Simulate scenarios and project outcomes
            </p>
          </a>
        </div>
      </div>

      {/* Info Section */}
      <div className="card bg-blue-50 border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-900">About Evently</h3>
        <p className="text-blue-800 mt-2">
          Evently analyzes the economic and touristic impact of major urban events across
          global cities. The platform tracks metrics like tourism flows, hotel demand,
          pricing, economic activity, and mobility patterns to help governments,
          organizers, and consultants make data-driven decisions.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          <span className="px-3 py-1 bg-blue-200 text-blue-800 rounded-full text-sm">
            Tourism Analysis
          </span>
          <span className="px-3 py-1 bg-blue-200 text-blue-800 rounded-full text-sm">
            Hotel Metrics
          </span>
          <span className="px-3 py-1 bg-blue-200 text-blue-800 rounded-full text-sm">
            Economic Impact
          </span>
          <span className="px-3 py-1 bg-blue-200 text-blue-800 rounded-full text-sm">
            Mobility Tracking
          </span>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
