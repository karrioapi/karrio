import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Redirect /docs to /docs/developing/introduction
  if (request.nextUrl.pathname === '/docs') {
    return NextResponse.redirect(new URL('/docs/developing', request.url))
  }

  // Clone the request headers and add pathname
  const response = NextResponse.next()

  // Add the current pathname to headers for server components
  response.headers.set('x-pathname', request.nextUrl.pathname)

  return response
}

export const config = {
  matcher: [
    /*
     * Match all paths except for:
     * 1. /api routes
     * 2. /_next (Next.js internals)
     * 3. /_static (inside /public)
     * 4. all root files inside /public (e.g. /favicon.ico)
     */
    "/((?!api/|_next/|_static/|_vercel|[\\w-]+\\.\\w+).*)",
    // Add /docs path to matcher
    "/docs",
  ],
};
