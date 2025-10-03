import React from 'react'
import { cn } from '@karrio/ui/lib/utils'

type CalloutProps = {
  children: React.ReactNode
  type?: 'default' | 'info' | 'warning' | 'error'
  icon?: React.ReactNode
  className?: string
}

export function Callout({
  children,
  type = 'default',
  icon,
  className,
  ...props
}: CalloutProps) {
  const typeMap = {
    default: 'bg-gray-100 border-gray-300 text-gray-800 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200',
    info: 'bg-blue-50 border-blue-300 text-blue-800 dark:bg-blue-900/30 dark:border-blue-800 dark:text-blue-300',
    warning: 'bg-yellow-50 border-yellow-300 text-yellow-800 dark:bg-yellow-900/30 dark:border-yellow-800 dark:text-yellow-300',
    error: 'bg-red-50 border-red-300 text-red-800 dark:bg-red-900/30 dark:border-red-800 dark:text-red-300',
  }

  return (
    <div
      className={cn(
        'border-l-4 p-4 my-6 rounded-r-md',
        typeMap[type],
        className
      )}
      {...props}
    >
      {icon && <div className="callout-icon mr-2">{icon}</div>}
      <div className="callout-content">{children}</div>
    </div>
  )
}