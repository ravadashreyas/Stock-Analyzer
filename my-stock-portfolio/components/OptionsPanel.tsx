"use client"
import React, { useState } from 'react'
import PlotlyChart from './PlotlyChart'

export default function OptionsPanel({ ticker }: { ticker: string }) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  async function loadOptions() {
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
    <div>
      <div className="mb-2">
        <button onClick={() => void loadOptions()} className="px-3 py-2 bg-indigo-600 text-white rounded">Load Options</button>
      </div>
      {loading && <div>Loading...</div>}
      {data && (
        <div>
          <h4>Calls</h4>
          <pre className="max-h-44 overflow-auto bg-slate-100 p-2">{JSON.stringify(data.calls, null, 2)}</pre>
          <h4>Puts</h4>
          <pre className="max-h-44 overflow-auto bg-slate-100 p-2">{JSON.stringify(data.puts, null, 2)}</pre>
          <h4>Call Graph</h4>
          <PlotlyChart figureJSON={data.callGraph} />
          <h4>Put Graph</h4>
          <PlotlyChart figureJSON={data.putGraph} />
        </div>
      )}
    </div>
  )
}
