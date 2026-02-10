"use client"
import Link from 'next/link'
import HistoryTable from './HistoryTable'
import React, { useState, useEffect} from 'react'


export default function HistoryClient(){
    const [data, setData] = useState<any>(null) 
    useEffect(() => {
        loadHistory()
    },[])

    async function loadHistory() {
        try {
        const res = await fetch('/api/getTrades', { method: 'GET', headers: { 'Content-Type': 'application/json' }})
        const json = await res.json()
        setData(json)
        } catch (err) {
        alert('Failed to load Transaction: ' + err)
        }
    }

    return(
        <div className="">
                <Link
                href = "/"
                aria-label = "Home"
                className="absolute top-4 left-4 z-50 flex h-10 w-10 items-center justify-center rounded-full border border-solid border-black/[.08] bg-white/80 hover:bg-black/[.04] dark:bg-black/60 dark:border-white/[.145] dark:hover:bg-[#1a1a1a]"            href="/"
            >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-5 w-5 text-black dark:text-white" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M3 11.5L12 4l9 7.5" />
                <path d="M9 21V13h6v8" />
                <path d="M21 21H3" />
            </svg>
            <span className="sr-only">Home</span>
                </Link>
                <div>
                    <HistoryTable history={data}/>
                </div>
        </div>
    )
}