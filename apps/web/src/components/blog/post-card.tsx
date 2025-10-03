import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@karrio/ui/components/ui/card';
import { Badge } from '@karrio/ui/components/ui/badge';
import { Post } from '@/lib/get-posts';
import { formatDate } from '@/lib/utils';
import Link from 'next/link';
import Image from 'next/image';

export function PostCard({ post }: { post: Post }) {
  const { title, date, description, tags, author, image, draft } = post.frontMatter;
  const isDraft = draft === true;
  const isDevelopment = process.env.NODE_ENV === 'development';

  return (
    <article className="group">
      <Link href={post.route}>
        <div className="mb-4 overflow-hidden rounded-lg relative">
          {image ? (
            <div className="relative aspect-[16/6] w-full overflow-hidden">
              <Image
                src={image}
                alt={title}
                className="object-cover transition-transform duration-500 group-hover:scale-105"
                fill
                sizes="(max-width: 768px) 100vw, 768px"
              />
            </div>
          ) : (
            <div className="relative aspect-[16/6] w-full overflow-hidden bg-gradient-to-br from-primary/10 to-secondary/10 dark:from-[#5722cc]/20 dark:to-purple-900/30" />
          )}

          {/* Draft indicator overlay - only show in development */}
          {isDraft && isDevelopment && (
            <div className="absolute top-3 right-3">
              <Badge variant="destructive" className="text-xs font-medium bg-yellow-500 hover:bg-yellow-600 text-black">
                DRAFT
              </Badge>
            </div>
          )}
        </div>
        <div>
          <div className="flex items-center gap-2 mb-2">
            <h2 className="text-2xl font-semibold group-hover:text-primary dark:group-hover:text-[#8a5cf5] transition-colors duration-200 dark:text-white flex-1">{title}</h2>
            {/* Small draft indicator next to title - only show in development */}
            {isDraft && isDevelopment && (
              <Badge variant="outline" className="text-xs border-yellow-500 text-yellow-600 dark:text-yellow-400">
                Draft
              </Badge>
            )}
          </div>
          <div className="mt-2 flex items-center text-sm text-muted-foreground dark:text-white/60">
            <time dateTime={date}>{formatDate(date)}</time>
            {author && (
              <>
                <span className="mx-1 dark:text-white/60">•</span>
                <span>{author}</span>
              </>
            )}
          </div>
          {description && (
            <p className="mt-3 text-muted-foreground dark:text-white/70 line-clamp-2">{description}</p>
          )}
          {tags && tags.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {tags.map(tag => (
                <Badge key={tag} variant="secondary" className="hover:bg-primary/20 dark:bg-[#2d1d51] dark:text-white/80 dark:hover:bg-[#3a2466]">
                  {tag}
                </Badge>
              ))}
            </div>
          )}
        </div>
      </Link>
    </article>
  );
}
