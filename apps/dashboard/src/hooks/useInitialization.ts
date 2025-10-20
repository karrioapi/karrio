import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { authManager } from '@/lib/auth'

/**
 * Hook to track API and Auth initialization state
 * This ensures that queries don't run before the system is ready
 */
export function useInitialization() {
  const [isInitialized, setIsInitialized] = useState(false)

  useEffect(() => {
    let mounted = true

    async function initialize() {
      try {
        // Initialize both API and auth manager in parallel
        await Promise.all([
          api.initialize(),
          authManager.initialize(),
        ])

        if (mounted) {
          setIsInitialized(true)
        }
      } catch (error) {
        console.error('Initialization error:', error)
        // Still mark as initialized to allow the app to work with fallbacks
        if (mounted) {
          setIsInitialized(true)
        }
      }
    }

    initialize()

    return () => {
      mounted = false
    }
  }, [])

  return { isInitialized }
}
