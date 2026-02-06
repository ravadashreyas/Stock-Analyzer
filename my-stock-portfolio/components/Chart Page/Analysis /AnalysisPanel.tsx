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
        <div className="rounded-lg border bg-white shadow-sm dark:bg-zinc-900 dark:border-zinc-800">
        <div className="p-4 border-b dark:border-zinc-800 flex justify-between items-center">
          <h4 className="text-lg font-semibold">Market Analysis</h4>
           <span className={`px-3 py-1 rounded-full text-sm font-bold 
            ${data.analysis.rating === 'Buy' ? 'bg-green-100 text-green-700' : 
              data.analysis.rating === 'Neutral' ? 'bg-gray-100 text-gray-700' : 
              'bg-red-100 text-red-700'}`}>
            {data.analysis.rating}
          </span>
        </div>

        <div className="p-4">
          <h5 className="text-sm font-medium text-gray-500 mb-2">Analyst Remarks</h5>
          <ul className="space-y-2">
            {data.analysis.remark.split('. ').map((sentence, index) => (
              sentence && (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex gap-2">
                  <span className="text-blue-500">•</span>
                  {sentence.trim()}
                </li>
              )
            ))}
          </ul>
        </div>
      </div>
            )}
    </div>
  )
}
