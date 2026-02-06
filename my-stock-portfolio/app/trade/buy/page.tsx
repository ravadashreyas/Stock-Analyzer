import BuyTradeClient from '../../../components/Trade Page/BuyPage/BuyTradeClient'

export default function BuyPage() {
    return (
        <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white">
            <main className="max-w-5xl mx-auto py-12 px-6">
                <h1 className="text-3xl font-bold mb-6 text-[#FFFFFF]">Buy Stock</h1>
                <BuyTradeClient />
            </main>
        </div>
    )
}
