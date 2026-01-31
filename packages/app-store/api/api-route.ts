import { NextRequest, NextResponse } from 'next/server';
import { join } from 'path';

// Cache for loaded route handlers to avoid repeated imports
const routeCache = new Map<string, any>();

async function loadAppRoute(appId: string, apiPath: string) {
  const cacheKey = `${appId}:${apiPath}`;

  if (routeCache.has(cacheKey)) {
    return routeCache.get(cacheKey);
  }

  // Add debug logging
  console.log(`Loading app route: ${appId}/${apiPath}`);

  try {
    // Use webpackIgnore to prevent bundler static analysis of dynamic paths.
    // These imports are resolved at runtime on the server.
    const packagePath = `@karrio/app-store/apps/${appId}/api/${apiPath}/route`;
    const routeModule = await import(/* webpackIgnore: true */ packagePath);
    routeCache.set(cacheKey, routeModule);
    return routeModule;
  } catch (error) {
    try {
      // Fallback to direct file system path
      const directPath = join(process.cwd(), 'packages', 'app-store', 'apps', appId, 'api', apiPath, 'route.ts');
      const routeModule = await import(/* webpackIgnore: true */ directPath);
      routeCache.set(cacheKey, routeModule);
      return routeModule;
    } catch (directError) {
      console.error(`Failed to load app route ${appId}/${apiPath}:`, { error, directError });
      throw new Error(`Route not found: ${appId}/${apiPath}`);
    }
  }
}

async function handleRequest(
  request: NextRequest,
  method: string,
  params: { appId: string; paths: string[] }
) {
  try {
    const { appId, paths } = params;
    const apiPath = paths.join('/');

    // Load the app route module
    const routeModule = await loadAppRoute(appId, apiPath);

    if (!routeModule || typeof routeModule[method] !== 'function') {
      return new NextResponse(`Method ${method} not allowed`, { status: 405 });
    }

    // For private endpoints, add authentication logic here if needed
    // For now, just call the route handler directly
    return await routeModule[method](request, { params: Promise.resolve(params) });

  } catch (error) {
    console.error('App API route error:', error);

    if (error instanceof Error && error.message.includes('Route not found')) {
      return new NextResponse('Not Found', { status: 404 });
    }

    return new NextResponse('Internal Server Error', { status: 500 });
  }
}

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ appId: string; paths: string[] }> }
) {
  return handleRequest(request, 'GET', await params);
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ appId: string; paths: string[] }> }
) {
  return handleRequest(request, 'POST', await params);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ appId: string; paths: string[] }> }
) {
  return handleRequest(request, 'PUT', await params);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ appId: string; paths: string[] }> }
) {
  return handleRequest(request, 'DELETE', await params);
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ appId: string; paths: string[] }> }
) {
  return handleRequest(request, 'PATCH', await params);
}
