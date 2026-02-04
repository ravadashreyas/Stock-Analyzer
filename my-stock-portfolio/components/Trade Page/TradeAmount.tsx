 "use client";
import React, { useState, useEffect } from 'react'

interface TradeAmountProps {
  value: string;                   
  onChange: (val: string) => void; 
}

export default function TradeAmount({ value, onChange }: TradeAmountProps){

    return(
       <div className="flex gap-2 mb-4">
                <input
                value={value}
                onChange={e => onChange(e.target.value)}
                className="border px-3 py-2 w-full max-w-xs"
                placeholder="Enter Number of Shares (e.g. 150)"
                />
            </div> 
    )
}