import { useMDXComponents as getNextraComponents } from 'nextra/mdx-components'
import { useMDXComponents as getBlogMDXComponents, BlogWrapper } from './blog-mdx-components'

// For blog pages, use the blog MDX components
export const useMDXComponents = components => {
  // Get all components from blog
  const blogComponents = getBlogMDXComponents()

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
    ...components
  }
}
