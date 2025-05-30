import { useMDXComponents as getNextraComponents } from 'nextra/mdx-components'
import { useMDXComponents as getBlogMDXComponents, BlogWrapper } from './blog-mdx-components'
import { DocsWrapper } from './components/docs/docs-wrapper'

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
      const isDocsPage = props.filepath?.includes('/docs/') || false

      if (isBlogPage) {
        return <BlogWrapper {...props} />
      }

      if (isDocsPage) {
        return <DocsWrapper pageMap={props.pageMap}>{props.children}</DocsWrapper>
      }

      // For non-blog/docs pages, just show the content
      const { children } = props
      return <>{children}</>
    },
    ...components
  }
}
