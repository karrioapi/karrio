import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { IMAGES } from '@/lib/types';

const MULTI_TENANT = (
  Boolean(JSON.parse(process.env.MULTI_TENANT || 'false'))
);
export const config = {
  matcher: [
    /*
     * Match all paths except for:
     * 1. /api routes
     * 2. /_next (Next.js internals)
     * 3. /examples (inside /public)
     * 4. all root files inside /public (e.g. /favicon.ico)
     */
    "/((?!api/|_next/|_static/|[\\w-]+\\.\\w+).*)",
  ],
};

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const hostname = req.headers.get("host") as string;

  if (pathname.startsWith('/carriers')) {
    const unknown = IMAGES.filter(k => req.url.includes(k)).length === 0;
    if (unknown) {
      const name = req.url.split('/carriers/').pop();
      return NextResponse.rewrite(new URL(`/api/images/${name}`, req.url));
    }
    return;
  }

  if (MULTI_TENANT === false) return;

  // Prevent security issues – users should not be able to canonically access
  // the pages/sites folder and its respective contents. This can also be done
  // via rewrites to a custom 404 page
  if (pathname.startsWith(`/_sites`)) {
    return new Response(null, { status: 404 });
  }

  // rewrite everything else to `/_sites/[site] dynamic route
  return NextResponse.rewrite(
    new URL(`/_sites/${hostname}${pathname}`, req.url)
  );
}