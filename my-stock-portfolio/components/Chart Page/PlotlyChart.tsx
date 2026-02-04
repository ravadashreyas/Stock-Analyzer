"use client"
import dynamic from 'next/dynamic'
import React from 'react'

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

type PlotlyJSON = any

export default function PlotlyChart({ figureJSON } : { figureJSON: PlotlyJSON }) {
  if (!figureJSON) return null

  const data = figureJSON.data || []
  const layout = figureJSON.layout || {}

  return (
    <div className="w-full">
      <Plot data={data} layout={layout} style={{width: '100%'}} useResizeHandler={true} />
    </div>
  )
}
