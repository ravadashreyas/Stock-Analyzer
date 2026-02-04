import HistoryClient from '../../components/History Page/HistoryClient'

export default function HistoryPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-black">
      <main className="max-w-5xl mx-auto py-12">
        <h1 className="text-3xl font-bold mb-6">Transaction History</h1>
        <HistoryClient />
      </main>
    </div>
  )
}
