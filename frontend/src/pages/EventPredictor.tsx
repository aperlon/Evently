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
    { value: 'business', label: 'Business' },
    { value: 'fair', label: 'Fair' },
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
        <h1 className="text-4xl font-bold text-gray-900">Event Impact Predictor</h1>
        <p className="mt-2 text-lg text-gray-600">
          Predict the economic impact of a future event using our regression model
        </p>
      </div>

      {/* Prediction Form */}
      <div className="card">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Event Details</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Event Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Event Type *
            </label>
            <select
              value={eventType}
              onChange={(e) => setEventType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
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
            <label className="block text-sm font-medium text-gray-700 mb-2">
              City *
            </label>
            <select
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
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
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Duration (days) *
            </label>
            <input
              type="number"
              min="1"
              max="365"
              value={durationDays}
              onChange={(e) => setDurationDays(parseInt(e.target.value) || 1)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>

          {/* Attendance (Optional) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Expected Attendance (optional)
            </label>
            <input
              type="number"
              min="0"
              value={attendance || ''}
              onChange={(e) => setAttendance(e.target.value ? parseInt(e.target.value) : undefined)}
              placeholder="Auto-estimated if not provided"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
            <p className="mt-1 text-sm text-gray-500">
              Leave empty to auto-estimate based on similar events
            </p>
          </div>
        </div>

        <button
          onClick={handlePredict}
          disabled={isLoading}
          className="mt-6 w-full md:w-auto px-8 py-3 bg-gradient-mellow text-gray-900 rounded-lg font-semibold hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl border border-mellow-peach"
        >
          {isLoading ? 'Predicting...' : 'Predict Economic Impact'}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="card bg-red-50 border border-red-200">
          <h3 className="text-red-800 font-semibold">Prediction Error</h3>
          <p className="text-red-600 mt-2">{error}</p>
        </div>
      )}

      {/* Prediction Results */}
      {prediction && (
        <div className="space-y-6">
          {/* Main Prediction Card */}
          <div className="card bg-gradient-to-br from-primary-50 to-primary-100 border-2 border-primary-300">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-gray-900">Predicted Economic Impact</h2>
              <span className="px-3 py-1 bg-primary-600 text-white rounded-full text-sm font-semibold">
                {prediction.prediction?.confidence_level || '90%'} Confidence
              </span>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <p className="text-sm text-gray-600 mb-1">Total Impact</p>
                <p className="text-3xl font-bold text-primary-600">
                  ${(prediction.prediction?.total_economic_impact_usd || 0).toLocaleString()}
                </p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <p className="text-sm text-gray-600 mb-1">Lower Bound</p>
                <p className="text-2xl font-semibold text-gray-700">
                  ${(prediction.prediction?.lower_bound_usd || 0).toLocaleString()}
                </p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <p className="text-sm text-gray-600 mb-1">Upper Bound</p>
                <p className="text-2xl font-semibold text-gray-700">
                  ${(prediction.prediction?.upper_bound_usd || 0).toLocaleString()}
                </p>
              </div>
            </div>
          </div>

          {/* Breakdown */}
          <div className="card">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Economic Breakdown</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <p className="text-sm text-blue-600 font-medium mb-1">Direct Spending</p>
                <p className="text-2xl font-bold text-blue-700">
                  ${(prediction.breakdown?.direct_spending_usd || 0).toLocaleString()}
                </p>
                <p className="text-xs text-blue-600 mt-1">64% of total</p>
              </div>
              
              <div className="bg-green-50 rounded-lg p-4">
                <p className="text-sm text-green-600 font-medium mb-1">Indirect Spending</p>
                <p className="text-2xl font-bold text-green-700">
                  ${(prediction.breakdown?.indirect_spending_usd || 0).toLocaleString()}
                </p>
                <p className="text-xs text-green-600 mt-1">25% of total</p>
              </div>
              
              <div className="bg-purple-50 rounded-lg p-4">
                <p className="text-sm text-purple-600 font-medium mb-1">Induced Spending</p>
                <p className="text-2xl font-bold text-purple-700">
                  ${(prediction.breakdown?.induced_spending_usd || 0).toLocaleString()}
                </p>
                <p className="text-xs text-purple-600 mt-1">11% of total</p>
              </div>
            </div>
          </div>

          {/* Estimates */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card">
              <h4 className="text-lg font-semibold text-gray-900 mb-2">Jobs Created</h4>
              <p className="text-3xl font-bold text-primary-600">
                {(prediction.estimates?.jobs_created || 0).toLocaleString()}
              </p>
              <p className="text-sm text-gray-600 mt-2">
                Estimated at $40,000 per job created
              </p>
            </div>
            
            <div className="card">
              <h4 className="text-lg font-semibold text-gray-900 mb-2">ROI Ratio</h4>
              <p className="text-3xl font-bold text-green-600">
                {prediction.estimates?.roi_ratio?.toFixed(2) || 'N/A'}x
              </p>
              <p className="text-sm text-gray-600 mt-2">
                Return on investment
              </p>
            </div>
            
            <div className="card">
              <h4 className="text-lg font-semibold text-gray-900 mb-2">Estimated Cost</h4>
              <p className="text-3xl font-bold text-gray-700">
                ${(prediction.estimates?.estimated_event_cost_usd || 0).toLocaleString()}
              </p>
              <p className="text-sm text-gray-600 mt-2">
                Estimated event organization cost
              </p>
            </div>
          </div>

          {/* Baseline Comparison */}
          {prediction.baseline_comparison && (
            <div className="card bg-gradient-to-br from-yellow-50 to-orange-50 border-2 border-yellow-300">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">📊 Comparación con Semana Normal</h3>
                <span className="px-3 py-1 bg-yellow-600 text-white rounded-full text-sm font-semibold">
                  {prediction.baseline_comparison.impact_multiplier?.toFixed(1) || 'N/A'}x más impacto
                </span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <p className="text-sm text-gray-600 mb-1">Impacto Semana Normal</p>
                  <p className="text-3xl font-bold text-gray-700">
                    ${(prediction.baseline_comparison.baseline_weekly_impact_usd || 0).toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500 mt-2">
                    {prediction.baseline_comparison.duration_days} días sin evento
                  </p>
                </div>
                
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <p className="text-sm text-gray-600 mb-1">Impacto con Evento</p>
                  <p className="text-3xl font-bold text-primary-600">
                    ${(prediction.baseline_comparison.event_impact_usd || 0).toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500 mt-2">
                    Mismo período con evento
                  </p>
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Impacto Adicional del Evento</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-green-600">
                      +${(prediction.baseline_comparison.additional_impact_usd || 0).toLocaleString()}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">Impacto Adicional</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-blue-600">
                      +{prediction.baseline_comparison.impact_increase_pct?.toFixed(1) || '0'}%
                    </p>
                    <p className="text-sm text-gray-600 mt-1">Incremento Porcentual</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-purple-600">
                      {prediction.baseline_comparison.impact_multiplier?.toFixed(1) || '1.0'}x
                    </p>
                    <p className="text-sm text-gray-600 mt-1">Multiplicador de Impacto</p>
                  </div>
                </div>
              </div>

              <div className={`mt-4 rounded-lg p-4 ${
                (prediction.baseline_comparison.impact_multiplier || 0) > 1 
                  ? 'bg-green-50 border border-green-200' 
                  : 'bg-yellow-50 border border-yellow-200'
              }`}>
                <p className={`text-sm ${
                  (prediction.baseline_comparison.impact_multiplier || 0) > 1 
                    ? 'text-green-800' 
                    : 'text-yellow-800'
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
          <div className="card bg-gray-50">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">Model Information</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <p className="text-gray-600">Model Used</p>
                <p className="font-semibold text-gray-900 capitalize">
                  {prediction.model_info?.model_used?.replace('_', ' ') || 'N/A'}
                </p>
              </div>
              <div>
                <p className="text-gray-600">R² Score</p>
                <p className="font-semibold text-gray-900">
                  {prediction.model_info?.model_r2?.toFixed(4) || 'N/A'}
                </p>
              </div>
              <div>
                <p className="text-gray-600">MAPE</p>
                <p className="font-semibold text-gray-900">
                  {prediction.model_info?.model_mape?.toFixed(2) || 'N/A'}%
                </p>
              </div>
              <div>
                <p className="text-gray-600">Input Summary</p>
                <p className="font-semibold text-gray-900">
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

