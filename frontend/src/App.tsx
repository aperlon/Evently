import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import EventsList from './pages/EventsList'
import EventDetails from './pages/EventDetails'
import CitiesComparison from './pages/CitiesComparison'
import WhatIfSimulator from './pages/WhatIfSimulator'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center">
                <h1 className="text-3xl font-bold text-primary-600">Evently</h1>
                <span className="ml-3 text-sm text-gray-500">Event Impact Analyzer</span>
              </div>
              <nav className="flex space-x-8">
                <Link to="/" className="text-gray-700 hover:text-primary-600">
                  Dashboard
                </Link>
                <Link to="/events" className="text-gray-700 hover:text-primary-600">
                  Events
                </Link>
                <Link to="/compare" className="text-gray-700 hover:text-primary-600">
                  Compare
                </Link>
                <Link to="/simulator" className="text-gray-700 hover:text-primary-600">
                  What-If
                </Link>
              </nav>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/events" element={<EventsList />} />
            <Route path="/events/:id" element={<EventDetails />} />
            <Route path="/compare" element={<CitiesComparison />} />
            <Route path="/simulator" element={<WhatIfSimulator />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <p className="text-center text-gray-500 text-sm">
              Evently - Analyzing the economic and touristic impact of urban events
            </p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
