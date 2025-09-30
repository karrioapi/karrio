import { getPosts } from '../../../lib/get-posts';
import { NextResponse } from 'next/server';

export async function GET() {
  const posts = await getPosts();
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://karrio.io';

  const rss = `
    <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
      <channel>
        <title>Karrio Blog</title>
        <link>${baseUrl}/blog</link>
        <description>Latest news, updates and articles about Karrio</description>
        <language>en</language>
        <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
        <atom:link href="${baseUrl}/blog/feed.xml" rel="self" type="application/rss+xml"/>
        ${posts
      .map(
        post => `
              <item>
                <title>${post.frontMatter.title}</title>
                <link>${baseUrl}${post.route}</link>
                <description>${post.frontMatter.description || ''}</description>
                <pubDate>${new Date(post.frontMatter.date).toUTCString()}</pubDate>
                <guid>${baseUrl}${post.route}</guid>
              </item>
            `
      )
      .join('')}
      </channel>
    </rss>
  `.trim();

  return new NextResponse(rss, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600, s-maxage=21600'
    }
  });
}
