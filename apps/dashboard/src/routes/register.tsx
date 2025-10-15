import { createFileRoute, useRouter, Link } from '@tanstack/react-router'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { authManager } from '@/lib/auth'

export const Route = createFileRoute('/register')({
  component: RegisterPage,
  head: () => ({
    meta: [{ title: 'Register - JTL Shipping' }],
  }),
})

function RegisterPage() {
  const router = useRouter()

  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [tenantId, setTenantId] = useState('')
  const [userId, setUserId] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const validateForm = () => {
    if (!tenantId.trim()) {
      setError('Tenant ID is required')
      return false
    }

    if (!userId.trim()) {
      setError('User ID is required')
      return false
    }

    if (!email.trim()) {
      setError('Email is required')
      return false
    }

    if (!email.includes('@')) {
      setError('Please enter a valid email address')
      return false
    }

    if (!password.trim()) {
      setError('Password is required')
      return false
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long')
      return false
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return false
    }

    return true
  }

  const handleRegister = async () => {
    if (!validateForm()) {
      return
    }

    try {
      setError(null)
      setSuccess(null)
      setIsLoading(true)

      await authManager.registerJTLTenant({
        tenantId,
        userId,
        email,
        password,
      })

      setSuccess('Registration successful! Redirecting to sign in...')

      // Redirect to signin page after a short delay
      setTimeout(() => {
        router.navigate({ to: '/signin' })
      }, 1500)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed')
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleRegister()
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background py-12 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <img src="/logo.svg" alt="JTL Shipping" className="h-12 w-auto" />
          </div>
          <h1 className="text-2xl font-bold text-foreground">Create your account</h1>
          <p className="text-sm text-muted-foreground mt-2">
            Register your JTL tenant to get started
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

            {success && (
              <Alert className="mb-6 bg-green-50 border-green-200 dark:bg-green-950 dark:border-green-800">
                <AlertDescription className="text-green-800 dark:text-green-200">
                  {success}
                </AlertDescription>
              </Alert>
            )}

            <div className="space-y-4">
              <div>
                <Label htmlFor="tenantId">
                  Tenant ID <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="tenantId"
                  type="text"
                  value={tenantId}
                  onChange={(e) => setTenantId(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Your JTL tenant ID (UUID)"
                  disabled={isLoading}
                  className="mt-2"
                />
                <p className="mt-1 text-xs text-muted-foreground">
                  Your unique JTL tenant identifier
                </p>
              </div>

              <div>
                <Label htmlFor="userId">
                  User ID <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="userId"
                  type="text"
                  value={userId}
                  onChange={(e) => setUserId(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Your JTL user ID (UUID)"
                  disabled={isLoading}
                  className="mt-2"
                />
                <p className="mt-1 text-xs text-muted-foreground">
                  Your unique JTL user identifier
                </p>
              </div>

              <div>
                <Label htmlFor="email">
                  Email <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="you@example.com"
                  disabled={isLoading}
                  className="mt-2"
                />
                <p className="mt-1 text-xs text-muted-foreground">
                  Your email address for login
                </p>
              </div>

              <div>
                <Label htmlFor="password">
                  Password <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Create a strong password"
                  disabled={isLoading}
                  className="mt-2"
                />
                <p className="mt-1 text-xs text-muted-foreground">
                  Must be at least 8 characters long
                </p>
              </div>

              <div>
                <Label htmlFor="confirmPassword">
                  Confirm Password <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Re-enter your password"
                  disabled={isLoading}
                  className="mt-2"
                />
              </div>

              <Button
                onClick={handleRegister}
                disabled={isLoading || !!success}
                className="w-full"
                size="lg"
              >
                {isLoading ? 'Creating account...' : success ? 'Redirecting...' : 'Create Account'}
              </Button>
            </div>

            <p className="text-xs text-muted-foreground text-center mt-6">
              By creating an account, you agree to our Terms of Service and Privacy Policy
            </p>
          </CardContent>
        </Card>

        <div className="text-center mt-6 text-sm text-muted-foreground">
          Already have an account?{' '}
          <Link
            to="/signin"
            className="font-semibold text-primary hover:underline"
          >
            Sign in here
          </Link>
        </div>
      </div>
    </div>
  )
}
