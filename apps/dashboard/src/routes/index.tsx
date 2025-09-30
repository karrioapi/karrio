import { Navigate, createFileRoute } from '@tanstack/react-router'
import { useEffect, useState } from 'react'
import { oauth } from '@/lib/oauth'

export const Route = createFileRoute('/')({
  component: IndexPage,
})

function IndexPage() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)

  useEffect(() => {
    // Check OAuth authentication
    const checkAuth = async () => {
      try {
        const authenticated = await oauth.isAuthenticated()
        setIsAuthenticated(authenticated)
      } catch (error) {
        console.error('Auth check failed:', error)
        setIsAuthenticated(false)
      }
    }

    checkAuth()
  }, [])

  // Show loading while checking authentication
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" />
  }

  return <Navigate to="/signin" />
}
