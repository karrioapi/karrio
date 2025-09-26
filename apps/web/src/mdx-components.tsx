import { useMDXComponents as getNextraComponents } from 'nextra/mdx-components'
import { useMDXComponents as getBlogMDXComponents, BlogWrapper } from './blog-mdx-components'
import { CopyMarkdownButton } from '@/components/CopyMarkdownButton'

// For blog pages, use the blog MDX components
export const useMDXComponents = components => {
  // Get all components from blog
  const blogComponents = getBlogMDXComponents()

  const DocsH1 = (props) => {
    const { className = '', children, ...rest } = props || {}
    return (
      <h1
        {...rest}
        className={[
          className,
          // Mobile: stack vertically, left aligned; sm+: inline row with right actions
          'flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between'
        ].filter(Boolean).join(' ')}
      >
        <span>{children}</span>
        <CopyMarkdownButton />
      </h1>
    )
  }

  return {
    ...getNextraComponents({}),
    ...blogComponents,
    wrapper: props => {
      // Check if the path is from a blog page
      const isBlogPage = props.filepath?.includes('/blog/') || false

      if (isBlogPage) {
        return <BlogWrapper {...props} />
      }

      // For docs pages and others, just return children - NextraTheme handles theming
      const { children } = props
      return <>{children}</>
    },
    // For docs pages, override h1 to include the Copy button inline with title
    h1: DocsH1,
    ...components
  }
}
