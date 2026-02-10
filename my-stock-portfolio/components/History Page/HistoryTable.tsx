"use client"
import React, { useState, useEffect } from 'react'


interface HistoryData {
    user_id: string
    date_of_purchase: string
    stock_name: string
    stock_ticker: string
    action: string
    price_at_purchase: number
    number_of_shares: number
    total_cost: number
}

export default function HistoryTable({ history }: { history: HistoryData[] }) {
    if (!history || history.length === 0) return <div className="text-gray-500">No data available</div>

    const thClass = "px-2 py-1"
    const tdClass = "px-2 py-1"

    useEffect
    return (
        <div className="overflow-x-auto">
            <table className="min-w-full text-xs text-left">
                <thead className="bg-gray-100 dark:bg-zinc-800 font-medium text-gray-700 dark:text-gray-300">
                    <tr>
                        <th className={thClass}>Date of Action</th>
                        <th className={thClass}>Stock</th>
                        <th className={thClass}>Ticker</th>
                        <th className={thClass}>Action</th>
                        <th className={thClass}>Price at Action</th>
                        <th className={thClass}>Number of Shares</th>
                        <th className={thClass}>Total Cost</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-zinc-700">
                    {history.map((his) => (
                        <tr key={his.stock_ticker} className="hover:bg-gray-50 dark:hover:bg-zinc-900">
                            <td className={tdClass}>{new Date(his.date_of_purchase).toLocaleDateString()}</td>
                            <td className={`${tdClass} font-bold`}>{his.stock_name}</td>
                            <td className={tdClass}>{his.stock_ticker}</td>
                            <td className={tdClass}>{his.action.toUpperCase()}</td>
                            <td className={`${tdClass} text-gray-500`}>{his.price_at_purchase}</td>
                            <td className={`${tdClass} `}>{his.number_of_shares.toFixed(2)}</td>
                            <td className={`${tdClass}`}>{his.total_cost.toFixed(2)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}
