import React, { useState, useEffect } from 'react'


interface PorfolioData {
    user_id: string
    date_of_purchase: string
    stock_name: string
    stock_ticker: string
    price_at_purchase: number
    current_price: number
    number_of_shares: number
    total_cost: number
    current_value: number
    gain_loss: number
    percent_gain_loss: number
}

export default function PortfolioTable({ portfolio }: { portfolio: PorfolioData[] }) {
    if (!portfolio || portfolio.length === 0) return <div className="text-gray-500">No data available</div>

    const thClass = "px-2 py-1"
    const tdClass = "px-2 py-1"

    return (
        <div className="overflow-x-auto">
            <table className="min-w-full text-xs text-left">
                <thead className="bg-gray-100 dark:bg-zinc-800 font-medium text-gray-700 dark:text-gray-300">
                    <tr>
                        <th className={thClass}>Date of Purchase</th>
                        <th className={thClass}>Stock</th>
                        <th className={thClass}>Ticker</th>
                        <th className={thClass}>Price at Purchase</th>
                        <th className={thClass}>Number of Shares</th>
                        <th className={thClass}>Current Price</th>
                        <th className={thClass}>Number of Shares</th>
                        <th className={thClass}>Total Cost</th>
                        <th className={thClass}>Current Value</th>
                        <th className={thClass}>Gain/Loss</th>
                        <th className={thClass}>% Gain/Loss</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-zinc-700">
                    {portfolio.map((port) => (
                        <tr key={port.user_id} className="hover:bg-gray-50 dark:hover:bg-zinc-900">
                            <td className={tdClass}>{new Date(port.date_of_purchase).toLocaleDateString()}</td>
                            <td className={`${tdClass} font-bold`}>{port.stock_name}</td>
                            <td className={tdClass}>{port.stock_ticker}</td>
                            <td className={`${tdClass} text-gray-500`}>{port.price_at_purchase.toFixed(2)}</td>
                            <td className={`${tdClass} text-gray-500`}>{port.number_of_shares}</td>
                            <td className={`${tdClass} text-gray-500`}>{port.current_price.toFixed(2)}</td>
                            <td className={`${tdClass} text-right`}>{port.number_of_shares.toFixed(2)}</td>
                            <td className={`${tdClass} text-right`}>{port.total_cost.toFixed(2)}</td>
                            <td className={tdClass}>{port.current_value.toFixed(2)}</td>
                            <td className={`${tdClass} ${port.gain_loss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                {port.gain_loss > 0 ? '+' : ''}{port.gain_loss.toFixed(2)}
                            </td>
                            <td className={`${tdClass} ${port.percent_gain_loss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                {port.percent_gain_loss.toFixed(2)}%
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}
