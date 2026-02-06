import PortfolioPanel from "@/components/Home Page/PortfolioPanel";
import Link from "next/link";
import { cookies } from 'next/headers'

async function getPortfolioData() {
  const cookieStore = await cookies()
  const sessionCookie = cookieStore.get('session')

  if (!sessionCookie) return null

  try {
    const res = await fetch('http://127.0.0.1:5000/api/portfolio', {
      headers: {
        Cookie: `session=${sessionCookie.value}`
      },
      cache: 'no-store'
    })

    if (!res.ok) return null
    return res.json()
  } catch (error) {
    console.error("Failed to fetch portfolio data server-side:", error)
    return null
  }
}

export default async function Home() {
  const initialData = await getPortfolioData()

  return (
    <div className="min-h-screen flex flex-col bg-zinc-50 font-sans dark:bg-black">
      <Link
        href="/login"
        aria-label="Login"
        className="absolute top-4 right-4 z-50 flex h-10 w-10 items-center justify-center rounded-full border border-solid border-black/[.08] bg-white/80 hover:bg-black/[.04] dark:bg-black/60 dark:border-white/[.145] dark:hover:bg-[#1a1a1a]"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-5 w-5 text-black dark:text-white" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
        <span className="sr-only">Login</span>
      </Link>
      <div className="flex justify-center gap-4 py-8 text-base font-medium">
        <a
          className="flex h-12 items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
          href="/trade"
        >
          Trade
        </a>
        <a
          className="flex h-12 items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
          href="/history"
        >
          History
        </a>
        <a
          className="flex h-12 items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
          href="/dashboard"
        >
          Chart
        </a>
      </div>
      <main className="flex-1 flex items-center justify-center px-8">
        <div className="w-full max-w-5xl">
          <PortfolioPanel initialData={initialData} />
        </div>
      </main>
    </div>
  );
}
