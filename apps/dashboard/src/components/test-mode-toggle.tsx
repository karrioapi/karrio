import { useEffect, useState } from 'react'
import { authManager } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip'

// Custom Test Tube Icon SVG
function TestIcon({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <path d="M14.5 2v17.5c0 1.4-1.1 2.5-2.5 2.5s-2.5-1.1-2.5-2.5V2" />
      <path d="M8.5 2h7" />
      <path d="M14.5 16h-5" />
    </svg>
  )
}

export function TestModeToggle() {
  const [testMode, setTestMode] = useState(false)

  useEffect(() => {
    setTestMode(authManager.getTestMode())
  }, [])

  const handleToggle = () => {
    const newMode = !testMode
    authManager.setTestMode(newMode)
    setTestMode(newMode)
    // Reload to apply the new test mode context
    window.location.reload()
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            variant={testMode ? 'default' : 'outline'}
            size="sm"
            className="h-8 w-8 p-0"
            onClick={handleToggle}
          >
            <TestIcon className="h-4 w-4" />
          </Button>
        </TooltipTrigger>
        <TooltipContent>
          <p>{testMode ? 'Test Mode: ON' : 'Test Mode: OFF'}</p>
          <p className="text-xs text-muted-foreground">
            Click to {testMode ? 'disable' : 'enable'} test mode
          </p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
