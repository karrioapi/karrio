import { createServer } from 'node:http'
import server from './dist/server/server.js'

const port = parseInt(process.env.PORT || process.env.DASHBOARD_PORT || '3102')
const host = process.env.HOST || '0.0.0.0'

console.log(`Starting TanStack Start server on ${host}:${port}`)

const httpServer = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host}`)

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
