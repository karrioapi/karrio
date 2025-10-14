import { createFileRoute, useRouter } from '@tanstack/react-router'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { authManager } from '@/lib/auth'

export const Route = createFileRoute('/signin')({
  component: SignInPage,
  head: () => ({
    meta: [{ title: 'Sign In - JTL Shipping' }],
  }),
})

function SignInPage() {
  const router = useRouter()

  // Check if JTL Hub OAuth is configured
  const jtlClientId = import.meta.env.VITE_JTL_HUB_CLIENT_ID
  const isJTLConfigured = jtlClientId && jtlClientId.trim() !== ''

  // JTL OAuth is the primary method - always default to it
  const [activeTab, setActiveTab] = useState<'jtl' | 'token'>('jtl')
  const [error, setError] = useState<string | null>(null)
  const [apiToken, setApiToken] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleJTLLogin = async () => {
    try {
      setError(null)
      setIsLoading(true)
      await authManager.loginWithJTLHub()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication error')
      setIsLoading(false)
    }
    // Note: setIsLoading(false) is intentionally NOT called on success
    // because the page will redirect to JTL Hub
  }

  const handleTokenLogin = async () => {
    if (!apiToken.trim()) {
      setError('Please enter an API token')
      return
    }

    try {
      setError(null)
      setIsLoading(true)
      await authManager.loginWithToken(apiToken)
      router.navigate({ to: '/dashboard' })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid API token')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <img src="/logo.svg" alt="JTL Shipping" className="h-12 w-auto" />
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            Sign in to your account
          </p>
        </div>

        <Card className="border border-border shadow-sm">
          <CardContent className="p-0">
            {/* Tabs */}
            <div className="flex border-b border-border">
              <button
                onClick={() => {
                  setActiveTab('jtl')
                  setError(null)
                }}
                className={`flex-1 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'jtl'
                    ? 'border-primary text-primary'
                    : 'border-transparent text-muted-foreground hover:text-foreground'
                }`}
              >
                JTL Hub OAuth
              </button>
              <button
                onClick={() => {
                  setActiveTab('token')
                  setError(null)
                }}
                className={`flex-1 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'token'
                    ? 'border-primary text-primary'
                    : 'border-transparent text-muted-foreground hover:text-foreground'
                }`}
              >
                API Token
              </button>
            </div>

            {/* Tab Content */}
            <div className="p-8">
              {error && (
                <Alert variant="destructive" className="mb-6">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {activeTab === 'jtl' ? (
                <div>
                  <h2 className="text-xl font-semibold text-center mb-4 text-foreground">
                    JTL Hub SSO
                  </h2>
                  <p className="text-sm text-muted-foreground text-center mb-6">
                    Sign in with your JTL Hub account
                  </p>

                  {!isJTLConfigured && (
                    <Alert className="mb-6 bg-amber-50 dark:bg-amber-950 border-amber-200 dark:border-amber-800">
                      <AlertDescription className="text-amber-800 dark:text-amber-200">
                        <strong>Configuration Required:</strong> JTL Hub OAuth is not configured.
                        Please set <code className="text-xs bg-amber-100 dark:bg-amber-900 px-1 py-0.5 rounded">VITE_JTL_HUB_CLIENT_ID</code> in
                        your environment variables to enable this authentication method.
                      </AlertDescription>
                    </Alert>
                  )}

                  <Button
                    onClick={handleJTLLogin}
                    disabled={!isJTLConfigured || isLoading}
                    className="w-full"
                    size="lg"
                  >
                    {isLoading && activeTab === 'jtl' ? 'Redirecting to JTL Hub...' : 'Sign in with JTL Hub'}
                  </Button>

                  {!isJTLConfigured && (
                    <p className="text-xs text-muted-foreground text-center mt-4">
                      Use the <strong>API Token</strong> tab to sign in with a Karrio API token instead.
                    </p>
                  )}
                </div>
              ) : (
                <div>
                  <h2 className="text-xl font-semibold text-center mb-4 text-foreground">
                    Karrio API Token
                  </h2>
                  <p className="text-sm text-muted-foreground text-center mb-6">
                    Use your Karrio API token to authenticate
                  </p>
                  <div className="space-y-4">
                    <div>
                      <label htmlFor="apiToken" className="block text-sm font-medium text-foreground mb-2">
                        API Token
                      </label>
                      <input
                        id="apiToken"
                        type="password"
                        value={apiToken}
                        onChange={(e) => setApiToken(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            handleTokenLogin()
                          }
                        }}
                        placeholder="Enter your Karrio API token"
                        className="w-full px-3 py-2 border border-input bg-background text-foreground rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-input"
                        disabled={isLoading}
                      />
                      <p className="mt-2 text-xs text-muted-foreground">
                        You can generate an API token in your Karrio dashboard settings
                      </p>
                    </div>
                    <Button
                      onClick={handleTokenLogin}
                      disabled={isLoading}
                      className="w-full"
                      size="lg"
                    >
                      {isLoading ? 'Authenticating...' : 'Sign in with Token'}
                    </Button>
                  </div>
                </div>
              )}

              <p className="text-xs text-muted-foreground text-center mt-6">
                By signing in, you agree to our Terms of Service and Privacy Policy
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="text-center mt-6 text-sm text-muted-foreground">
          Need help?{' '}
          <a
            href="https://support.jtl-software.com"
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold text-primary hover:underline"
          >
            Contact Support
          </a>
        </div>
      </div>
    </div>
  )
}
