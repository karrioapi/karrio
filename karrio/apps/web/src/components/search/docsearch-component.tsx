"use client";

import React, { useEffect, useState, useCallback, useRef } from 'react';
import { usePathname } from 'next/navigation';

// Declare types for DocSearch
declare global {
    interface Window {
        docsearch: any;
        _algoliaDocSearchInstance?: any;
    }
}

interface DocSearchWrapperProps {
    className?: string;
    buttonText?: string;
}

export function DocSearchWrapper({
    className = '',
    buttonText = 'Search documentation...'
}: DocSearchWrapperProps) {
    const [docSearchLoaded, setDocSearchLoaded] = useState(false);
    const [docSearchInitialized, setDocSearchInitialized] = useState(false);
    const buttonRef = useRef<HTMLButtonElement>(null);
    const pathname = usePathname();

    // Determine if the current page is a documentation or blog page
    const facetFilters = pathname?.startsWith('/blog')
        ? ['type:blog']
        : ['type:docs'];

    // Load DocSearch dynamically
    useEffect(() => {
        if (typeof window === 'undefined') return;

        // Only load once
        if (docSearchLoaded) return;

        console.log('Loading DocSearch scripts and styles...');

        // Load DocSearch CSS
        const cssLink = document.createElement('link');
        cssLink.rel = 'stylesheet';
        cssLink.href = 'https://cdn.jsdelivr.net/npm/@docsearch/css@3';
        document.head.appendChild(cssLink);

        // Load DocSearch JS
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/@docsearch/js@3';
        script.onload = () => {
            console.log('DocSearch script loaded successfully');
            setDocSearchLoaded(true);
        };
        script.onerror = (err) => {
            console.error('Failed to load DocSearch:', err);
        };
        document.body.appendChild(script);

        return () => {
            // Cleanup if component unmounts
            if (document.head.contains(cssLink)) {
                document.head.removeChild(cssLink);
            }
            if (document.body.contains(script)) {
                document.body.removeChild(script);
            }
        };
    }, []);

    // Initialize DocSearch once loaded
    useEffect(() => {
        if (!docSearchLoaded || !window.docsearch || docSearchInitialized) return;

        console.log('Initializing DocSearch...');

        try {
            // Initialize DocSearch
            const docsearchInstance = window.docsearch({
                appId: process.env.NEXT_PUBLIC_ALGOLIA_APP_ID,
                apiKey: process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY,
                indexName: process.env.NEXT_PUBLIC_ALGOLIA_INDEX_NAME,
                container: '#docsearch-container',
                searchParameters: {
                    facetFilters: facetFilters
                },
                transformItems: (items: any[]) => {
                    return items.map((item) => {
                        // Strip the hash from the URL if it exists
                        const a = document.createElement('a');
                        a.href = item.url;

                        // Clean up the URL
                        const hash = a.hash === '#content-wrapper' ? '' : a.hash;

                        return {
                            ...item,
                            url: `${a.pathname}${hash}`,
                        };
                    });
                }
            });

            console.log('DocSearch initialized successfully');
            setDocSearchInitialized(true);

            // Store the docsearch instance
            window._algoliaDocSearchInstance = docsearchInstance;
        } catch (error) {
            console.error('Error initializing DocSearch:', error);
        }
    }, [docSearchLoaded, facetFilters, docSearchInitialized]);

    // Handle opening the search modal
    const handleDocSearchOpen = useCallback(() => {
        if (!docSearchLoaded) {
            console.warn('DocSearch not loaded yet');
            return;
        }

        console.log('Opening DocSearch modal...');

        // Use the stored instance or try to find the trigger directly
        if (window._algoliaDocSearchInstance) {
            console.log('Using stored DocSearch instance');
            window._algoliaDocSearchInstance.open();
        } else {
            // Fallback to using keyboard shortcut
            console.log('Using keyboard shortcut fallback');
            const isMac = /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform);
            const event = new KeyboardEvent('keydown', {
                key: 'k',
                code: 'KeyK',
                metaKey: isMac,
                ctrlKey: !isMac,
                bubbles: true
            });
            document.dispatchEvent(event);
        }
    }, [docSearchLoaded]);

    // Set up keyboard shortcuts for opening the search modal
    useEffect(() => {
        if (!docSearchLoaded) return;

        const handleKeyDown = (event: KeyboardEvent) => {
            // Check for Cmd+K or Ctrl+K
            if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
                event.preventDefault();
                handleDocSearchOpen();
            }
        };

        document.addEventListener('keydown', handleKeyDown);
        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [docSearchLoaded, handleDocSearchOpen]);

    return (
        <>
            <button
                ref={buttonRef}
                type="button"
                className={`DocSearch-Button ${className}`}
                onClick={handleDocSearchOpen}
                aria-label="Search documentation"
            >
                <span className="DocSearch-Button-Container">
                    <svg
                        width="20"
                        height="20"
                        className="DocSearch-Search-Icon"
                        viewBox="0 0 20 20"
                    >
                        <path
                            d="M14.386 14.386l4.0877 4.0877-4.0877-4.0877c-2.9418 2.9419-7.7115 2.9419-10.6533 0-2.9419-2.9418-2.9419-7.7115 0-10.6533 2.9418-2.9419 7.7115-2.9419 10.6533 0 2.9419 2.9418 2.9419 7.7115 0 10.6533z"
                            stroke="currentColor"
                            fill="none"
                            fillRule="evenodd"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                    </svg>
                    <span className="DocSearch-Button-Placeholder">{buttonText}</span>
                </span>
                <span className="DocSearch-Button-Keys">
                    <kbd className="DocSearch-Button-Key">⌘</kbd>
                    <kbd className="DocSearch-Button-Key">K</kbd>
                </span>
            </button>
            {/* Hidden container for DocSearch to initialize into */}
            <div id="docsearch-container" style={{ display: 'none' }} />
        </>
    );
}
