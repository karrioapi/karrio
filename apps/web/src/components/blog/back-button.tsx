'use client'

import { Button } from "@karrio/ui/components/ui/button"
import { ChevronLeftIcon } from "@radix-ui/react-icons"
import Link from 'next/link'
import React from 'react'

export interface BackButtonProps {
    href?: string
    onClick?: () => void
    className?: string
}

export function BackButton({ href = '/blog', onClick, className = '' }: BackButtonProps) {
    if (onClick) {
        return (
            <Button
                variant="ghost"
                size="sm"
                onClick={onClick}
                className={`mb-4 flex items-center gap-1 ${className}`}
            >
                <ChevronLeftIcon className="h-4 w-4" />
                Back to Blog
            </Button>
        )
    }

    return (
        <Link href={href}>
            <Button
                variant="ghost"
                size="sm"
                className={`mb-4 flex items-center gap-1 ${className}`}
            >
                <ChevronLeftIcon className="h-4 w-4" />
                Back to Blog
            </Button>
        </Link>
    )
}
