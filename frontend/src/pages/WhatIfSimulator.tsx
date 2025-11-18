import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiService } from '../services/api'

function WhatIfSimulator() {
  const [selectedEventId, setSelectedEventId] = useState<number | null>(null)
  const [attendanceChange, setAttendanceChange] = useState(0)

  const { data: events } = useQuery({
    queryKey: ['events'],
    queryFn: apiService.getEvents,
  })

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold">What-If Scenario Simulator</h2>
        <p className="text-gray-600 mt-2">
          Simulate different scenarios and project event impacts
        </p>
      </div>

      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Configure Scenario</h3>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Event
            </label>
            <select
              className="w-full border border-gray-300 rounded-md px-3 py-2"
              value={selectedEventId || ''}
              onChange={(e) => setSelectedEventId(parseInt(e.target.value))}
            >
              <option value="">Choose an event...</option>
              {events?.map((event) => (
                <option key={event.id} value={event.id}>
                  {event.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Attendance Change (%)
            </label>
            <input
              type="range"
              min="-50"
              max="200"
              value={attendanceChange}
              onChange={(e) => setAttendanceChange(parseInt(e.target.value))}
              className="w-full"
            />
            <p className="text-center mt-2 font-semibold">
              {attendanceChange > 0 ? '+' : ''}
              {attendanceChange}%
            </p>
          </div>

          <button
            className="btn-primary w-full"
            disabled={!selectedEventId}
          >
            Run Simulation
          </button>
        </div>

        {!selectedEventId && (
          <p className="text-center text-gray-500 mt-8">
            Select an event and adjust parameters to run a simulation
          </p>
        )}
      </div>
    </div>
  )
}

export default WhatIfSimulator
