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
    // Try package alias import first
    const packagePath = `@karrio/app-store/apps/${appId}/api/${apiPath}/route`;
    console.log(`Trying package import: ${packagePath}`);
    const routeModule = await import(packagePath);
    console.log(`Successfully loaded package import: ${packagePath}`);
    routeCache.set(cacheKey, routeModule);
    return routeModule;
  } catch (error) {
    console.log(`Package import failed: ${error.message}`);
    try {
      // Fallback to relative import (8 levels up from dashboard route to workspace root)
      const relativePath = `../../../../../../../../packages/app-store/apps/${appId}/api/${apiPath}/route`;
      console.log(`Trying relative import: ${relativePath}`);
      const routeModule = await import(relativePath);
      console.log(`Successfully loaded relative import: ${relativePath}`);
      routeCache.set(cacheKey, routeModule);
      return routeModule;
    } catch (fallbackError) {
      console.log(`Relative import failed: ${fallbackError.message}`);

      // Try one more approach - direct file system path
      try {
        const directPath = join(process.cwd(), 'packages', 'app-store', 'apps', appId, 'api', apiPath, 'route.ts');
        console.log(`Trying direct file path: ${directPath}`);
        const routeModule = await import(directPath);
        console.log(`Successfully loaded direct import: ${directPath}`);
        routeCache.set(cacheKey, routeModule);
        return routeModule;
      } catch (directError) {
        console.log(`Direct import failed: ${directError.message}`);
        console.error(`Failed to load app route ${appId}/${apiPath}:`, { error, fallbackError, directError });
        throw new Error(`Route not found: ${appId}/${apiPath}`);
      }
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
