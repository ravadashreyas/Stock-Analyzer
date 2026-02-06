import Link from 'next/link'

export default function TradePage() {
    return (
        <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white">
            <main className="max-w-5xl mx-auto py-12 px-6">
                <h1 className="text-3xl font-bold mb-6">Trade Execution</h1>
                <div className="flex w-full gap-4 max-w-md">
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
                    <Link
                        href="/trade/buy"
                        className="rounded-lg bg-zinc-100 dark:bg-zinc-900 py-4 px-12 font-semibold text-black dark:text-white text-center
                                border border-zinc-300 dark:border-zinc-700
                                transition-all duration-200 ease-in-out
                                hover:bg-zinc-200 dark:hover:bg-zinc-800 hover:-translate-y-0.5 
                                active:translate-y-0.5"
                    >
                        Buy
                    </Link>
                    <Link
                        href="/trade/sell"
                        className="rounded-lg bg-zinc-100 dark:bg-zinc-900 py-4 px-12 font-semibold text-black dark:text-white text-center
                                border border-zinc-300 dark:border-zinc-700
                                transition-all duration-200 ease-in-out
                                hover:bg-zinc-200 dark:hover:bg-zinc-800 hover:-translate-y-0.5 
                                active:translate-y-0.5"
                    >
                        Sell
                    </Link>
                </div>
            </main>
        </div>
    )
}
