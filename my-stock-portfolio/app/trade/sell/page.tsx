import SellTradeClient from '../../../components/Trade Page/SellPage/SellTradeClient'

export default function SellPage() {
    return (
        <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white">
            <main className="max-w-5xl mx-auto py-12 px-6">
                <h1 className="text-3xl font-bold mb-6 text-[#ff5000]">Sell Stock</h1>
                <SellTradeClient />
            </main>
        </div>
    )
}
