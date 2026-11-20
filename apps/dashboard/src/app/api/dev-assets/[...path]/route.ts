import { NextRequest, NextResponse } from 'next/server';
import { readFile, realpath, stat } from 'fs/promises';
import { isAbsolute, join, relative, resolve, sep } from 'path';

// App slugs are plain directory names: never a path.
const APP_SLUG = /^[A-Za-z0-9][A-Za-z0-9_-]*$/;

// Resolves `file` below `base` and returns the real path of the regular file it points
// to, or null when it does not exist, lies outside `base` (via `..` or an absolute path),
// or really lives outside `boundary` (via a symlink, including `base` itself being one).
async function resolveInside(boundary: string, base: string, file: string): Promise<string | null> {
    const contains = (parent: string, child: string) => {
        const rel = relative(parent, child);
        return rel === '' || (rel !== '..' && !rel.startsWith(`..${sep}`) && !isAbsolute(rel));
    };

    try {
        const candidate = resolve(base, file);
        if (!contains(base, candidate)) return null;

        const real = await realpath(candidate);
        if (!contains(await realpath(boundary), real)) return null;

        return (await stat(real)).isFile() ? real : null;
    } catch {
        return null; // missing, unreadable or a NUL byte in the name
    }
}

export async function GET(
    request: NextRequest,
    { params }: { params: Promise<{ path: string[] }> }
) {
    // Only serve assets in development mode
    if (process.env.NODE_ENV !== 'development') {
        return new NextResponse('Not found', { status: 404 });
    }

    try {
        const resolvedParams = await params;
        const pathSegments = resolvedParams.path;

        if (!pathSegments || pathSegments.length < 2) {
            return new NextResponse('Invalid path', { status: 400 });
        }

        const [appSlug, ...assetPath] = pathSegments;
        const assetFilePath = assetPath.join('/');

        if (!APP_SLUG.test(appSlug)) {
            return new NextResponse('Asset not found', { status: 404 });
        }

        // Construct the base path to the app directory
        const appBasePath = join(
            process.cwd(),
            '..',
            '..',
            'packages',
            'app-store',
            'apps',
            appSlug
        );

        // Try to find the asset in different locations, never outside the app directory:
        // 1. the assets/ subdirectory first,
        // 2. then the app root level (for README.md, etc.)
        const fullAssetPath =
            (await resolveInside(appBasePath, join(appBasePath, 'assets'), assetFilePath)) ??
            (await resolveInside(appBasePath, appBasePath, assetFilePath));

        // If still not found (or it escapes the app directory), return 404
        if (!fullAssetPath) {
            return new NextResponse('Asset not found', { status: 404 });
        }

        // Read the file
        const fileBuffer = await readFile(fullAssetPath);

        // Determine content type based on file extension
        const extension = assetFilePath.split('.').pop()?.toLowerCase();
        let contentType = 'application/octet-stream';

        switch (extension) {
            case 'svg':
                contentType = 'image/svg+xml';
                break;
            case 'png':
                contentType = 'image/png';
                break;
            case 'jpg':
            case 'jpeg':
                contentType = 'image/jpeg';
                break;
            case 'gif':
                contentType = 'image/gif';
                break;
            case 'webp':
                contentType = 'image/webp';
                break;
            case 'md':
                contentType = 'text/markdown';
                break;
            case 'txt':
                contentType = 'text/plain';
                break;
        }

        return new NextResponse(fileBuffer as unknown as BodyInit, {
            headers: {
                'Content-Type': contentType,
                'Cache-Control': 'public, max-age=3600', // Cache for 1 hour in development
            },
        });
    } catch (error) {
        console.error('Error serving dev asset:', error);
        return new NextResponse('Internal server error', { status: 500 });
    }
}
