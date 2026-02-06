"use client";
import React, { useState, useEffect, useRef } from 'react'
import PortfolioTable from './PortfolioTable'
import PlotlyChart from '../Chart Page/PlotlyChart'

const TIME_FRAMES = ['1D', '5D', '1M', '3M', '6M', 'YTD', '1Y', '5Y', 'ALL'] as const
type TimeFrame = typeof TIME_FRAMES[number]

export default function PortfolioPanel({ initialData }: { initialData?: any }) {
  const [data, setData] = useState<any>(initialData || null)
  const lastFetchTime = useRef<number>(0)
  const [plotData, setPlotData] = useState<any>(null)
  const [timeFrame, setTimeFrame] = useState<TimeFrame>('3M')
  const [loading, setLoading] = useState(false)
  const THROTTLE_MS = 30000

  async function loadPortfolio(force = false) {
    const now = Date.now()
    if (!force && now - lastFetchTime.current < THROTTLE_MS) {
      return
    }
    lastFetchTime.current = now

    try {
      const res = await fetch('/api/portfolio', { method: 'GET', headers: { 'Content-Type': 'application/json' } })
      const json = await res.json()
      setData(json)
    } catch (err) {
      console.error('Failed to load Portfolio:', err)
    }
  }

  async function loadPlot(tf: TimeFrame = timeFrame) {
    setLoading(true)
    try {
      const result = await fetch('/api/portfolioPlot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ timeFrame: tf })
      })
      const plotJson = await result.json()
      setPlotData(plotJson)
    } catch (err) {
      console.error('Failed to load plot:', err)
    }
    setLoading(false)
  }

  function handleTimeFrameChange(tf: TimeFrame) {
    setTimeFrame(tf)
    loadPlot(tf)
  }

  useEffect(() => {
    loadPortfolio(true)
    loadPlot()

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        loadPortfolio()
      }
    }

    document.addEventListener('visibilitychange', handleVisibilityChange)

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, [])

  return (
    <div className="space-y-8">
      <div>
        <h3 className="text-lg font-medium mb-2">Portfolio Summary</h3>
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
        {loading && <div className="text-gray-500">Loading...</div>}
        <PlotlyChart figureJSON={plotData} />
      </div>
      <div className="max-h-96 overflow-y-auto">
        <PortfolioTable portfolio={data} />
      </div>
    </div>
  )
}