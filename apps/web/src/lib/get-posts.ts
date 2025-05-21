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
  };
};

export async function getPosts(): Promise<Post[]> {
  const { directories } = normalizePages({
    list: await getPageMap('/blog'),
    route: '/blog'
  });

  return directories
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
        tags: post.frontMatter.tags
      }
    }))
    .sort((a, b) => new Date(b.frontMatter.date).getTime() - new Date(a.frontMatter.date).getTime());
}

export async function getTags(): Promise<string[]> {
  const posts = await getPosts();
  const tagSet = new Set<string>();

  posts.forEach(post => {
    if (post.frontMatter.tags) {
      post.frontMatter.tags.forEach(tag => tagSet.add(tag));
    }
  });

  return Array.from(tagSet);
}

export async function getPostsByTag(tag: string): Promise<Post[]> {
  const posts = await getPosts();
  return posts.filter(post =>
    post.frontMatter.tags && post.frontMatter.tags.includes(tag)
  );
}