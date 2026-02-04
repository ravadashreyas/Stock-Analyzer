"use client"
import React, { useState, useEffect } from 'react'

export default function AnalysisPanel({ ticker }: { ticker: string }) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadAnalysis()
  }, [ticker])

  async function loadAnalysis() {
    if (!ticker) return
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
