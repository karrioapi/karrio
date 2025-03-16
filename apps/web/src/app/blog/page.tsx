import { getPosts, getTags } from '@/lib/get-posts';
import { PostCard } from '@/components/blog/post-card';
import { Badge } from '@karrio/ui/components/ui/badge';
import Link from 'next/link';

export const metadata = {
  title: 'Blog - Karrio',
  description: 'Latest news, updates, and articles about Karrio'
};

export default async function BlogPage() {
  const posts = await getPosts();
  const tags = await getTags();

  return (
    <div>
      <div className="mb-10 pb-6 border-b dark:border-white/10">
        <h1 className="text-4xl font-bold mb-3 dark:text-white">Karrio Blog</h1>
        <p className="text-lg text-muted-foreground dark:text-white/70">
          Latest news, updates, and articles about Karrio shipping infrastructure
        </p>
      </div>

      {tags.length > 0 && (
        <div className="mb-10">
          <h2 className="text-xl font-semibold mb-3 dark:text-white">Browse by tag</h2>
          <div className="flex flex-wrap gap-2">
            {tags.map(tag => (
              <Link key={tag} href={`/blog/tags/${tag}`}>
                <Badge variant="outline" className="hover:bg-primary/10 dark:bg-[#2d1d51] dark:border-[#3a2466] dark:text-white/80 dark:hover:bg-[#3a2466]">
                  {tag}
                </Badge>
              </Link>
            ))}
          </div>
        </div>
      )}

      <div className="space-y-10">
        {posts.length > 0 ? (
          posts.map(post => (
            <PostCard key={post.route} post={post} />
          ))
        ) : (
          <div className="text-center py-10">
            <p className="text-muted-foreground dark:text-white/70">No posts yet. Check back soon!</p>
          </div>
        )}
      </div>
    </div>
  );
}
