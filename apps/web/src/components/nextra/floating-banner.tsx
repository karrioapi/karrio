"use client"
import Link from 'next/link'
import { useState, useEffect } from 'react'

export const FloatingBanner = () => {
    const [isVisible, setIsVisible] = useState(true)
    const [lastScrollY, setLastScrollY] = useState(0)

    useEffect(() => {
        const handleScroll = () => {
            const currentScrollY = window.scrollY

            // Hide banner when scrolling down, show when scrolling up or at top
            if (currentScrollY > lastScrollY && currentScrollY > 50) {
                setIsVisible(false)
            } else {
                setIsVisible(true)
            }

            setLastScrollY(currentScrollY)
        }

        window.addEventListener('scroll', handleScroll, { passive: true })
        return () => window.removeEventListener('scroll', handleScroll)
    }, [lastScrollY])

    return (
        <div
            className={`fixed top-16 left-1/2 transform -translate-x-1/2 z-50 transition-all duration-300 md:ml-32 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'
                }`}
        >
            <div className="bg-blue-50 dark:bg-blue-900/50 border border-blue-200 dark:border-blue-700 rounded-lg shadow-sm backdrop-blur-sm px-4 py-2 mx-4">
                <p className="text-xs text-blue-700 dark:text-blue-300 mb-0 whitespace-nowrap">
                    📖 Looking for karrio's legacy docs? Visit {' '}
                    <Link
                        href="https://docs.karrio.io"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-medium underline hover:no-underline text-blue-700 dark:text-blue-300"
                    >
                        docs.karrio.io
                    </Link>
                </p>
            </div>
        </div>
    )
}
