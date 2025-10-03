import { normalizePages } from 'nextra/normalize-pages';
import { getPageMap } from 'nextra/page-map';

export type Post = {
  route: string;
  name: string;
  frontMatter: {
    title: string;
    date: string;
    description?: string;
    author?: string;
    image?: string;
    tags?: string[];
    draft?: boolean;
  };
};

// Helper function to determine if we should show draft posts
function shouldShowDrafts(): boolean {
  return process.env.NODE_ENV === 'development';
}

// Helper function to filter out draft posts based on environment
function filterDraftPosts(posts: any[]): any[] {
  if (shouldShowDrafts()) {
    return posts; // Show all posts in development
  }
  return posts.filter(post => !post.frontMatter?.draft); // Hide drafts in production
}

export async function getPosts(): Promise<Post[]> {
  const { directories } = normalizePages({
    list: await getPageMap('/blog'),
    route: '/blog'
  });

  const allPosts = directories
    .filter(post =>
      post.name !== 'index' &&
      !post.name.startsWith('_') &&
      post.frontMatter?.title &&
      post.frontMatter?.date
    )
    .map(post => ({
      route: post.route,
      name: post.name,
      frontMatter: {
        title: post.frontMatter.title,
        date: post.frontMatter.date,
        description: post.frontMatter.description,
        author: post.frontMatter.author,
        image: post.frontMatter.image,
        tags: post.frontMatter.tags,
        draft: post.frontMatter.draft
      }
    }));

  // Filter drafts based on environment
  const filteredPosts = filterDraftPosts(allPosts);

  return filteredPosts
    .sort((a, b) => new Date(b.frontMatter.date).getTime() - new Date(a.frontMatter.date).getTime());
}

export async function getTags(): Promise<string[]> {
  const posts = await getPosts(); // This already filters drafts
  const tagSet = new Set<string>();

  posts.forEach(post => {
    if (post.frontMatter.tags) {
      post.frontMatter.tags.forEach(tag => tagSet.add(tag));
    }
  });

  return Array.from(tagSet);
}

export async function getPostsByTag(tag: string): Promise<Post[]> {
  const posts = await getPosts(); // This already filters drafts
  return posts.filter(post =>
    post.frontMatter.tags && post.frontMatter.tags.includes(tag)
  );
}

// New function to get a specific post (useful for checking draft status)
export async function getPostByRoute(route: string): Promise<Post | null> {
  const { directories } = normalizePages({
    list: await getPageMap('/blog'),
    route: '/blog'
  });

  const post = directories.find(p => p.route === route);

  if (!post || post.name === 'index' || post.name.startsWith('_') ||
    !post.frontMatter?.title || !post.frontMatter?.date) {
    return null;
  }

  return {
    route: post.route,
    name: post.name,
    frontMatter: {
      title: post.frontMatter.title,
      date: post.frontMatter.date,
      description: post.frontMatter.description,
      author: post.frontMatter.author,
      image: post.frontMatter.image,
      tags: post.frontMatter.tags,
      draft: post.frontMatter.draft
    }
  };
}
