import { useEffect, useRef, useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import createGlobe from 'cobe'
import { motion } from 'framer-motion'
import { TrendingUp, DollarSign, Users, Globe2, Target, Sparkles, ChevronDown } from 'lucide-react'
import { apiService, City } from '../services/api'

type MarkerWithCity = {
  location: [number, number]
  size: number
  city: City
}

function GlobeLanding() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const globeRef = useRef<any>(null)
  const [selectedCity, setSelectedCity] = useState<City | null>(null)
  const [globeTransform, setGlobeTransform] = useState('scale(0.8) translateX(30%)')
  const phi = useRef(0)
  const theta = useRef(0)

  // Adjust globe transform based on screen size
  useEffect(() => {
    const updateGlobeTransform = () => {
      const width = window.innerWidth
      if (width < 768) {
        // Small screens: hide globe
        setGlobeTransform('scale(0)')
      } else if (width < 1024) {
        // Medium screens: smaller scale, less translation
        setGlobeTransform('scale(0.6) translateX(20%)')
      } else {
        // Large screens: original size
        setGlobeTransform('scale(0.8) translateX(30%)')
      }
    }

    updateGlobeTransform()
    window.addEventListener('resize', updateGlobeTransform)
    return () => window.removeEventListener('resize', updateGlobeTransform)
  }, [])

  // Fetch cities
  const { data: cities, isLoading } = useQuery({
    queryKey: ['cities'],
    queryFn: () => apiService.getCities(),
  })

  // Convert cities to COBE markers
  const markers = useMemo<MarkerWithCity[]>(
    () =>
      cities?.map((city) => ({
        location: [city.latitude, city.longitude] as [number, number],
        size: 0.1,
        city,
      })) || [],
    [cities]
  )

  // Initialize COBE globe
  useEffect(() => {
    if (!canvasRef.current || !cities || cities.length === 0) return

    const canvas = canvasRef.current
    let currentGlobe: any = null

    const initGlobe = () => {
      if (!containerRef.current) return
      
      const rect = containerRef.current.getBoundingClientRect()
      const width = rect.width * 2
      const height = rect.height * 2
      
      canvas.width = width
      canvas.height = height

      // Create COBE globe with slow auto-rotation
      const globe = createGlobe(canvas, {
        devicePixelRatio: 2,
        width,
        height,
        phi: 0,
        theta: 0,
        dark: 0.0, // No dark areas for lighter globe
        diffuse: 1.8, // More diffuse light for brighter appearance
        mapSamples: 16000,
        mapBrightness: 10, // Increased brightness
        baseColor: [0.85, 0.85, 0.9], // Much lighter gray-blue background
        markerColor: [0.95, 0.64, 0.42], // Orange color #F3A46C in RGB
        glowColor: [0.95, 0.64, 0.42],
        markers: markers.map((m) => ({
          location: m.location,
          size: m.size,
        })),
        onRender: (state) => {
          // Slow auto-rotation to see all cities
          phi.current += 0.0015 // Slower rotation speed
          state.phi = phi.current
          state.theta = theta.current
        },
      })

      currentGlobe = globe
      globeRef.current = globe
    }

    initGlobe()

    // Handle resize
    const handleResize = () => {
      if (containerRef.current && canvas && currentGlobe) {
        const rect = containerRef.current.getBoundingClientRect()
        const newWidth = rect.width * 2
        const newHeight = rect.height * 2
        canvas.width = newWidth
        canvas.height = newHeight
        currentGlobe.width = newWidth
        currentGlobe.height = newHeight
      }
    }

    window.addEventListener('resize', handleResize)
    const resizeObserver = new ResizeObserver(handleResize)
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current)
    }

    return () => {
      window.removeEventListener('resize', handleResize)
      resizeObserver.disconnect()
      if (currentGlobe) {
        currentGlobe.destroy()
      }
    }
  }, [cities, markers])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl text-gray-600">Loading globe...</div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-sky-50">
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
            <h1 className="text-6xl font-display text-black leading-tight pt-4">
              Evently
            </h1>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <p className="text-2xl font-mono text-black mb-6">
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
                <span className="text-sm font-mono text-gray-600 uppercase tracking-wide">
                  Total Impact
                </span>
              </div>
              <div className="text-3xl font-display text-gray-900">$12.4B</div>
              <div className="text-xs font-mono text-gray-500 mt-1">Analyzed to date</div>
            </div>

            <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-ice border-opacity-50 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <Users className="w-5 h-5 text-mellow-ice" />
                <span className="text-sm font-mono text-gray-600 uppercase tracking-wide">
                  Jobs Created
                </span>
              </div>
              <div className="text-3xl font-display text-gray-900">847K</div>
              <div className="text-xs font-mono text-gray-500 mt-1">From major events</div>
            </div>

            <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-cream border-opacity-50 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <Globe2 className="w-5 h-5 text-mellow-cream" />
                <span className="text-sm font-mono text-gray-600 uppercase tracking-wide">
                  Cities
                </span>
              </div>
              <div className="text-3xl font-display text-gray-900">{cities?.length || 0}</div>
              <div className="text-xs font-mono text-gray-500 mt-1">Worldwide coverage</div>
            </div>

            <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-peach border-opacity-30 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-mellow-peach" />
                <span className="text-sm font-mono text-gray-600 uppercase tracking-wide">
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

        {/* Globe - Hidden on small screens, visible on medium+ */}
        <div className="absolute inset-0 w-full h-full hidden md:flex items-center justify-center">
          <div 
            className="relative w-full h-full"
            style={{
              transform: globeTransform,
              transformOrigin: 'center center',
            }}
          >
            <canvas
              ref={canvasRef}
              style={{
                width: '100%',
                height: '100%',
                pointerEvents: 'none',
              }}
            />
          </div>
        </div>

        {/* Navigation hint */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="absolute bottom-8 left-8"
        >
          <span className="px-4 py-2 bg-mellow-ice bg-opacity-40 border border-mellow-ice rounded-full text-gray-800 text-sm font-mono backdrop-blur-sm whitespace-nowrap inline-flex items-center gap-3">
            <span>🌍 Select a city from the panel to explore</span>
          </span>
        </motion.div>
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
          <div className="h-full flex flex-col items-center justify-center p-8">
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
              className="text-2xl font-display text-gray-900 mb-2 text-center"
            >
              Welcome to Evently
            </motion.h3>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-base text-gray-700 mb-8 max-w-md font-mono text-center"
            >
              Select a city from the dropdown to explore how major events
              impact tourism, hotels, and local economies worldwide.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="w-full max-w-sm"
            >
              <label htmlFor="city-select" className="block text-sm font-mono text-gray-700 mb-2 uppercase tracking-wide">
                Select a City
              </label>
              <div className="relative">
                <select
                  id="city-select"
                  value={selectedCity ? String((selectedCity as City).id) : ''}
                  onChange={(e) => {
                    const value = e.target.value
                    if (value === '') {
                      setSelectedCity(null)
                    } else {
                      const cityId = parseInt(value, 10)
                      if (!isNaN(cityId) && cities) {
                        const city = cities.find((c: City) => c.id === cityId)
                        if (city) {
                          setSelectedCity(city)
                        }
                      }
                    }
                  }}
                  className="w-full px-4 py-3 bg-white bg-opacity-80 backdrop-blur-md border-2 border-mellow-peach border-opacity-50 rounded-xl text-gray-900 font-mono shadow-lg appearance-none hover:border-mellow-peach focus:outline-none focus:ring-2 focus:ring-mellow-peach focus:border-mellow-peach transition-all cursor-pointer"
                >
                  <option value="">-- Select a city --</option>
                  {cities && cities.length > 0 ? cities.map((city: City) => (
                    <option key={city.id} value={String(city.id)}>
                      {city.name}, {city.country} ({city.continent})
                    </option>
                  )) : (
                    <option value="" disabled>Loading cities...</option>
                  )}
                </select>
                <ChevronDown className="absolute right-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-mellow-peach pointer-events-none" />
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="mt-8 space-y-3 w-full max-w-sm"
            >
              <div className="bg-white bg-opacity-80 backdrop-blur-md rounded-xl p-4 border border-mellow-peach border-opacity-30 shadow-lg text-left">
                <div className="flex items-center gap-3">
                  <TrendingUp className="w-5 h-5 text-mellow-peach" />
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
                  <Target className="w-5 h-5 text-mellow-ice" />
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
                  <Sparkles className="w-5 h-5 text-mellow-ice" />
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
              transition={{ duration: 0.6, delay: 0.5 }}
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
