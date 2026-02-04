 "use client";
import React, { useState, useEffect } from 'react'

interface TradeDateProps {
  value: string;                   
  onChange: (val: string) => void; 
}

export default function TradeDate({ value, onChange }: TradeDateProps){

    return(
       <div className="flex gap-2 mb-4">
                <input
                value={value}
                onChange={e => onChange(e.target.value)}
                className="border px-3 py-2 w-full max-w-xs"
                placeholder="Enter Date of Purchase (e.g. 2025-01-01)"
                />
            </div> 
    )
}