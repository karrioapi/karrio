import React from 'react';

type ThemeType = 'light' | 'dark' | 'platform';

interface ThemeProviderProps {
    theme: ThemeType;
    children: React.ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({
    theme,
    children,
}) => {
    const themeAttribute = theme === 'light' ? undefined : `data-theme="${theme}"`;

    return (
        <html
            lang="en"
            {...(themeAttribute ? { 'data-theme': theme } : {})}
            suppressHydrationWarning
        >
            <body className="min-h-screen font-sans antialiased">
                {children}
            </body>
        </html>
    );
};

// Usage example:
// <ThemeProvider theme="platform">
//   <YourLayout />
// </ThemeProvider>
