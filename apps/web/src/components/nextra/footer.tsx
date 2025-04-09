"use client"

import type { FC } from 'react'
import { Github, Linkedin } from "lucide-react"

export const Footer: FC = () => {
  return (
    <footer className="w-full border-t border-border bg-background px-0 py-6 dark:border-white/10">
      <div className="mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
        <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
          <div className="flex items-center space-x-5">
            <a
              href="https://github.com/karrioapi/karrio"
              target="_blank"
              rel="noopener noreferrer"
              className="text-foreground/60 hover:text-foreground dark:text-white/60 dark:hover:text-white transition-colors"
            >
              <Github className="h-5 w-5" />
              <span className="sr-only">GitHub</span>
            </a>

            <a
              href="https://linkedin.com/company/karrio"
              target="_blank"
              rel="noopener noreferrer"
              className="text-foreground/60 hover:text-foreground dark:text-white/60 dark:hover:text-white transition-colors"
            >
              <Linkedin className="h-5 w-5" />
              <span className="sr-only">LinkedIn</span>
            </a>
          </div>

          <div className="text-xs text-foreground/60 dark:text-white/60">
            © {new Date().getFullYear()} Karrio, Inc. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  )
}
