import axios from 'axios'

// Use relative path in production (Vercel), absolute in development
const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '/api/v1' : 'http://localhost:8000/api/v1')

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface City {
  id: number
  name: string
  country: string
  country_code: string
  continent: string
  latitude: number
  longitude: number
  timezone: string
  population: number
  annual_tourists: number
  hotel_rooms: number
  avg_hotel_price_usd: number
}

export interface Event {
  id: number
  city_id: number
  name: string
  event_type: string
  start_date: string
  end_date: string
  expected_attendance?: number
  actual_attendance?: number
  year: number
}

export interface EventImpact {
  id: number
  event_id: number
  baseline_daily_visitors?: number
  event_period_daily_visitors?: number
  visitor_increase_pct: number
  price_increase_pct: number
  occupancy_increase_pct: number
  total_economic_impact_usd: number
  jobs_created: number
  roi_ratio: number
  additional_visitors?: number
}

export interface DashboardKPIs {
  total_events_analyzed: number
  total_cities: number
  avg_economic_impact_per_event_usd: number
  avg_visitor_increase_pct: number
  avg_hotel_price_increase_pct: number
  total_jobs_created: number
  highest_impact_event_name?: string
  highest_impact_city?: string
}

// API Functions
export const apiService = {
  // Cities
  getCities: async (): Promise<City[]> => {
    const response = await api.get('/cities')
    return response.data
  },

  getCity: async (id: number): Promise<City> => {
    const response = await api.get(`/cities/${id}`)
    return response.data
  },

  // Events
  getEvents: async (filters?: {
    city_id?: number
    event_type?: string
    year?: number
  }): Promise<Event[]> => {
    const response = await api.get('/events', { params: filters })
    return response.data
  },

  getEvent: async (id: number): Promise<Event> => {
    const response = await api.get(`/events/${id}`)
    return response.data
  },

  // Impact Analysis
  getEventImpact: async (eventId: number, recalculate = false): Promise<EventImpact> => {
    const response = await api.get(`/events/${eventId}/impact`, {
      params: { recalculate },
    })
    return response.data
  },

  // Dashboard
  getDashboardKPIs: async (): Promise<DashboardKPIs> => {
    const response = await api.get('/analytics/dashboard/kpis')
    return response.data
  },

  // Comparisons
  compareEvents: async (eventIds: number[]) => {
    const response = await api.post('/analytics/compare/events', eventIds)
    return response.data
  },

  compareCities: async (cityIds: number[]) => {
    const response = await api.post('/analytics/compare/cities', cityIds)
    return response.data
  },

  // What-If Simulation
  simulateAttendanceChange: async (params: {
    event_id: number
    attendance_change_pct: number
    price_elasticity?: number
    spending_multiplier?: number
  }) => {
    const response = await api.post('/analytics/whatif/attendance', params)
    return response.data
  },

  simulateEventGrowth: async (
    eventId: number,
    years: number,
    annualGrowthPct: number
  ) => {
    const response = await api.get(`/analytics/whatif/growth/${eventId}`, {
      params: { years, annual_growth_pct: annualGrowthPct },
    })
    return response.data
  },

  // Time Series
  getTimeSeries: async (
    cityId: number,
    metricType: string,
    startDate: string,
    endDate: string
  ) => {
    const response = await api.get(`/analytics/timeseries/${cityId}`, {
      params: {
        metric_type: metricType,
        start_date: startDate,
        end_date: endDate,
      },
    })
    return response.data
  },

  // Prediction
  predictEvent: async (params: {
    event_type: string
    city: string
    duration_days: number
    attendance?: number
  }) => {
    const response = await api.post('/predict', params)
    return response.data
  },

  getPredictionOptions: async () => {
    const response = await api.get('/predict/options')
    return response.data
  },
}

export default api
