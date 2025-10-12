import { useEffect, useState } from 'react'
import { createFileRoute, useRouter } from '@tanstack/react-router'
import { authManager } from '@/lib/auth'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'

export const Route = createFileRoute('/auth/callback')({
  component: CallbackPage,
})

function CallbackPage() {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(true)

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Extract JWT token from URL (query params or hash fragment)
        const params = new URLSearchParams(window.location.search)
        const hash = new URLSearchParams(window.location.hash.substring(1))

        const token = params.get('token') || hash.get('token')
        const state = params.get('state') || hash.get('state')

        if (!token) {
          throw new Error('No authentication token received from JTL Hub')
        }

        // Verify state for CSRF protection
        if (state && !authManager.verifyOAuthState(state)) {
          throw new Error('Invalid state parameter - possible CSRF attack')
        }

        // Exchange JTL token for Karrio JWT
        await authManager.handleJTLCallback(token)

        // Redirect to dashboard
        router.navigate({ to: '/dashboard' })
      } catch (err) {
        console.error('Authentication error:', err)
        setError(err instanceof Error ? err.message : 'Authentication failed')
        setIsProcessing(false)
      }
    }

    handleCallback()
  }, [router])

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="w-full max-w-md">
          <Card className="border border-red-200 dark:border-red-900">
            <CardContent className="p-8">
              <div className="text-center mb-4">
                <svg
                  className="mx-auto h-12 w-12 text-red-600 dark:text-red-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>

              <h2 className="text-xl font-semibold text-center text-red-900 dark:text-red-100 mb-2">
                Authentication Failed
              </h2>

              <Alert variant="destructive" className="mb-6">
                <AlertDescription>{error}</AlertDescription>
              </Alert>

              <button
                onClick={() => router.navigate({ to: '/signin' })}
                className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
              >
                Back to Sign In
              </button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4" />
        <h2 className="text-xl font-semibold text-foreground mb-2">
          Completing Sign In
        </h2>
        <p className="text-muted-foreground">
          Please wait while we authenticate you...
        </p>
      </div>
    </div>
  )
}
