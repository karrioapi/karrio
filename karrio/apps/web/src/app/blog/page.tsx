import { PostCard } from '@/components/blog/post-card';
import { getPosts, getTags } from '@/lib/get-posts';

export const metadata = {
  title: 'Blog - Karrio',
  description: 'Latest news, updates, and articles about Karrio'
};

export default async function BlogPage() {
  const posts = await getPosts();
  const tags = await getTags();

  return (
    <div className="py-16">
      <div className="mb-8 pb-4 border-b dark:border-white/10">
        <h2 className="text-3xl font-bold mb-4 dark:text-white">The Latest Karrio News</h2>
      </div>

      <div className="space-y-10 mb-8">
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
