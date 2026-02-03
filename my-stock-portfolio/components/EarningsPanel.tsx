"use client"
import React, { useState, useEffect } from 'react'
import EarningsTable from './EarningsTable'

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
            <div className="max-h-96 overflow-y-auto">
                <EarningsTable earnings={data.anEarnings} />
            </div>
          <h4>Quarterly</h4>
          <div className="max-h-96 overflow-y-auto">
                <EarningsTable earnings={data.quEarnings} />
        </div>
        </div>
      )}
    </div>
  )
}
