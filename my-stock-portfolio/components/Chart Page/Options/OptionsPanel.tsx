import React, { useState, useEffect } from 'react'
import PlotlyChart from '../PlotlyChart'
import OptionsTable from './OptionsTable'

export default function OptionsPanel({ ticker }: { ticker: string }) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadOptions()
  }, [ticker])

  async function loadOptions() {
    if (!ticker) return
    setLoading(true)
    try {
      const res = await fetch('/api/options', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(ticker) })
      const json = await res.json()
      setData(json)
    } catch (err) {
      alert('Failed to load options: ' + err)
    }
    setLoading(false)
  }

  return (
    <div className="space-y-8">
      {loading && <div>Loading...</div>}
      {data && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="border p-4 rounded shadow-sm">
              <h3 className="text-xl font-bold mb-2 text-green-700">Calls</h3>
              <div className="max-h-96 overflow-y-auto">
                <OptionsTable options={data.calls} />
              </div>
            </div>
            <div className="border p-4 rounded shadow-sm">
              <h3 className="text-xl font-bold mb-2 text-red-700">Puts</h3>
              <div className="max-h-96 overflow-y-auto">
                <OptionsTable options={data.puts} />
              </div>
            </div>
          </div>
          <h4>Call Graph</h4>
          <PlotlyChart figureJSON={data.callGraph} />
          <h4>Put Graph</h4>
          <PlotlyChart figureJSON={data.putGraph} />
        </div>
      )}
    </div>
  )
}
