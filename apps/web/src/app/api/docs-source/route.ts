import { NextRequest } from 'next/server'
import { promises as fs } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

export const runtime = 'nodejs'

async function resolveDocsRoot(): Promise<string> {
    const cwd = process.cwd()
    const candidate1 = path.join(cwd, 'src', 'app', 'docs')
    const candidate2 = path.join(cwd, 'apps', 'web', 'src', 'app', 'docs')
    try { await fs.stat(candidate1); return candidate1 } catch { }
    try { await fs.stat(candidate2); return candidate2 } catch { }
    // Fallback to candidate1; read will fail with 404 later
    return candidate1
}

export async function GET(req: NextRequest) {
    const url = new URL(req.url)
    const p = url.searchParams.get('p') || ''

    if (!p.startsWith('/docs/')) {
        return new Response('Bad request', { status: 400 })
    }

    const normalized = p.endsWith('/') && p !== '/' ? p.slice(0, -1) : p
    const relativeUnderDocs = normalized.replace(/^\/docs\//, '')

    // Candidate 1: relative to this route file (dev reliability)
    let routeDirDocs: string | null = null
    try {
        const routeFilePath = fileURLToPath(import.meta.url)
        const routeDir = path.dirname(routeFilePath)
        // ../../docs from .../app/api/docs-source -> .../app/docs
        routeDirDocs = path.resolve(routeDir, '../../docs')
    } catch {
        routeDirDocs = null
    }

    const candidates: string[] = []
    if (routeDirDocs) {
        candidates.push(path.join(routeDirDocs, relativeUnderDocs, 'page.mdx'))
    }
    const docsRoot = await resolveDocsRoot()
    candidates.push(path.join(docsRoot, relativeUnderDocs, 'page.mdx'))

    let foundPath: string | null = null
    for (const candidate of candidates) {
        try {
            const resolved = path.resolve(candidate)
            // Ensure final path stays under a known docs root if possible
            const rootForCheck = routeDirDocs && resolved.startsWith(routeDirDocs) ? routeDirDocs : docsRoot
            if (!resolved.startsWith(rootForCheck)) continue
            await fs.stat(resolved)
            foundPath = resolved
            break
        } catch { }
    }

    try {
        const targetPath = foundPath ?? path.join(docsRoot, relativeUnderDocs, 'page.mdx')
        const content = await fs.readFile(targetPath, 'utf8')
        return new Response(content, {
            status: 200,
            headers: {
                'content-type': 'text/plain; charset=utf-8',
                'cache-control': 'no-store'
            }
        })
    } catch {
        return new Response('Not found', { status: 404 })
    }
}


