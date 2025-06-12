import { ThemeConfig, getThemeConfig } from '@/types/theme'
import type { FC, ReactNode } from 'react'
import type { PageMapItem } from 'nextra'
import { headers } from 'next/headers'
import { NextraThemeClient } from '@/components/nextra/theme-client'

// Server component wrapper that extracts theme config
export default async function NextraTheme({
  children,
  pageMap
}: {
  children: ReactNode
  pageMap: PageMapItem[]
}) {
  const headersList = await headers()
  const currentRoute = headersList.get('x-pathname') || ''

  const themeConfig = getThemeConfig(pageMap, currentRoute)

  return (
    <NextraThemeClient
      pageMap={pageMap}
      themeConfig={themeConfig}
    >
      {children}
    </NextraThemeClient>
  )
}
