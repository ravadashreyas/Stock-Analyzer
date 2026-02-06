"use client"
import React, { useState, useEffect } from 'react'
import PlotlyChart from './PlotlyChart'
import OptionsPanel from './Options/OptionsPanel'
import EarningsPanel from './Earnings/EarningsPanel'
import AnalysisPanel from './Analysis /AnalysisPanel'
import Link from 'next/link'

const TIME_FRAMES = ['1D', '5D', '1M', '3M', '6M', 'YTD', '1Y', '5Y', 'ALL'] as const
type TimeFrame = typeof TIME_FRAMES[number]

export default function DashboardClient() {
  const [ticker, setTicker] = useState('')
  const [plotData, setPlotData] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [tab, setTab] = useState<'plot' | 'options' | 'earnings' | 'analysis'>('plot')
  const [timeFrame, setTimeFrame] = useState<TimeFrame>('1Y')

  async function loadPlot(tf: TimeFrame = timeFrame) {
    if (!ticker) return
    setLoading(true)
    try {
      const res = await fetch('/api/plot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, timeFrame: tf }),
      })
      const json = await res.json()
      setPlotData(json)
    } catch (err) {
      console.error(err)
      alert('Failed to load plot: ' + err)
    }
    setLoading(false)
  }

  function handleTimeFrameChange(tf: TimeFrame) {
    setTimeFrame(tf)
    loadPlot(tf)
  }

  return (
    <div className="p-6">
      <div className="">
        <Link
          href="/"
          aria-label="Home"
          className="absolute top-4 left-4 z-50 flex h-10 w-10 items-center justify-center rounded-full border border-solid border-black/[.08] bg-white/80 hover:bg-black/[.04] dark:bg-black/60 dark:border-white/[.145] dark:hover:bg-[#1a1a1a]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-5 w-5 text-black dark:text-white" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M3 11.5L12 4l9 7.5" />
            <path d="M9 21V13h6v8" />
            <path d="M21 21H3" />
          </svg>
          <span className="sr-only">Home</span>
        </Link>
        <Link
          href="/login"
          aria-label="Login"
          className="absolute top-4 right-4 z-50 flex h-10 w-10 items-center justify-center rounded-full border border-solid border-black/[.08] bg-white/80 hover:bg-black/[.04] dark:bg-black/60 dark:border-white/[.145] dark:hover:bg-[#1a1a1a]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-5 w-5 text-black dark:text-white" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <span className="sr-only">Login</span>
        </Link>
      </div>
      <div className="flex gap-2 mb-4">
        <input
          value={ticker}
          onChange={e => setTicker(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter') void loadPlot()
          }}
          className="border px-3 py-2 w-full max-w-xs"
          placeholder="Enter ticker (e.g. AAPL) and press Enter"
        />
      </div>

      <div className="flex gap-2 mb-4">
        <button onClick={() => setTab('plot')} className={`px-3 py-2 rounded ${tab === 'plot' ? 'bg-slate-800 text-white' : 'bg-slate-100 text-black'}`}>Plot</button>
        <button onClick={() => setTab('options')} className={`px-3 py-2 rounded ${tab === 'options' ? 'bg-slate-800 text-white' : 'bg-slate-100 text-black'}`}>Options</button>
        <button onClick={() => setTab('earnings')} className={`px-3 py-2 rounded ${tab === 'earnings' ? 'bg-slate-800 text-white' : 'bg-slate-100 text-black'}`}>Earnings</button>
        <button onClick={() => setTab('analysis')} className={`px-3 py-2 rounded ${tab === 'analysis' ? 'bg-slate-800 text-white' : 'bg-slate-100 text-black'}`}>Analysis</button>
      </div>

      {tab === 'plot' && (
        <div>
          {/* Time Frame Buttons */}
          <div className="flex gap-1 mb-4 flex-wrap">
            {TIME_FRAMES.map((tf) => (
              <button
                key={tf}
                onClick={() => handleTimeFrameChange(tf)}
                className={`px-3 py-1 rounded text-sm ${timeFrame === tf ? 'bg-blue-600 text-white' : 'bg-zinc-200 dark:bg-zinc-700 text-black dark:text-white'}`}
              >
                {tf}
              </button>
            ))}
          </div>
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
