"use client"
import React, { useState } from 'react'
import PlotlyChart from './PlotlyChart'
import OptionsPanel from './OptionsPanel'
import EarningsPanel from './EarningsPanel'
import AnalysisPanel from './AnalysisPanel'

export default function DashboardClient() {
  const [ticker, setTicker] = useState('AAPL')
  const [plotData, setPlotData] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [tab, setTab] = useState<'plot'|'options'|'earnings'|'analysis'>('plot')

  async function loadPlot() {
    setLoading(true)
    try {
      const res = await fetch('/api/plot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, timeFrame: '1Y' }),
      })
      const json = await res.json()
      setPlotData(json)
    } catch (err) {
      console.error(err)
      alert('Failed to load plot: ' + err)
    }
    setLoading(false)
  }

  return (
    <div className="p-6">
      <div className="flex gap-2 mb-4">
        <input value={ticker} onChange={e => setTicker(e.target.value)} className="border px-3 py-2" />
        <button onClick={() => void loadPlot()} className="px-4 py-2 bg-sky-600 text-white rounded">Load Plot</button>
      </div>

      <div className="flex gap-2 mb-4">
        <button onClick={() => setTab('plot')} className={`px-3 py-2 rounded ${tab==='plot'?'bg-slate-800 text-white':'bg-slate-100'}`}>Plot</button>
        <button onClick={() => setTab('options')} className={`px-3 py-2 rounded ${tab==='options'?'bg-slate-800 text-white':'bg-slate-100'}`}>Options</button>
        <button onClick={() => setTab('earnings')} className={`px-3 py-2 rounded ${tab==='earnings'?'bg-slate-800 text-white':'bg-slate-100'}`}>Earnings</button>
        <button onClick={() => setTab('analysis')} className={`px-3 py-2 rounded ${tab==='analysis'?'bg-slate-800 text-white':'bg-slate-100'}`}>Analysis</button>
      </div>

      {tab === 'plot' && (
        <div>
          {loading && <div>Loading...</div>}
          {plotData && (
            <div>
              <h3 className="text-lg font-medium mb-2">Price Chart</h3>
              <PlotlyChart figureJSON={plotData} />
            </div>
          )}
        </div>
      )}

      {tab === 'options' && <OptionsPanel ticker={ticker} />}
      {tab === 'earnings' && <EarningsPanel ticker={ticker} />}
      {tab === 'analysis' && <AnalysisPanel ticker={ticker} />}
    </div>
  )
}
