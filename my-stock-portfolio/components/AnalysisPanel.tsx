"use client"
import React, { useState } from 'react'

export default function AnalysisPanel({ ticker }: { ticker: string }) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  async function loadAnalysis() {
    setLoading(true)
    try {
      const res = await fetch('/api/analysis', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ticker }) })
      const json = await res.json()
      setData(json)
    } catch (err) {
      alert('Failed to load analysis: ' + err)
    }
    setLoading(false)
  }

  return (
    <div>
      <div className="mb-2">
        <button onClick={() => void loadAnalysis()} className="px-3 py-2 bg-yellow-600 text-white rounded">Load Analysis</button>
      </div>
      {loading && <div>Loading...</div>}
      {data && (
        <div>
          <h4>Analysis</h4>
          <pre className="max-h-96 overflow-auto bg-slate-100 p-2">{JSON.stringify(data.analysis, null, 2)}</pre>
          <h4>Stock Data</h4>
          <pre className="max-h-96 overflow-auto bg-slate-100 p-2">{JSON.stringify(data.stockData, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
