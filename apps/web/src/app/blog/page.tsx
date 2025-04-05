import { PostCard } from '@/components/blog/post-card';
import { Badge } from '@karrio/ui/components/ui/badge';
import { getPosts, getTags } from '@/lib/get-posts';
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
      <div className="mb-8 pb-4 border-b dark:border-white/10">
        <h2 className="text-3xl font-bold mb-3 dark:text-white">The Latest Karrio News</h2>
      </div>

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
