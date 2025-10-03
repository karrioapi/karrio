import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

export async function middleware(req: NextRequest) {
  const { pathname, search, href } = req.nextUrl;
  const hostname = req.headers.get("host") as string;
  const requestHeaders = new Headers(req.headers);
  requestHeaders.set("x-pathname", pathname);
  requestHeaders.set("x-search", search);
  requestHeaders.set("x-href", href);

  if (pathname.startsWith("/api")) {
    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    });
  }

  // rewrite everything else to `/[domain]/[slug] dynamic route
  return NextResponse.rewrite(
    new URL(`/${hostname}${pathname}${search}`, req.url),
    {
      request: {
        headers: requestHeaders,
      },
    },
  );
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
  ],
};
