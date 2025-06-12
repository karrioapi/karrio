export interface ThemeConfig {
    breadcrumb?: boolean
    footer?: boolean
    layout?: 'default' | 'full' | 'raw'
    navbar?: boolean
    pagination?: boolean
    sidebar?: boolean
    timestamp?: boolean
    toc?: boolean
    typesetting?: 'default' | 'article'
}

// Helper function to get theme config from pageMap
export const getThemeConfig = (pageMap: any[], currentRoute: string): ThemeConfig => {
    if (!pageMap || !currentRoute) {
        console.log('getThemeConfig: Missing pageMap or currentRoute', { pageMap: !!pageMap, currentRoute })
        return {}
    }

    console.log('getThemeConfig: Searching for theme config', {
        currentRoute,
        pageMapLength: pageMap.length,
        routeParts: currentRoute.split('/').filter(Boolean)
    })

    // Find the theme configuration for the current route
    const findThemeConfig = (items: any[], route: string): any => {
        const routeParts = route.split('/').filter(Boolean)

        console.log('findThemeConfig: Looking for route:', route)
        console.log('findThemeConfig: Route parts:', routeParts)

        // For /docs/products, we need to navigate: find 'docs' item -> find 'products' child -> get data
        if (routeParts.length >= 2 && routeParts[0] === 'docs') {
            console.log('findThemeConfig: Processing docs route')

            // Find the docs item
            const docsItem = items.find(item => item.name === 'docs')
            if (!docsItem) {
                console.log('findThemeConfig: docs item not found')
                return null
            }

            console.log('findThemeConfig: Found docs item, has children:', !!docsItem.children)

            if (!docsItem.children) return null

            // Find the specific section (e.g., 'products')
            const sectionName = routeParts[1] // 'products'
            const sectionItem = docsItem.children.find(child => child.name === sectionName)

            if (!sectionItem) {
                console.log('findThemeConfig: section item not found:', sectionName)
                return null
            }

            console.log('findThemeConfig: Found section item:', sectionName, 'has children:', !!sectionItem.children)

            if (!sectionItem.children) return null

            // Look for specific page config in section children
            if (routeParts.length >= 3) {
                // For specific pages like /docs/products/carrier-connections
                const pageName = routeParts[2]

                for (const child of sectionItem.children) {
                    if (child.data) {
                        console.log('findThemeConfig: Found data in section child, keys:', Object.keys(child.data))

                        const pageConfig = child.data[pageName]
                        if (pageConfig?.theme) {
                            console.log('findThemeConfig: Found page theme config for', pageName, ':', pageConfig.theme)
                            return pageConfig.theme
                        }
                    }
                }
            } else if (routeParts.length === 2) {
                // For section index pages like /docs/products
                for (const child of sectionItem.children) {
                    if (child.data) {
                        console.log('findThemeConfig: Found data in section child, keys:', Object.keys(child.data))

                        const indexConfig = child.data['index']
                        if (indexConfig?.theme) {
                            console.log('findThemeConfig: Found index theme config:', indexConfig.theme)
                            return indexConfig.theme
                        }
                    }
                }
            }
        }

        // Fallback: direct route matching
        for (const item of items) {
            if (item.route === route) {
                console.log('findThemeConfig: Found direct route match:', route)

                if (item.frontMatter?.theme) {
                    console.log('findThemeConfig: Found frontMatter theme:', item.frontMatter.theme)
                    return item.frontMatter.theme
                }
            }

            // Recursively search in children
            if (item.children) {
                const found = findThemeConfig(item.children, route)
                if (found) return found
            }
        }

        console.log('findThemeConfig: No theme config found')
        return null
    }

    const config = findThemeConfig(pageMap, currentRoute) || {}

    // Set default values - TOC should be true by default
    const finalConfig = {
        toc: true,  // Default to true
        ...config   // Override with any specific config found
    }

    console.log('Final theme config for route', currentRoute, ':', finalConfig)
    return finalConfig
}
