import * as React from 'react'
import { Badge } from './badge'
import { cn } from '@/lib/utils'

interface StatusBadgeProps {
  status: string
  variant?: 'default' | 'secondary' | 'destructive' | 'outline'
  className?: string
}

const statusVariants = {
  // Connection statuses
  active: 'bg-green-100 dark:bg-green-950 text-green-800 dark:text-green-200 border-green-200 dark:border-green-800',
  inactive: 'bg-muted text-muted-foreground border-border',
  enabled: 'bg-green-100 dark:bg-green-950 text-green-800 dark:text-green-200 border-green-200 dark:border-green-800',
  disabled: 'bg-muted text-muted-foreground border-border',

  // Test mode
  test: 'bg-orange-100 dark:bg-orange-950 text-orange-800 dark:text-orange-200 border-orange-200 dark:border-orange-800',
  live: 'bg-green-100 dark:bg-green-950 text-green-800 dark:text-green-200 border-green-200 dark:border-green-800',

  // Generic statuses
  success: 'bg-green-100 dark:bg-green-950 text-green-800 dark:text-green-200 border-green-200 dark:border-green-800',
  failed: 'bg-red-100 dark:bg-red-950 text-red-800 dark:text-red-200 border-red-200 dark:border-red-800',
  running: 'bg-primary/10 text-primary border-primary/20',
  unknown: 'bg-muted text-muted-foreground border-border',
} as const

const formatStatus = (status: string) => {
  return status
    .split(/[\s_-]/)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  variant = 'secondary',
  className,
}) => {
  const normalizedStatus = status?.toLowerCase().replace(/\s+/g, '_')
  const statusClass =
    statusVariants[normalizedStatus as keyof typeof statusVariants]

  return (
    <Badge
      variant={variant}
      className={cn('text-xs px-2 py-1 border', statusClass, className)}
    >
      {formatStatus(status || '')}
    </Badge>
  )
}
