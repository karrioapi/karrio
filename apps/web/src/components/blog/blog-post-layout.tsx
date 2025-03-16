import { Badge } from '@karrio/ui/components/ui/badge';
import { formatDate } from '@/lib/utils';
import Link from 'next/link';

export function BlogPostLayout({
  title,
  date,
  tags,
  children
}: {
  title: string;
  date: string;
  tags?: string[];
  children: React.ReactNode;
}) {
  return (
    <article className="prose dark:prose-invert max-w-none">
      <div className="mb-10">
        <h1 className="mb-2">{title}</h1>
        <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
          <time dateTime={date}>{formatDate(date)}</time>
          {tags && tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {tags.map(tag => (
                <Link key={tag} href={`/blog/tags/${tag}`}>
                  <Badge variant="outline" className="hover:bg-primary/10">
                    {tag}
                  </Badge>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
      {children}
    </article>
  );
}