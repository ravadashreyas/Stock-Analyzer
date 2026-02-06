"use client"
import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function LoginPage() {
  const [isRegistering, setIsRegistering] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [currentUser, setCurrentUser] = useState<string | null>(null)
  const [checkingAuth, setCheckingAuth] = useState(true)
  const router = useRouter()

  useEffect(() => {
    fetch('/api/auth/me')
      .then(async (res) => {
        if (res.ok) {
          const data = await res.json()
          setCurrentUser(data.username || data.user_id || 'User')
        }
      })
      .catch(() => { })
      .finally(() => setCheckingAuth(false))
  }, [])

  const handleLogout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' })
    setCurrentUser(null)
    router.refresh()
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const endpoint = isRegistering ? '/api/auth/register' : '/api/auth/login'

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })

      const data = await res.json()

      if (res.ok) {
        if (isRegistering) {

        }
        router.push('/')
        router.refresh()
      } else {
        setError(data.error || (isRegistering ? 'Registration failed' : 'Login failed'))
      }
    } catch (err) {
      setError('An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (checkingAuth) {
    return <div className="min-h-screen bg-gray-50 dark:bg-black flex items-center justify-center text-gray-500">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-black flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white dark:bg-zinc-900 rounded-lg shadow-lg p-8 border border-gray-200 dark:border-zinc-800">

        {currentUser ? (
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Welcome Back</h1>
            <p className="text-gray-600 dark:text-gray-400 mb-8">
              You are logged in as <span className="font-semibold text-blue-500">{currentUser}</span>
            </p>
            <div className="space-y-4">
              <Link href="/" className="block w-full bg-white text-black font-semibold py-3 rounded-lg hover:bg-gray-200 transition-colors border border-gray-200 dark:border-zinc-700">
                Go to Dashboard
              </Link>
              <button
                onClick={handleLogout}
                className="block w-full bg-zinc-200 dark:bg-zinc-800 text-gray-900 dark:text-white font-semibold py-3 rounded-lg hover:opacity-90 transition-opacity"
              >
                Sign Out
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                {isRegistering ? 'Create Account' : 'Welcome Back'}
              </h1>
              <p className="text-gray-500 dark:text-gray-400 mt-2">
                {isRegistering ? 'Sign up to start tracking' : 'Please sign in to continue'}
              </p>
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded text-sm text-center">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Username
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-4 py-2 rounded border border-gray-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-gray-900 dark:text-white outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                  placeholder="Enter your username"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-2 rounded border border-gray-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-gray-900 dark:text-white outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                  placeholder="••••••••"
                  required
                />
              </div>

              <button type="submit" disabled={loading} className="w-full bg-zinc-900 dark:bg-zinc-100 text-white dark:text-black font-semibold py-3 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50">
                {loading ? 'Processing...' : (isRegistering ? 'Sign Up' : 'Sign In')}
              </button>
            </form>

            <div className="mt-6 text-center">
              <button
                onClick={() => {
                  setIsRegistering(!isRegistering)
                  setError('')
                }}
                className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
              >
                {isRegistering ? 'Already have an account? Sign In' : "Don't have an account? Create one"}
              </button>
            </div>

            <div className="mt-4 text-center">
              <Link href="/" className="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
                Back to Dashboard
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
