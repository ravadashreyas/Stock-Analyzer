import TradeClient from '../../components/Trade Page/TradeClient'


export default function TradePage() {
    

    return (
        <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white">
            <main className="max-w-5xl mx-auto py-12 px-6">
                <h1 className="text-3xl font-bold mb-6">Trade Execution</h1>
                    <TradeClient />
            </main>
        </div>
    )
}
