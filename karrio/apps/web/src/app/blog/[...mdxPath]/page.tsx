import { generateStaticParamsFor, importPage } from 'nextra/pages'
import { useMDXComponents as getMDXComponents, BlogWrapper } from '@/blog-mdx-components'
import { notFound } from 'next/navigation'

export const generateStaticParams = generateStaticParamsFor('mdxPath')

export async function generateMetadata(props) {
  const params = await props.params
  const { metadata } = await importPage(params.mdxPath)

  // Return metadata even for drafts (for development), but check in the component
  return metadata
}

export default async function Page(props) {
  const params = await props.params
  const result = await importPage(params.mdxPath)
  const { default: MDXContent, toc, metadata } = result

  // Check if this is a draft post in production
  const isDraft = (metadata as any)?.draft === true
  const isProduction = process.env.NODE_ENV === 'production'

  if (isDraft && isProduction) {
    notFound() // Return 404 for draft posts in production
  }

  return (
    <BlogWrapper toc={toc} metadata={metadata}>
      <MDXContent {...props} params={params} />
    </BlogWrapper>
  )
}
