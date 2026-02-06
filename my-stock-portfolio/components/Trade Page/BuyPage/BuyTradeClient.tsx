"use client"
import React, { useState, useEffect } from 'react'
import TradeTicker from '../TradeTicker'
import TradeDate from '../TradeDate'
import TradeAmount from '../TradeAmount'
import Link from 'next/link'

export default function BuyTradeClient() {
    const [ticker, setTicker] = useState('')
    const [number_of_shares, setNumberOfShares] = useState('')
    const [date_purchased, setDate] = useState('')
    const [valid, setValid] = useState('')

    async function stockAction() {
        try {
            const res = await fetch('/api/buyTrade', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ticker, number_of_shares, date_purchased }) })
            const json = await res.json()
            setValid(json)
        } catch (err) {
            alert('Failed to add Trade: ' + err)
        }
    }
    return (
        <div className="">
            <Link
                href="/"
                aria-label="Home"
                className="absolute top-4 left-4 z-50 flex h-10 w-10 items-center justify-center rounded-full border border-solid border-black/[.08] bg-white/80 hover:bg-black/[.04] dark:bg-black/60 dark:border-white/[.145] dark:hover:bg-[#1a1a1a]" href="/"
            >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-5 w-5 text-black dark:text-white" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <path d="M3 11.5L12 4l9 7.5" />
                    <path d="M9 21V13h6v8" />
                    <path d="M21 21H3" />
                </svg>
                <span className="sr-only">Home</span>
            </Link>
            <div className="border border-zinc-200 dark:border-zinc-800 rounded-lg p-6">
                <p>Stock Ticker</p>
                <TradeTicker
                    value={ticker}
                    onChange={setTicker}
                />
            </div>
            <div className="border border-zinc-200 dark:border-zinc-800 rounded-lg p-6">
                <p>Number of Shares</p>
                <TradeAmount
                    value={number_of_shares}
                    onChange={setNumberOfShares}
                />
            </div>
            <div className="border border-zinc-200 dark:border-zinc-800 rounded-lg p-6">
                <p>Date of Order</p>
                <TradeDate
                    value={date_purchased}
                    onChange={setDate}
                />
            </div>
            <div className='border border-zince-200 dark:border-zinc-800 rounded-lg p-6 text-center'>
                <p>{valid.Result}</p>
            </div>
            <button
                onClick={stockAction}
                className="w-full bg-zinc-900 hover:bg-zinc-800 text-white dark:bg-zinc-100 dark:hover:bg-zinc-200 dark:text-black font-bold py-3 px-4 rounded-lg transition-colors duration-200 mt-4 shadow-md hover:shadow-lg"
            >
                Place Order
            </button>
        </div>

    )
}