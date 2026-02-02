"use client"
import React, { useState, useEffect } from 'react'

export default function EarningsPanel({ ticker }: { ticker: string }) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadEarnings()
  }, [ticker])

  async function loadEarnings() {
    if (!ticker) return
    setLoading(true)
    try {
      const res = await fetch('/api/earnings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(ticker) })
      const json = await res.json()
      setData(json)
    } catch (err) {
      alert('Failed to load earnings: ' + err)
    }
    setLoading(false)
  }

  return (
    <div>
      {loading && <div>Loading...</div>}
      {data && (
        <div>
          <h4>Annual</h4>
          <pre className="max-h-44 overflow-auto bg-slate-100 p-2">{JSON.stringify(data.anEarnings, null, 2)}</pre>
          <h4>Quarterly</h4>
          <pre className="max-h-44 overflow-auto bg-slate-100 p-2">{JSON.stringify(data.quEarnings, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
