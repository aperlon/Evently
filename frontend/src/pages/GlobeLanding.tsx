import { useEffect, useRef, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import Globe from 'react-globe.gl'
import { apiService, City } from '../services/api'

interface GlobePoint {
  lat: number
  lng: number
  size: number
  color: string
  city: City
}

function GlobeLanding() {
  const globeEl = useRef<any>()
  const [selectedCity, setSelectedCity] = useState<City | null>(null)
  const [dimensions, setDimensions] = useState({
    width: window.innerWidth * 0.65,
    height: window.innerHeight - 100,
  })

  // Fetch cities
  const { data: cities, isLoading } = useQuery({
    queryKey: ['cities'],
    queryFn: apiService.getCities,
  })

  // Convert cities to globe points
  const points: GlobePoint[] =
    cities?.map((city) => ({
      lat: city.latitude,
      lng: city.longitude,
      size: 0.5,
      color: '#ef4444', // red-500
      city,
    })) || []

  // Auto-rotate globe
  useEffect(() => {
    if (globeEl.current) {
      globeEl.current.controls().autoRotate = true
      globeEl.current.controls().autoRotateSpeed = 0.5
    }
  }, [])

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      setDimensions({
        width: window.innerWidth * 0.65,
        height: window.innerHeight - 100,
      })
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl text-gray-600">Loading globe...</div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Globe Section */}
      <div className="flex-1 flex flex-col items-center justify-center relative">
        {/* Title Overlay */}
        <div className="absolute top-8 left-8 z-10">
          <h1 className="text-5xl font-bold text-white mb-2">
            Evently
          </h1>
          <p className="text-xl text-blue-200">
            Global Event Impact Analyzer
          </p>
          <div className="mt-4 flex gap-2">
            <span className="px-3 py-1 bg-red-500 bg-opacity-20 border border-red-500 rounded-full text-red-300 text-sm">
              📍 {cities?.length || 0} Cities
            </span>
            <span className="px-3 py-1 bg-blue-500 bg-opacity-20 border border-blue-500 rounded-full text-blue-300 text-sm">
              🌍 Global Coverage
            </span>
          </div>
        </div>

        {/* Globe */}
        <Globe
          ref={globeEl}
          width={dimensions.width}
          height={dimensions.height}
          globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
          backgroundImageUrl="//unpkg.com/three-globe/example/img/night-sky.png"
          pointsData={points}
          pointLat={(d: any) => d.lat}
          pointLng={(d: any) => d.lng}
          pointColor={(d: any) => d.color}
          pointAltitude={0.02}
          pointRadius={(d: any) => d.size}
          pointLabel={(d: any) => `
            <div style="
              background: rgba(0, 0, 0, 0.8);
              padding: 12px;
              border-radius: 8px;
              color: white;
              font-family: sans-serif;
              border: 2px solid #ef4444;
            ">
              <div style="font-weight: bold; font-size: 16px; margin-bottom: 4px;">
                ${d.city.name}
              </div>
              <div style="font-size: 12px; opacity: 0.8;">
                ${d.city.country}
              </div>
              <div style="font-size: 11px; margin-top: 8px; opacity: 0.6;">
                Click for details →
              </div>
            </div>
          `}
          onPointClick={(point: any) => {
            setSelectedCity(point.city)
            // Zoom to city
            globeEl.current.pointOfView(
              {
                lat: point.lat,
                lng: point.lng,
                altitude: 2,
              },
              1000
            )
          }}
        />

        {/* Navigation hint */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-white text-sm opacity-60">
          <div className="flex items-center gap-2">
            <span>🖱️ Drag to rotate</span>
            <span>•</span>
            <span>📍 Click city for info</span>
            <span>•</span>
            <span>🔍 Scroll to zoom</span>
          </div>
        </div>
      </div>

      {/* City Info Panel */}
      <div className="w-[35%] bg-white overflow-y-auto">
        {selectedCity ? (
          <div className="p-8">
            {/* Header */}
            <div className="mb-6">
              <div className="flex items-start justify-between mb-2">
                <h2 className="text-4xl font-bold text-gray-900">
                  {selectedCity.name}
                </h2>
                <button
                  onClick={() => setSelectedCity(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              <p className="text-xl text-gray-600">
                {selectedCity.country}
              </p>
              <div className="mt-3 inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                {selectedCity.continent}
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
                <div className="text-sm text-blue-600 font-medium mb-1">
                  Population
                </div>
                <div className="text-2xl font-bold text-blue-900">
                  {(selectedCity.population / 1000000).toFixed(1)}M
                </div>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg">
                <div className="text-sm text-green-600 font-medium mb-1">
                  Annual Tourists
                </div>
                <div className="text-2xl font-bold text-green-900">
                  {(selectedCity.annual_tourists / 1000000).toFixed(1)}M
                </div>
              </div>

              <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg">
                <div className="text-sm text-purple-600 font-medium mb-1">
                  Hotel Rooms
                </div>
                <div className="text-2xl font-bold text-purple-900">
                  {(selectedCity.hotel_rooms / 1000).toFixed(0)}K
                </div>
              </div>

              <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-lg">
                <div className="text-sm text-orange-600 font-medium mb-1">
                  Avg Hotel Price
                </div>
                <div className="text-2xl font-bold text-orange-900">
                  ${selectedCity.avg_hotel_price_usd}
                </div>
              </div>
            </div>

            {/* Details */}
            <div className="space-y-4 text-sm">
              <div className="flex justify-between py-2 border-b">
                <span className="text-gray-600">Coordinates</span>
                <span className="font-medium text-gray-900">
                  {selectedCity.latitude.toFixed(4)}°, {selectedCity.longitude.toFixed(4)}°
                </span>
              </div>
              <div className="flex justify-between py-2 border-b">
                <span className="text-gray-600">Timezone</span>
                <span className="font-medium text-gray-900">
                  {selectedCity.timezone}
                </span>
              </div>
              <div className="flex justify-between py-2 border-b">
                <span className="text-gray-600">Country Code</span>
                <span className="font-medium text-gray-900">
                  {selectedCity.country_code}
                </span>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="mt-8 space-y-3">
              <a
                href={`/events?city=${selectedCity.name}`}
                className="block w-full btn-primary text-center"
              >
                View Events in {selectedCity.name}
              </a>
              <button className="w-full btn-secondary">
                Analyze Impact
              </button>
            </div>

            {/* Fun Fact */}
            <div className="mt-8 p-4 bg-gray-50 rounded-lg">
              <div className="text-xs text-gray-500 uppercase tracking-wide mb-1">
                Did you know?
              </div>
              <div className="text-sm text-gray-700">
                {selectedCity.name} attracts{' '}
                <span className="font-bold text-blue-600">
                  {(selectedCity.annual_tourists / 1000000).toFixed(1)} million
                </span>{' '}
                tourists annually, generating significant economic impact through
                major events and cultural activities.
              </div>
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center p-8 text-center">
            <div className="w-24 h-24 mb-6 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-4xl">
              🌍
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              Welcome to Evently
            </h3>
            <p className="text-gray-600 mb-8 max-w-md">
              Click on any red pin on the globe to explore how major events
              impact tourism, hotels, and local economies in cities worldwide.
            </p>

            <div className="space-y-3 w-full max-w-sm">
              <div className="text-left p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="text-3xl">📊</div>
                  <div>
                    <div className="font-semibold text-gray-900">
                      Real Data Analysis
                    </div>
                    <div className="text-sm text-gray-600">
                      Track tourism, hotels & economy
                    </div>
                  </div>
                </div>
              </div>

              <div className="text-left p-4 bg-purple-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="text-3xl">🎯</div>
                  <div>
                    <div className="font-semibold text-gray-900">
                      Event Impact Insights
                    </div>
                    <div className="text-sm text-gray-600">
                      Measure ROI and economic benefits
                    </div>
                  </div>
                </div>
              </div>

              <div className="text-left p-4 bg-green-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="text-3xl">🔮</div>
                  <div>
                    <div className="font-semibold text-gray-900">
                      What-If Scenarios
                    </div>
                    <div className="text-sm text-gray-600">
                      Simulate and forecast outcomes
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-8">
              <a
                href="/dashboard"
                className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Go to Dashboard →
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default GlobeLanding
