import { useQuery } from '@tanstack/react-query'
import { apiService } from '../services/api'

function Dashboard() {
  const { data: kpis, isLoading, error } = useQuery({
    queryKey: ['dashboardKPIs'],
    queryFn: () => apiService.getDashboardKPIs(),
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
        <h2 className="text-3xl font-display text-gray-900">Event Impact Dashboard</h2>
        <p className="mt-2 text-gray-600 font-mono">
          Overview of economic and touristic impact across major urban events
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="card bg-gradient-to-br from-mellow-ice to-mellow-cream border border-mellow-ice shadow-lg">
          <h3 className="text-sm font-mono font-medium text-gray-700">Total Events Analyzed</h3>
          <p className="text-4xl font-display text-gray-900 mt-2">{kpis?.total_events_analyzed || 0}</p>
          <p className="text-sm font-mono text-gray-600 mt-2">
            {kpis?.total_cities || 0} cities in system
          </p>
        </div>

        <div className="card bg-gradient-to-br from-mellow-cream to-mellow-peach border border-mellow-peach shadow-lg">
          <h3 className="text-sm font-mono font-medium text-gray-700">Avg Economic Impact</h3>
          <p className="text-4xl font-display text-gray-900 mt-2">
            ${(kpis?.avg_economic_impact_per_event_usd || 0).toLocaleString('en-US', {
              maximumFractionDigits: 0,
            })}
          </p>
          <p className="text-sm font-mono text-gray-600 mt-2">Per event</p>
        </div>

        <div className="card bg-gradient-to-br from-mellow-peach to-mellow-cream border border-mellow-peach shadow-lg">
          <h3 className="text-sm font-mono font-medium text-gray-700">Total Jobs Created</h3>
          <p className="text-4xl font-display text-gray-900 mt-2">
            {(kpis?.total_jobs_created || 0).toLocaleString()}
          </p>
          <p className="text-sm font-mono text-gray-600 mt-2">From all events</p>
        </div>

        <div className="card bg-gradient-to-br from-mellow-ice to-mellow-peach border border-mellow-ice shadow-lg">
          <h3 className="text-sm font-mono font-medium text-gray-700">Avg Visitor Increase</h3>
          <p className="text-4xl font-display text-gray-900 mt-2">
            +{(kpis?.avg_visitor_increase_pct || 0).toFixed(1)}%
          </p>
          <p className="text-sm font-mono text-gray-600 mt-2">During events</p>
        </div>

        <div className="card bg-gradient-to-br from-mellow-cream to-mellow-ice border border-mellow-cream shadow-lg">
          <h3 className="text-sm font-mono font-medium text-gray-700">Avg Hotel Price Increase</h3>
          <p className="text-4xl font-display text-gray-900 mt-2">
            +{(kpis?.avg_hotel_price_increase_pct || 0).toFixed(1)}%
          </p>
          <p className="text-sm font-mono text-gray-600 mt-2">During events</p>
        </div>

        <div className="card bg-gradient-mellow border border-mellow-peach shadow-lg">
          <h3 className="text-sm font-mono font-medium text-gray-700">Cities</h3>
          <p className="text-4xl font-display text-gray-900 mt-2">{kpis?.total_cities || 0}</p>
          <p className="text-sm font-mono text-gray-600 mt-2">Worldwide coverage</p>
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
