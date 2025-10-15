import { createFileRoute, useRouter, Link } from '@tanstack/react-router'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { authManager } from '@/lib/auth'

export const Route = createFileRoute('/signin')({
  component: SignInPage,
  head: () => ({
    meta: [{ title: 'Sign In - JTL Shipping' }],
  }),
})

function SignInPage() {
  const router = useRouter()

  const [error, setError] = useState<string | null>(null)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleEmailLogin = async () => {
    if (!email.trim() || !password.trim()) {
      setError('Please enter both email and password')
      return
    }

    try {
      setError(null)
      setIsLoading(true)
      await authManager.loginWithEmailPassword(email, password)
      router.navigate({ to: '/dashboard' })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication failed')
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleEmailLogin()
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <img src="/logo.svg" alt="JTL Shipping" className="h-12 w-auto" />
          </div>
          <h1 className="text-2xl font-bold text-foreground">Sign in to your account</h1>
          <p className="text-sm text-muted-foreground mt-2">
            Enter your credentials to access your account
          </p>
        </div>

        <Card className="border border-border shadow-sm">
          <CardContent className="p-8">
            <Alert className="mb-6 bg-blue-50 border-blue-200 dark:bg-blue-950 dark:border-blue-800">
              <AlertDescription className="text-blue-800 dark:text-blue-200 text-sm">
                <strong>Development Notice:</strong> This is a temporary authentication method for development.
                We will migrate to JTL App Shell and SSO in the future.
              </AlertDescription>
            </Alert>

            {error && (
              <Alert variant="destructive" className="mb-6">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-4">
              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="you@example.com"
                  disabled={isLoading}
                  className="mt-2"
                  autoComplete="email"
                  autoFocus
                />
              </div>

              <div>
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Enter your password"
                  disabled={isLoading}
                  className="mt-2"
                  autoComplete="current-password"
                />
              </div>

              <Button
                onClick={handleEmailLogin}
                disabled={isLoading}
                className="w-full"
                size="lg"
              >
                {isLoading ? 'Signing in...' : 'Sign in'}
              </Button>
            </div>

            <p className="text-xs text-muted-foreground text-center mt-6">
              By signing in, you agree to our Terms of Service and Privacy Policy
            </p>
          </CardContent>
        </Card>

        <div className="text-center mt-6 text-sm text-muted-foreground">
          Don't have an account?{' '}
          <Link
            to="/register"
            className="font-semibold text-primary hover:underline"
          >
            Register here
          </Link>
        </div>
      </div>
    </div>
  )
}
