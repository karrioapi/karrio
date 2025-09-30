import { Navigate, createFileRoute, useRouter } from '@tanstack/react-router'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { oauth } from '@/lib/oauth'

export const Route = createFileRoute('/signin')({
  component: SignInPage,
})

function SignInPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    // Simulate authentication
    if (formData.email && formData.password) {
      // In a real app, you'd call your auth API here
      localStorage.setItem('isAuthenticated', 'true')
      router.navigate({ to: '/dashboard' })
    } else {
      setError('Please fill in all fields')
    }
    setIsLoading(false)
  }

  const handleInputChange =
    (field: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
      setFormData((prev) => ({ ...prev, [field]: e.target.value }))
      if (error) setError(null)
    }

  const handleOAuthLogin = () => {
    try {
      const authUrl = oauth.getAuthorizationUrl()
      window.location.href = authUrl
    } catch (err) {
      setError(err instanceof Error ? err.message : 'OAuth configuration error')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">JTL App</h1>
        </div>

        <Card className="border border-gray-200 shadow-sm">
          <CardContent className="p-8">
            <h2 className="text-xl font-semibold text-center mb-6">
              Sign in to your account
            </h2>

            {error && (
              <Alert variant="destructive" className="mb-4">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* OAuth Login Button */}
            <div className="space-y-4 mb-6">
              <Button
                type="button"
                onClick={handleOAuthLogin}
                className="w-full bg-blue-600 hover:bg-blue-700"
                disabled={isLoading}
              >
                Sign in with Karrio
              </Button>
            </div>

            {/* Divider */}
            <div className="relative mb-6">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white px-2 text-muted-foreground">
                  Or continue with email
                </span>
              </div>
            </div>

            {/* Traditional Email/Password Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange('email')}
                  placeholder="Enter your email"
                  required
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password">Password</Label>
                  <button
                    type="button"
                    className="text-sm text-blue-600 hover:underline"
                    onClick={() => console.log('Forgot password clicked')}
                  >
                    Forgot your password?
                  </button>
                </div>
                <Input
                  id="password"
                  type="password"
                  value={formData.password}
                  onChange={handleInputChange('password')}
                  placeholder="Enter your password"
                  required
                />
              </div>

              <Button
                type="submit"
                className="w-full"
                variant="outline"
                disabled={isLoading}
              >
                {isLoading ? 'Signing in...' : 'Sign in with Email'}
              </Button>
            </form>
          </CardContent>
        </Card>

        <div className="text-center mt-6 text-sm text-gray-600">
          Don't have an account?{' '}
          <button className="font-semibold text-blue-600 hover:underline">
            Sign up
          </button>
        </div>
      </div>
    </div>
  )
}
