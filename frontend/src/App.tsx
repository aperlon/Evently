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
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <Link to="/" className="flex items-center">
              <h1 className="text-3xl font-bold text-primary-600">Evently</h1>
              <span className="ml-3 text-sm text-gray-500">Event Impact Analyzer</span>
            </Link>
            <nav className="flex space-x-8">
              <Link to="/" className="text-gray-700 hover:text-primary-600">
                Home
              </Link>
              <Link to="/dashboard" className="text-gray-700 hover:text-primary-600">
                Dashboard
              </Link>
              <Link to="/events" className="text-gray-700 hover:text-primary-600">
                Events
              </Link>
              <Link to="/compare" className="text-gray-700 hover:text-primary-600">
                Compare
              </Link>
              <Link to="/predict" className="text-gray-700 hover:text-primary-600">
                Predict
              </Link>
              <Link to="/about" className="text-gray-700 hover:text-primary-600">
                About
              </Link>
              <Link to="/case-studies" className="text-gray-700 hover:text-primary-600">
                Cases
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <Footer />
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
        <Route path="/case-studies" element={<CaseStudies />} />
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
