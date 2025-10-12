import { Navigate, createFileRoute } from '@tanstack/react-router'
import { authManager } from '@/lib/auth'

export const Route = createFileRoute('/')({
  component: IndexPage,
})

function IndexPage() {
  // Check authentication synchronously (no async needed)
  const isAuthenticated = authManager.isAuthenticated()

  if (isAuthenticated) {
    return <Navigate to="/dashboard" />
  }

  return <Navigate to="/signin" />
}
