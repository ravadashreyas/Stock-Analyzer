import DashboardClient from '../../components/Chart Page/DashboardClient'

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-black">
      <main className="max-w-5xl mx-auto py-12">
        <h1 className="text-3xl font-bold mb-6">Trading Dashboard</h1>
        <DashboardClient />
      </main>
    </div>
  )
}
