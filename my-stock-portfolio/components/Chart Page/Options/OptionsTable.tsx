import React from 'react'

interface OptionData {
    contractSymbol: string
    lastTradeDate: string
    strike: number
    lastPrice: number
    bid: number
    ask: number
    change: number
    percentChange: number
    volume: number
    openInterest: number
    impliedVolatility: number
}

export default function OptionsTable({ options }: { options: OptionData[] }) {
    if (!options || options.length === 0) return <div className="text-gray-500">No data available</div>

    const thClass = "px-2 py-1"
    const tdClass = "px-2 py-1"

    return (
        <div className="overflow-x-auto">
            <table className="min-w-full text-xs text-left">
                <thead className="bg-gray-100 dark:bg-zinc-800 font-medium text-gray-700 dark:text-gray-300">
                    <tr>
                        <th className={thClass}>Symbol</th>
                        <th className={thClass}>Date</th>
                        <th className={thClass}>Strike</th>
                        <th className={thClass}>Last</th>
                        <th className={thClass}>Bid</th>
                        <th className={thClass}>Ask</th>
                        <th className={thClass}>Change</th>
                        <th className={thClass}>% Chg</th>
                        <th className={thClass}>Vol</th>
                        <th className={thClass}>OI</th>
                        <th className={thClass}>IV</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-zinc-700">
                    {options.map((opt) => (
                        <tr key={opt.contractSymbol} className="hover:bg-gray-50 dark:hover:bg-zinc-900">
                            <td className={`${tdClass} font-mono`}>{opt.contractSymbol}</td>
                            <td className={tdClass}>{new Date(opt.lastTradeDate).toLocaleDateString()}</td>
                            <td className={`${tdClass} font-bold`}>{opt.strike}</td>
                            <td className={tdClass}>{opt.lastPrice}</td>
                            <td className={`${tdClass} text-gray-500`}>{opt.bid}</td>
                            <td className={`${tdClass} text-gray-500`}>{opt.ask}</td>
                            <td className={`${tdClass} ${opt.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                {opt.change > 0 ? '+' : ''}{opt.change.toFixed(2)}
                            </td>
                            <td className={`${tdClass} ${opt.percentChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                {opt.percentChange.toFixed(2)}%
                            </td>
                            <td className={`${tdClass} text-right`}>{opt.volume}</td>
                            <td className={`${tdClass} text-right`}>{opt.openInterest}</td>
                            <td className={tdClass}>{opt.impliedVolatility.toFixed(2)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}
