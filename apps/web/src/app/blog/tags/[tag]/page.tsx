import { getPostsByTag, getTags } from '@/lib/get-posts';
import { PostCard } from '@/components/blog/post-card';
import { notFound } from 'next/navigation';
import { Metadata } from 'next';

export async function generateStaticParams() {
  const tags = await getTags();
  return tags.map(tag => ({ tag }));
}

export async function generateMetadata({ params }: { params: { tag: string } }): Promise<Metadata> {
  return {
    title: `Posts tagged with ${params.tag} - Karrio Blog`
  };
}

type SegmentParams = { [key: string]: string | string[] | undefined };

interface PageProps {
  params?: Promise<SegmentParams>;
  searchParams?: Promise<any>;
}

export default async function TagPage({ params }: PageProps) {
  const resolvedParams = await params;
  const tag = resolvedParams?.tag as string;
  const posts = await getPostsByTag(tag);

  if (!posts.length) {
    notFound();
  }

  return (
    <div>
      <h1 className="text-4xl font-bold mb-2">Posts tagged with</h1>
      <div className="text-3xl font-bold text-primary mb-8">{tag}</div>

      <div className="space-y-8">
        {posts.map(post => (
          <PostCard key={post.route} post={post} />
        ))}
      </div>
    </div>
  );
}
