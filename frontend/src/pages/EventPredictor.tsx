import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiService } from '../services/api'

function EventPredictor() {
  const [eventType, setEventType] = useState('sports')
  const [city, setCity] = useState('London')
  const [durationDays, setDurationDays] = useState(7)
  const [attendance, setAttendance] = useState<number | undefined>(undefined)
  const [prediction, setPrediction] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Get available cities
  const { data: cities } = useQuery({
    queryKey: ['cities'],
    queryFn: apiService.getCities,
  })

  const eventTypes = [
    { value: 'sports', label: 'Sports' },
    { value: 'music', label: 'Music' },
    { value: 'culture', label: 'Culture' },
    { value: 'festival', label: 'Festival' },
  ]

  const handlePredict = async () => {
    setIsLoading(true)
    setError(null)
    setPrediction(null)

    try {
      const result = await apiService.predictEvent({
        event_type: eventType,
        city: city,
        duration_days: durationDays,
        attendance: attendance,
      })
      setPrediction(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Error making prediction')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-display text-gray-900">Event Impact Predictor</h1>
        <p className="mt-2 text-lg text-gray-600 font-mono">
          Predict the economic impact of a future event using our regression model
        </p>
      </div>

      {/* Prediction Form */}
      <div className="card">
        <h2 className="text-2xl font-display text-gray-900 mb-6">Event Details</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Event Type */}
          <div>
            <label className="block text-sm font-mono text-gray-700 mb-2">
              Event Type *
            </label>
            <select
              value={eventType}
              onChange={(e) => setEventType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-200 lg:border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-gray-50 lg:bg-white text-gray-700 lg:text-gray-800"
            >
              {eventTypes.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          {/* City */}
          <div>
            <label className="block text-sm font-mono text-gray-700 mb-2">
              City *
            </label>
            <select
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="w-full px-4 py-2 border border-gray-200 lg:border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-gray-50 lg:bg-white text-gray-700 lg:text-gray-800"
            >
              {cities?.map((c) => (
                <option key={c.id} value={c.name}>
                  {c.name}, {c.country}
                </option>
              ))}
            </select>
          </div>

          {/* Duration */}
          <div>
            <label className="block text-sm font-mono text-gray-700 mb-2">
              Duration (days) *
            </label>
            <input
              type="number"
              min="1"
              max="365"
              value={durationDays}
              onChange={(e) => setDurationDays(parseInt(e.target.value) || 1)}
              className="w-full px-4 py-2 border border-gray-200 lg:border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-gray-50 lg:bg-white text-gray-700 lg:text-gray-800"
            />
          </div>

          {/* Attendance (Optional) */}
          <div>
            <label className="block text-sm font-mono text-gray-700 mb-2">
              Expected Attendance (optional)
            </label>
            <input
              type="number"
              min="0"
              value={attendance || ''}
              onChange={(e) => setAttendance(e.target.value ? parseInt(e.target.value) : undefined)}
              placeholder="Auto-estimated if not provided"
              className="w-full px-4 py-2 border border-gray-200 lg:border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-gray-50 lg:bg-white text-gray-700 lg:text-gray-800"
            />
            <p className="mt-1 text-sm text-gray-500 font-mono">
              Leave empty to auto-estimate based on similar events
            </p>
          </div>
        </div>

        <button
          onClick={handlePredict}
          disabled={isLoading}
          className="mt-6 w-full md:w-auto px-8 py-3 bg-gradient-mellow text-gray-900 rounded-lg font-mono font-semibold hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl border border-mellow-peach"
        >
          {isLoading ? 'Predicting...' : 'Predict Economic Impact'}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="card bg-red-50 border border-red-200">
          <h3 className="text-red-800 font-display">Prediction Error</h3>
          <p className="text-red-600 mt-2 font-mono">{error}</p>
        </div>
      )}

      {/* Prediction Results */}
      {prediction && (
        <div className="space-y-6">
          {/* Main Prediction Card */}
          <div className="card bg-gray-50 border-2 border-mellow-peach">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-display text-gray-900">Predicted Economic Impact</h2>
              <span className="px-3 py-1 bg-mellow-peach text-gray-900 rounded-full text-sm font-mono font-semibold">
                {prediction.prediction?.confidence_level || '90%'} Confidence
              </span>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <p className="text-sm text-gray-600 mb-1 font-mono">Total Impact</p>
                <p className="text-3xl font-mono text-gray-900">
                  ${(prediction.prediction?.total_economic_impact_usd || 0).toLocaleString()}
                </p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <p className="text-sm text-gray-600 mb-1 font-mono">Lower Bound</p>
                <p className="text-2xl font-mono text-gray-700">
                  ${(prediction.prediction?.lower_bound_usd || 0).toLocaleString()}
                </p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <p className="text-sm text-gray-600 mb-1 font-mono">Upper Bound</p>
                <p className="text-2xl font-mono text-gray-700">
                  ${(prediction.prediction?.upper_bound_usd || 0).toLocaleString()}
                </p>
              </div>
            </div>
          </div>

          {/* Breakdown */}
          <div className="card">
            <h3 className="text-xl font-display text-gray-900 mb-4">Economic Breakdown</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gradient-to-br from-mellow-ice to-mellow-cream rounded-lg p-4 border border-mellow-ice">
                <p className="text-sm text-gray-700 font-mono mb-1">Direct Spending</p>
                <p className="text-2xl font-mono text-gray-900">
                  ${(prediction.breakdown?.direct_spending_usd || 0).toLocaleString()}
                </p>
                <p className="text-xs text-gray-600 mt-1 font-mono">64% of total</p>
              </div>
              
              <div className="bg-gradient-to-br from-mellow-cream to-mellow-peach rounded-lg p-4 border border-mellow-cream">
                <p className="text-sm text-gray-700 font-mono mb-1">Indirect Spending</p>
                <p className="text-2xl font-mono text-gray-900">
                  ${(prediction.breakdown?.indirect_spending_usd || 0).toLocaleString()}
                </p>
                <p className="text-xs text-gray-600 mt-1 font-mono">25% of total</p>
              </div>
              
              <div className="bg-gradient-to-br from-mellow-peach to-mellow-ice rounded-lg p-4 border border-mellow-peach">
                <p className="text-sm text-gray-700 font-mono mb-1">Induced Spending</p>
                <p className="text-2xl font-mono text-gray-900">
                  ${(prediction.breakdown?.induced_spending_usd || 0).toLocaleString()}
                </p>
                <p className="text-xs text-gray-600 mt-1 font-mono">11% of total</p>
              </div>
            </div>
          </div>

          {/* Estimates */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card">
              <h4 className="text-lg font-display text-gray-900 mb-2">Jobs Created</h4>
              <p className="text-3xl font-mono text-gray-900">
                {(prediction.estimates?.jobs_created || 0).toLocaleString()}
              </p>
              <p className="text-sm text-gray-600 mt-2 font-mono">
                {prediction.estimates?.jobs_ratio_usd 
                  ? `$${Math.round(prediction.estimates.jobs_ratio_usd).toLocaleString()} per job`
                  : 'Estimated at $40,000 per job created'}
              </p>
            </div>
            
            <div className="card">
              <h4 className="text-lg font-display text-gray-900 mb-2">ROI Ratio</h4>
              <p className="text-3xl font-mono text-gray-900">
                {prediction.estimates?.roi_ratio?.toFixed(2) || 'N/A'}x
              </p>
              <p className="text-sm text-gray-600 mt-2 font-mono">
                Return on investment
              </p>
            </div>
            
            <div className="card">
              <h4 className="text-lg font-display text-gray-900 mb-2">Estimated Cost</h4>
              <p className="text-3xl font-mono text-gray-900">
                ${(prediction.estimates?.estimated_event_cost_usd || 0).toLocaleString()}
              </p>
              <p className="text-sm text-gray-600 mt-2 font-mono">
                Estimated event organization cost
              </p>
            </div>
          </div>

          {/* Baseline Comparison */}
          {prediction.baseline_comparison && (
            <div className="card bg-gradient-to-br from-mellow-cream to-mellow-ice border-2 border-mellow-peach">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-display text-gray-900">📊 Comparación con Semana Normal</h3>
                <span className="px-3 py-1 bg-mellow-peach text-gray-900 rounded-full text-sm font-mono font-semibold">
                  {prediction.baseline_comparison.impact_multiplier?.toFixed(1) || 'N/A'}x más impacto
                </span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <p className="text-sm text-gray-600 mb-1 font-mono">Impacto Semana Normal</p>
                  <p className="text-3xl font-mono text-gray-900">
                    ${(prediction.baseline_comparison.baseline_weekly_impact_usd || 0).toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500 mt-2 font-mono">
                    {prediction.baseline_comparison.duration_days} días sin evento
                  </p>
                </div>
                
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <p className="text-sm text-gray-600 mb-1 font-mono">Impacto con Evento</p>
                  <p className="text-3xl font-mono text-gray-900">
                    ${(prediction.baseline_comparison.event_impact_usd || 0).toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500 mt-2 font-mono">
                    Mismo período con evento
                  </p>
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h4 className="text-lg font-display text-gray-900 mb-4">Impacto Adicional del Evento</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-mono text-gray-900">
                      +${(prediction.baseline_comparison.additional_impact_usd || 0).toLocaleString()}
                    </p>
                    <p className="text-sm text-gray-600 mt-1 font-mono">Impacto Adicional</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-mono text-gray-900">
                      +{prediction.baseline_comparison.impact_increase_pct?.toFixed(1) || '0'}%
                    </p>
                    <p className="text-sm text-gray-600 mt-1 font-mono">Incremento Porcentual</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-mono text-gray-900">
                      {prediction.baseline_comparison.impact_multiplier?.toFixed(1) || '1.0'}x
                    </p>
                    <p className="text-sm text-gray-600 mt-1 font-mono">Multiplicador de Impacto</p>
                  </div>
                </div>
              </div>

              <div className={`mt-4 rounded-lg p-4 ${
                (prediction.baseline_comparison.impact_multiplier || 0) > 1 
                  ? 'bg-gradient-to-br from-mellow-cream to-mellow-ice border border-mellow-peach' 
                  : 'bg-gradient-to-br from-mellow-ice to-mellow-cream border border-mellow-ice'
              }`}>
                <p className={`text-sm font-mono ${
                  (prediction.baseline_comparison.impact_multiplier || 0) > 1 
                    ? 'text-gray-800' 
                    : 'text-gray-800'
                }`}>
                  <strong>💡 Interpretación:</strong>{' '}
                  {(prediction.baseline_comparison.impact_multiplier || 0) > 1 ? (
                    <>
                      Este evento genera{' '}
                      <strong>{prediction.baseline_comparison.impact_multiplier?.toFixed(1) || '1.0'} veces</strong> más impacto económico
                      que un período normal de {prediction.baseline_comparison.duration_days} días en {prediction.input_summary?.city || 'esta ciudad'}.
                      Esto representa un{' '}
                      <strong>+{prediction.baseline_comparison.impact_increase_pct?.toFixed(1) || '0'}%</strong> de incremento
                      sobre el impacto económico normal del período.
                    </>
                  ) : (
                    <>
                      Este evento genera un impacto económico{' '}
                      <strong>{prediction.baseline_comparison.impact_multiplier?.toFixed(2) || '1.0'} veces</strong> el de un período normal.
                      Para eventos de corta duración o baja asistencia, el impacto puede ser similar al turismo normal.
                    </>
                  )}
                </p>
              </div>
            </div>
          )}

          {/* Model Info */}
          <div className="card bg-gray-50 border border-mellow-ice">
            <h4 className="text-lg font-display text-gray-900 mb-3">Model Information</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <p className="text-gray-600 font-mono">Model Used</p>
                <p className="font-mono text-gray-900 capitalize">
                  {prediction.model_info?.model_used?.replace('_', ' ') || 'N/A'}
                </p>
              </div>
              <div>
                <p className="text-gray-600 font-mono">R² Score</p>
                <p className="font-mono text-gray-900">
                  {prediction.model_info?.model_r2?.toFixed(4) || 'N/A'}
                </p>
              </div>
              <div>
                <p className="text-gray-600 font-mono">MAPE</p>
                <p className="font-mono text-gray-900">
                  {prediction.model_info?.model_mape?.toFixed(2) || 'N/A'}%
                </p>
              </div>
              <div>
                <p className="text-gray-600 font-mono">Input Summary</p>
                <p className="font-mono text-gray-900">
                  {prediction.input_summary?.event_type || 'N/A'} • {prediction.input_summary?.city || 'N/A'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default EventPredictor

