import { createServer } from 'node:http'
import { readFile } from 'node:fs/promises'
import { join, extname } from 'node:path'
import { fileURLToPath } from 'node:url'
import server from './dist/server/server.js'

const __dirname = fileURLToPath(new URL('.', import.meta.url))
const clientDir = join(__dirname, 'dist', 'client')

const port = parseInt(process.env.PORT || process.env.DASHBOARD_PORT || '3102')
const host = process.env.HOST || '0.0.0.0'

console.log(`Starting TanStack Start server on ${host}:${port}`)
console.log(`Serving static assets from: ${clientDir}`)

const mimeTypes = {
  '.js': 'application/javascript',
  '.mjs': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.webp': 'image/webp',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.eot': 'font/eot',
}

async function serveStatic(pathname) {
  try {
    // Remove leading slash and resolve path
    const filePath = join(clientDir, pathname.slice(1))
    const content = await readFile(filePath)
    const ext = extname(filePath)
    const contentType = mimeTypes[ext] || 'application/octet-stream'

    return new Response(content, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Cache-Control': 'public, max-age=31536000, immutable',
      },
    })
  } catch (error) {
    return null
  }
}

const httpServer = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host}`)

    // Try to serve static assets first
    if (url.pathname.startsWith('/assets/') ||
        url.pathname.startsWith('/carriers/') ||
        url.pathname.match(/\.(js|css|png|jpg|jpeg|gif|svg|ico|webp|woff|woff2|ttf|eot|json)$/)) {
      const staticResponse = await serveStatic(url.pathname)
      if (staticResponse) {
        res.statusCode = staticResponse.status
        staticResponse.headers.forEach((value, key) => {
          res.setHeader(key, value)
        })
        const arrayBuffer = await staticResponse.arrayBuffer()
        res.end(Buffer.from(arrayBuffer))
        return
      }
    }

    // Fall back to TanStack Start server for SSR
    const request = new Request(url, {
      method: req.method,
      headers: req.headers,
      body: req.method !== 'GET' && req.method !== 'HEAD' ? req : undefined,
    })

    const response = await server.fetch(request)

    res.statusCode = response.status
    response.headers.forEach((value, key) => {
      res.setHeader(key, value)
    })

    if (response.body) {
      const reader = response.body.getReader()
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        res.write(value)
      }
    }
    res.end()
  } catch (error) {
    console.error('Server error:', error)
    res.statusCode = 500
    res.end('Internal Server Error')
  }
})

httpServer.listen(port, host, () => {
  console.log(`Server running at http://${host}:${port}`)
})
