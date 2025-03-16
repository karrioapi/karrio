import { BlogPostLayout } from '@/components/blog/blog-post-layout';

export function useMDXComponents(components: any) {
  return {
    ...components,
    // Add blog-specific components here
    BlogPostLayout
  };
}