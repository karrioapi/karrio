import { MDXPageWrapper } from "@/components/mdx-page-wrapper";

export default function MDXLayout({ children }: { children: React.ReactNode }) {
  return (
    <MDXPageWrapper>{children}</MDXPageWrapper>
  )
}
