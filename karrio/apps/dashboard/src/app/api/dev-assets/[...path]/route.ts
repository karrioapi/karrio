import { NextRequest, NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';

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

        // Try to find the asset in different locations
        let fullAssetPath: string | null = null;

        // 1. Try in the assets/ subdirectory first
        const assetsSubdirPath = join(appBasePath, 'assets', assetFilePath);
        if (existsSync(assetsSubdirPath)) {
            fullAssetPath = assetsSubdirPath;
        }

        // 2. If not found in assets/, try at the app root level (for README.md, etc.)
        if (!fullAssetPath) {
            const rootLevelPath = join(appBasePath, assetFilePath);
            if (existsSync(rootLevelPath)) {
                fullAssetPath = rootLevelPath;
            }
        }

        // If still not found, return 404
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
