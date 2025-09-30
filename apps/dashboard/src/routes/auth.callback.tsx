import { createFileRoute, useRouter, useSearch } from '@tanstack/react-router'
import { useEffect, useState } from 'react'
import { oauth } from '@/lib/oauth'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'

export const Route = createFileRoute('/auth/callback')({
  component: OAuthCallback,
  validateSearch: (search: Record<string, unknown>) => {
    return {
      code: (search.code as string) || '',
      state: (search.state as string) || '',
      error: (search.error as string) || '',
      error_description: (search.error_description as string) || '',
    }
  },
})

function OAuthCallback() {
  const router = useRouter()
  const search = useSearch({ from: '/auth/callback' })
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>(
    'loading',
  )
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Check for OAuth errors
        if (search.error) {
          throw new Error(search.error_description || search.error)
        }

        // Check for authorization code
        if (!search.code) {
          throw new Error('No authorization code received')
        }

        setStatus('loading')

        // Exchange code for tokens
        const tokens = await oauth.exchangeCodeForToken(
          search.code,
          search.state,
        )

        // Store tokens
        oauth.storeTokens(tokens)

        // Get user info
        const userInfo = await oauth.getUserInfo(tokens.access_token)

        // Store user info
        localStorage.setItem('karrio_user_info', JSON.stringify(userInfo))
        localStorage.setItem('isAuthenticated', 'true')

        setStatus('success')

        // Redirect to dashboard after short delay
        setTimeout(() => {
          router.navigate({ to: '/dashboard' })
        }, 1000)
      } catch (err) {
        console.error('OAuth callback error:', err)
        setError(err instanceof Error ? err.message : 'Authentication failed')
        setStatus('error')

        // Clear any partial tokens
        oauth.clearTokens()

        // Redirect to signin after delay
        setTimeout(() => {
          router.navigate({ to: '/signin' })
        }, 3000)
      }
    }

    handleCallback()
  }, [search, router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">JTL App</h1>
        </div>

        <Card className="border border-gray-200 shadow-sm">
          <CardContent className="p-8">
            {status === 'loading' && (
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <h2 className="text-lg font-semibold mb-2">
                  Authenticating...
                </h2>
                <p className="text-gray-600">
                  Please wait while we complete your sign in
                </p>
              </div>
            )}

            {status === 'success' && (
              <div className="text-center">
                <div className="rounded-full h-8 w-8 bg-green-100 flex items-center justify-center mx-auto mb-4">
                  <svg
                    className="h-5 w-5 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
                <h2 className="text-lg font-semibold mb-2 text-green-600">
                  Success!
                </h2>
                <p className="text-gray-600">
                  You have been successfully authenticated. Redirecting to
                  dashboard...
                </p>
              </div>
            )}

            {status === 'error' && (
              <div className="text-center">
                <Alert variant="destructive" className="mb-4">
                  <AlertDescription>
                    <strong>Authentication Failed</strong>
                    <br />
                    {error}
                  </AlertDescription>
                </Alert>
                <p className="text-sm text-gray-600">
                  Redirecting back to sign in...
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
