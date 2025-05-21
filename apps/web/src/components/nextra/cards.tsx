import { FC, ReactNode } from 'react'
import Link from 'next/link'
import clsx from 'clsx'

interface FeatureCardProps {
  title: string
  description: string
  icon: ReactNode
  href: string
}

export const FeatureCard: FC<FeatureCardProps> = ({ title, description, icon, href }) => {
  return (
    <Link href={href} className="group no-underline">
      <div className="relative flex flex-col h-full items-start rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:border-gray-300 hover:shadow-md dark:border-neutral-800 dark:bg-neutral-900 dark:hover:border-neutral-700 group-hover:bg-gray-50 dark:group-hover:bg-neutral-800 card-container">
        <div className="flex items-center mb-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gray-100 text-black dark:bg-neutral-800 dark:text-white group-hover:bg-gray-200 dark:group-hover:bg-neutral-700 card-icon">
            {icon}
          </div>
          <h3 className="ml-3 text-base font-medium text-black dark:text-white card-title">{title}</h3>
        </div>
        <p className="text-sm text-gray-600 dark:text-neutral-300 card-description">{description}</p>
      </div>
    </Link>
  )
}

interface FeatureGridProps {
  children: ReactNode
  className?: string
}

export const FeatureGrid: FC<FeatureGridProps> = ({ children, className }) => {
  return (
    <div className={clsx("mt-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3", className)}>
      {children}
    </div>
  )
}

interface QuickLinksProps {
  className?: string
}

export const QuickLinks: FC<QuickLinksProps> = ({ className }) => {
  return (
    <FeatureGrid className={className}>
      <FeatureCard
        title="Start developing"
        description="Follow our quickstart guide to start developing with Karrio"
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        }
        href="/docs/introduction"
      />
      <FeatureCard
        title="Self Host"
        description="Learn how to self-host Karrio for controlled instance"
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2" />
          </svg>
        }
        href="/docs/self-hosting"
      />
    </FeatureGrid>
  )
}

export const ApiLinks: FC<QuickLinksProps> = ({ className }) => {
  return (
    <FeatureGrid className={className}>
      <FeatureCard
        title="API"
        description="Learn how to use Karrio's API to CRUD various Karrio resources programmatically"
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        }
        href="/docs/api-v2-reference"
      />
    </FeatureGrid>
  )
}
