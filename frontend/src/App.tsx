import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import GlobeLanding from './pages/GlobeLanding'
import Dashboard from './pages/Dashboard'
import EventsList from './pages/EventsList'
import EventDetails from './pages/EventDetails'
import CitiesComparison from './pages/CitiesComparison'
import WhatIfSimulator from './pages/WhatIfSimulator'
import EventPredictor from './pages/EventPredictor'
import AboutUs from './pages/AboutUs'
import Methodology from './pages/Methodology'
import CaseStudies from './pages/CaseStudies'
import Footer from './components/Footer'

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-mellow border-b border-mellow-peach shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <Link to="/" className="flex items-center gap-3">
              <img
                src="/media/IMAGESEVENTLY/LOGOEVENTLY.png"
                alt="Evently Logo"
                className="w-10 h-10 object-contain"
              />
              <h1 className="text-3xl font-display text-gray-900 leading-tight">Evently</h1>
            </Link>
            <nav className="flex space-x-8">
              <Link to="/" className="text-gray-800 hover:text-gray-900 transition-colors font-mono">
                Home
              </Link>
              <Link to="/dashboard" className="text-gray-800 hover:text-gray-900 transition-colors font-mono">
                Dashboard
              </Link>
              <Link to="/events" className="text-gray-800 hover:text-gray-900 transition-colors font-mono">
                Events
              </Link>
              <Link to="/compare" className="text-gray-800 hover:text-gray-900 transition-colors font-mono">
                Compare
              </Link>
              <Link to="/predict" className="text-gray-800 hover:text-gray-900 transition-colors font-mono">
                Predict
              </Link>
              <Link to="/about" className="text-gray-800 hover:text-gray-900 transition-colors font-mono">
                About
              </Link>
              <Link to="/methodology" className="text-gray-800 hover:text-gray-900 transition-colors font-mono">
                Methodology
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content Container with footer background color */}
      <div className="bg-gradient-to-br from-mellow-cream to-mellow-ice -mb-px relative">
        <main className="w-full bg-white rounded-b-[60px] sm:rounded-b-[80px] lg:rounded-b-[100px] relative z-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {children}
          </div>
        </main>
      </div>

      {/* Footer - positioned behind main with negative margin */}
      <div className="relative -mt-[60px] sm:-mt-[80px] lg:-mt-[100px] z-0">
        <Footer />
      </div>
    </div>
  )
}

function AppRoutes() {
  const location = useLocation()

  // Pages that don't need the layout (full screen)
  const fullScreenPages = ['/']
  const isFullScreen = fullScreenPages.includes(location.pathname)

  if (isFullScreen) {
    return (
      <Routes>
        <Route path="/" element={<GlobeLanding />} />
      </Routes>
    )
  }

  return (
    <Layout>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/events" element={<EventsList />} />
        <Route path="/events/:id" element={<EventDetails />} />
        <Route path="/compare" element={<CitiesComparison />} />
        <Route path="/simulator" element={<WhatIfSimulator />} />
        <Route path="/predict" element={<EventPredictor />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/methodology" element={<Methodology />} />
        <Route path="/case-studies" element={<Methodology />} />
      </Routes>
    </Layout>
  )
}

function App() {
  return (
    <Router>
      <AppRoutes />
    </Router>
  )
}

export default App
