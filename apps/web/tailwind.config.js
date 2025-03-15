/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx,md,mdx}",
    "./docs/**/*.{md,mdx}",
    "./blog/**/*.{md,mdx}"
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  important: '#tailwind-selector',
  theme: {
    extend: {
      colors: {
        // Brand primary color - purple
        'karrio-purple': '#5722cc',
        'primary': '#5722cc',
        'primary-light': '#6f3dd4',
        'primary-dark': '#481da8',

        // Brand secondary color - teal
        'karrio-teal': '#79e5dd',
        'secondary': '#79e5dd',
        'secondary-light': '#8fe9e3',
        'secondary-dark': '#57d6cc',

        // Brand accent color - orange/red
        'karrio-orange': '#ff4800',
        'accent': '#ff4800',
        'accent-light': '#ff6933',
        'accent-dark': '#cc3a00',

        // Platform specific colors - dark mode
        'platform-purple': '#5722cc',
        'platform-purple-light': '#6f3dd4',
        'platform-purple-dark': '#481da8',
        'platform-teal': '#79e5dd',

        // Platform background colors - dark mode
        'platform-background': '#121212',
        'platform-card': '#1e1e1e',
        'platform-border': '#2e2e2e',
        'platform-muted': '#2a2a2a',
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            a: {
              color: theme('colors.primary'),
              '&:hover': {
                color: theme('colors.primary-dark'),
              },
            },
            h1: {
              color: theme('colors.gray.900'),
            },
            h2: {
              color: theme('colors.gray.900'),
            },
            h3: {
              color: theme('colors.gray.900'),
            },
            code: {
              color: theme('colors.pink.500'),
              backgroundColor: theme('colors.gray.100'),
              padding: '0.2em 0.4em',
              borderRadius: '0.25rem',
              fontWeight: '500',
            },
          },
        },
        dark: {
          css: {
            color: theme('colors.gray.300'),
            a: {
              color: theme('colors.platform-purple'),
              '&:hover': {
                color: theme('colors.platform-purple-light'),
              },
            },
            h1: {
              color: theme('colors.white'),
            },
            h2: {
              color: theme('colors.white'),
            },
            h3: {
              color: theme('colors.white'),
            },
            code: {
              color: theme('colors.pink.400'),
              backgroundColor: theme('colors.platform-muted'),
            },
          },
        },
      }),
    },
  },
  plugins: [require('@tailwindcss/typography')],
  corePlugins: {
    preflight: false,
  },
}
