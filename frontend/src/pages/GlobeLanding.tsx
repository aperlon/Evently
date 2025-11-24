import { useEffect, useRef, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import Globe from 'react-globe.gl'
import { motion } from 'framer-motion'
import { TrendingUp, DollarSign, Users, Globe2 } from 'lucide-react'
import { apiService, City } from '../services/api'
import * as THREE from 'three'

interface CityPoint {
  lat: number
  lng: number
  city: City
}

function GlobeLanding() {
  const globeEl = useRef<any>()
  const containerRef = useRef<HTMLDivElement>(null)
  const [selectedCity, setSelectedCity] = useState<City | null>(null)
  const [dimensions, setDimensions] = useState({
    width: window.innerWidth * 0.65,
    height: window.innerHeight,
  })

  // Fetch cities
  const { data: cities, isLoading } = useQuery({
    queryKey: ['cities'],
    queryFn: () => apiService.getCities(),
  })

  // Convert cities to points
  const pointsData: CityPoint[] =
    cities?.map((city) => ({
      lat: city.latitude,
      lng: city.longitude,
      city,
    })) || []

  // Create custom pin object (inverted teardrop shape) - 2.5x larger
  const createPinObject = () => {
    const group = new THREE.Group()
    
    // Create a proper teardrop shape using LatheGeometry
    // Define the profile of the teardrop (half profile, will be rotated)
    const points: THREE.Vector2[] = []
    const segments = 50
    
    // Create teardrop profile: circular top, smooth curve to sharp point
    // This creates a classic location pin shape
    for (let i = 0; i <= segments; i++) {
      const t = i / segments
      let x, y
      
      if (t < 0.2) {
        // Top circular section (hemisphere)
        const localT = t / 0.2
        const angle = localT * Math.PI / 2
        x = 2.2 * Math.sin(angle)
        y = 1.8 - (1.8 * localT)
      } else {
        // Body that tapers to a point (smooth curve)
        const localT = (t - 0.2) / 0.8
        // Use a smooth easing function for natural teardrop curve
        const ease = 1 - Math.pow(1 - localT, 2.5)
        x = 2.2 * (1 - ease)
        y = 0.0 - (3.7 * localT)
      }
      
      points.push(new THREE.Vector2(Math.max(0.01, x), y))
    }
    
    // Create lathe geometry from the profile
    const teardropGeometry = new THREE.LatheGeometry(points, 32)
    const teardropMaterial = new THREE.MeshPhongMaterial({
      color: '#F3A46C', // Orange color
      emissive: '#F3A46C',
      emissiveIntensity: 0.5,
      shininess: 100,
      side: THREE.DoubleSide,
    })
    const teardrop = new THREE.Mesh(teardropGeometry, teardropMaterial)
    teardrop.rotation.x = Math.PI // Flip to point down
    teardrop.position.y = 1.85 // Position so tip is at origin
    
    group.add(teardrop)
    
    return group
  }

  // Auto-rotate globe
  useEffect(() => {
    if (globeEl.current) {
      globeEl.current.controls().autoRotate = true
      globeEl.current.controls().autoRotateSpeed = 0.5
    }
  }, [])

  // Handle window resize and update dimensions based on container
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect()
        setDimensions({
          width: rect.width,
          height: rect.height,
        })
      }
    }
    
    updateDimensions()
    window.addEventListener('resize', updateDimensions)
    
    // Use ResizeObserver for more accurate container size tracking
    const resizeObserver = new ResizeObserver(updateDimensions)
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current)
    }
    
    return () => {
      window.removeEventListener('resize', updateDimensions)
      resizeObserver.disconnect()
    }
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl text-gray-600">Loading globe...</div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-black">
      {/* Globe Section */}
      <div 
        ref={containerRef}
        className="flex-1 flex flex-col items-center justify-center relative overflow-hidden"
      >
        {/* Hero Section with Stats */}
        <div className="absolute top-8 left-8 z-10 max-w-md">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="flex items-center gap-4 mb-4"
          >
            <img
              src="/media/IMAGESEVENTLY/LOGOEVENTLY.png"
              alt="Evently Logo"
              className="w-16 h-16 object-contain"
            />
            <h1 className="text-6xl font-display text-white leading-tight pt-4">
              Evently
            </h1>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <p className="text-2xl font-mono text-white mb-6">
              Global Event Impact Analyzer
            </p>
          </motion.div>

          {/* Impactful Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="grid grid-cols-2 gap-3 mb-4"
          >
            <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-peach border-opacity-30 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign className="w-5 h-5 text-mellow-peach" />
                <span className="text-xs font-mono text-gray-600 uppercase tracking-wide">
                  Total Impact
                </span>
              </div>
              <div className="text-3xl font-display text-gray-900">$12.4B</div>
              <div className="text-xs font-mono text-gray-500 mt-1">Analyzed to date</div>
            </div>

            <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-ice border-opacity-50 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <Users className="w-5 h-5 text-mellow-ice" />
                <span className="text-xs font-mono text-gray-600 uppercase tracking-wide">
                  Jobs Created
                </span>
              </div>
              <div className="text-3xl font-display text-gray-900">847K</div>
              <div className="text-xs font-mono text-gray-500 mt-1">From major events</div>
            </div>

            <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-cream border-opacity-50 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <Globe2 className="w-5 h-5 text-mellow-cream" />
                <span className="text-xs font-mono text-gray-600 uppercase tracking-wide">
                  Cities
                </span>
              </div>
              <div className="text-3xl font-display text-gray-900">{cities?.length || 0}</div>
              <div className="text-xs font-mono text-gray-500 mt-1">Worldwide coverage</div>
            </div>

            <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-peach border-opacity-30 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-mellow-peach" />
                <span className="text-xs font-mono text-gray-600 uppercase tracking-wide">
                  Avg ROI
                </span>
              </div>
              <div className="text-3xl font-display text-gray-900">420%</div>
              <div className="text-xs font-mono text-gray-500 mt-1">Return on investment</div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex gap-2"
          >
            <span className="px-3 py-1 bg-mellow-peach bg-opacity-30 border border-mellow-peach rounded-full text-gray-800 text-sm font-mono backdrop-blur-sm">
              📍 Real-time Data
            </span>
            <span className="px-3 py-1 bg-mellow-ice bg-opacity-40 border border-mellow-ice rounded-full text-gray-800 text-sm font-mono backdrop-blur-sm">
              🌍 5 Continents
            </span>
          </motion.div>
        </div>

        {/* Globe */}
        <div className="absolute inset-0 w-full h-full">
          <Globe
            ref={globeEl}
            width={dimensions.width}
            height={dimensions.height}
            globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
            backgroundImageUrl="//unpkg.com/three-globe/example/img/night-sky.png"
            showAtmosphere={true}
            atmosphereColor="#3b82f6"
            atmosphereAltitude={0.15}
            pointsData={pointsData}
            pointLat={(d: any) => d.lat}
            pointLng={(d: any) => d.lng}
            pointAltitude={0.05}
            pointRadius={1.2}
            pointColor={() => '#F3A46C'}
            pointResolution={8}
            pointObject={createPinObject}
            pointLabel={(d: any) => {
              const city = d.city
              if (!city) return ''
              return `
                <div style="
                  background: rgba(0, 0, 0, 0.9);
                  padding: 12px;
                  border-radius: 8px;
                  color: white;
                  font-family: sans-serif;
                  border: 2px solid #F3A46C;
                ">
                  <div style="font-weight: bold; font-size: 16px; margin-bottom: 4px;">
                    ${city.name}
                  </div>
                  <div style="font-size: 12px; opacity: 0.8;">
                    ${city.country}
                  </div>
                  <div style="font-size: 11px; margin-top: 8px; opacity: 0.6;">
                    Click for details →
                  </div>
                </div>
              `
            }}
            onPointClick={(point: any) => {
              const city = point.city
              if (city) {
                setSelectedCity(city)
                // Zoom to city
                globeEl.current.pointOfView(
                  {
                    lat: city.latitude,
                    lng: city.longitude,
                    altitude: 2,
                  },
                  1000
                )
              }
            }}
          />
        </div>

        {/* Navigation hint */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-white text-sm opacity-60">
          <div className="flex items-center gap-2">
            <span>🖱️ Drag to rotate</span>
            <span>•</span>
            <span>📍 Click pin for city info</span>
            <span>•</span>
            <span>🔍 Scroll to zoom</span>
          </div>
        </div>
      </div>

      {/* City Info Panel */}
      <div className="w-[35%] m-4 mr-6 my-6 bg-white bg-opacity-90 backdrop-blur-md overflow-y-auto rounded-3xl border border-mellow-ice border-opacity-40 shadow-2xl">
        {selectedCity ? (
          <div className="p-8">
            {/* Header */}
            <div className="mb-6">
              <div className="flex items-start justify-between mb-2">
                <h2 className="text-4xl font-display text-gray-900">
                  {selectedCity.name}
                </h2>
                <button
                  onClick={() => setSelectedCity(null)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  ✕
                </button>
              </div>
              <p className="text-xl font-mono text-gray-700 mb-3">
                {selectedCity.country}
              </p>
              <span className="px-3 py-1 bg-mellow-ice bg-opacity-40 border border-mellow-ice rounded-full text-gray-800 text-sm font-mono backdrop-blur-sm">
                {selectedCity.continent}
              </span>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-3 mb-6">
              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-peach border-opacity-30 shadow-lg">
                <div className="text-xs font-mono text-gray-600 uppercase tracking-wide mb-2">
                  Population
                </div>
                <div className="text-3xl font-display text-gray-900">
                  {(selectedCity.population / 1000000).toFixed(1)}M
                </div>
              </div>

              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-ice border-opacity-50 shadow-lg">
                <div className="text-xs font-mono text-gray-600 uppercase tracking-wide mb-2">
                  Annual Tourists
                </div>
                <div className="text-3xl font-display text-gray-900">
                  {(selectedCity.annual_tourists / 1000000).toFixed(1)}M
                </div>
              </div>

              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-cream border-opacity-50 shadow-lg">
                <div className="text-xs font-mono text-gray-600 uppercase tracking-wide mb-2">
                  Hotel Rooms
                </div>
                <div className="text-3xl font-display text-gray-900">
                  {(selectedCity.hotel_rooms / 1000).toFixed(0)}K
                </div>
              </div>

              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-peach border-opacity-30 shadow-lg">
                <div className="text-xs font-mono text-gray-600 uppercase tracking-wide mb-2">
                  Avg Hotel Price
                </div>
                <div className="text-3xl font-display text-gray-900">
                  ${selectedCity.avg_hotel_price_usd}
                </div>
              </div>
            </div>

            {/* Details */}
            <div className="space-y-3 mb-6">
              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-ice border-opacity-30 shadow-lg">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-mono text-gray-600 uppercase tracking-wide">Coordinates</span>
                  <span className="font-mono text-sm font-medium text-gray-900">
                    {selectedCity.latitude.toFixed(4)}°, {selectedCity.longitude.toFixed(4)}°
                  </span>
                </div>
              </div>
              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-ice border-opacity-30 shadow-lg">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-mono text-gray-600 uppercase tracking-wide">Timezone</span>
                  <span className="font-mono text-sm font-medium text-gray-900">
                    {selectedCity.timezone}
                  </span>
                </div>
              </div>
              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-ice border-opacity-30 shadow-lg">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-mono text-gray-600 uppercase tracking-wide">Country Code</span>
                  <span className="font-mono text-sm font-medium text-gray-900">
                    {selectedCity.country_code}
                  </span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="mt-8 space-y-3"
            >
              <a
                href={`/events?city=${selectedCity.name}`}
                className="block w-full px-6 py-3 bg-gradient-mellow border border-mellow-peach rounded-xl text-gray-900 font-mono hover:opacity-90 transition-all shadow-lg text-center"
              >
                View Events in {selectedCity.name}
              </a>
              <a
                href="/predict"
                className="block w-full px-6 py-3 bg-white bg-opacity-80 backdrop-blur-md border border-mellow-ice border-opacity-50 rounded-xl text-gray-900 font-mono hover:bg-opacity-100 transition-all shadow-lg text-center"
              >
                Analyze Impact
              </a>
            </motion.div>

            {/* Fun Fact */}
            <div className="mt-8 bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-ice border-opacity-30 shadow-lg">
              <div className="text-xs font-mono text-gray-600 uppercase tracking-wide mb-2">
                Did you know?
              </div>
              <div className="text-sm font-mono text-gray-700">
                {selectedCity.name} attracts{' '}
                <span className="font-bold text-gray-900">
                  {(selectedCity.annual_tourists / 1000000).toFixed(1)} million
                </span>{' '}
                tourists annually, generating significant economic impact through
                major events and cultural activities.
              </div>
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center p-8 text-center">
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="w-24 h-24 mb-6 rounded-full bg-white bg-opacity-80 backdrop-blur-md border border-mellow-ice border-opacity-50 shadow-lg flex items-center justify-center p-2"
            >
              <img
                src="/media/IMAGESEVENTLY/LOGOEVENTLY.png"
                alt="Evently Logo"
                className="w-full h-full object-contain"
              />
            </motion.div>
            <motion.h3
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-2xl font-display text-gray-900 mb-2"
            >
              Welcome to Evently
            </motion.h3>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-gray-700 mb-8 max-w-md font-mono"
            >
              Click on any orange pin on the globe to explore how major events
              impact tourism, hotels, and local economies in cities worldwide.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="space-y-3 w-full max-w-sm mb-6"
            >
              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-peach border-opacity-30 shadow-lg text-left">
                <div className="flex items-center gap-3">
                  <div className="text-3xl">📊</div>
                  <div>
                    <div className="font-display text-gray-900 mb-1">
                      Real Data Analysis
                    </div>
                    <div className="text-xs font-mono text-gray-600">
                      Track tourism, hotels & economy
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-ice border-opacity-50 shadow-lg text-left">
                <div className="flex items-center gap-3">
                  <div className="text-3xl">🎯</div>
                  <div>
                    <div className="font-display text-gray-900 mb-1">
                      Event Impact Insights
                    </div>
                    <div className="text-xs font-mono text-gray-600">
                      Measure ROI and economic benefits
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-cream border-opacity-50 shadow-lg text-left">
                <div className="flex items-center gap-3">
                  <div className="text-3xl">🔮</div>
                  <div>
                    <div className="font-display text-gray-900 mb-1">
                      What-If Scenarios
                    </div>
                    <div className="text-xs font-mono text-gray-600">
                      Simulate and forecast outcomes
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="mt-8"
            >
              <a
                href="/dashboard"
                className="inline-block px-6 py-3 bg-gradient-mellow border border-mellow-peach rounded-xl text-gray-900 font-mono hover:opacity-90 transition-all shadow-lg"
              >
                Go to Dashboard →
              </a>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  )
}

export default GlobeLanding
