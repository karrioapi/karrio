#!/usr/bin/env python3
"""
Local test server for Karrio embeddable elements.

Usage:
    python bin/elements-demo/serve.py [--port PORT]

Opens a browser at http://localhost:9876/test-embed.html where you can
fill in your API host/token and mount the rate sheet editor, devtools, template editor, or carrier connections iframe.
"""
import http.server
import os
import sys
import webbrowser

PORT = 9876

# Parse --port flag
for i, arg in enumerate(sys.argv):
    if arg == "--port" and i + 1 < len(sys.argv):
        PORT = int(sys.argv[i + 1])

# Serve from the repo root so relative paths to packages/elements/dist work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
os.chdir(ROOT)


class CORSHandler(http.server.SimpleHTTPRequestHandler):
    """Adds permissive CORS headers for local iframe testing."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def translate_path(self, path):
        """Route /test-embed.html to bin/elements-demo/test-embed.html, everything else from repo root."""
        if path == "/" or path == "/index.html":
            return os.path.join(SCRIPT_DIR, "test-embed.html")
        if path.startswith("/test-embed"):
            return os.path.join(SCRIPT_DIR, path.lstrip("/"))
        return super().translate_path(path)

    def log_message(self, format, *args):
        # Quieter logging – only show non-200 or interesting paths
        status = args[1] if len(args) > 1 else ""
        if str(status) != "200":
            super().log_message(format, *args)


def main():
    handler = CORSHandler
    with http.server.HTTPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}/test-embed.html"
        print(f"Karrio Elements test server")
        print(f"  Serving repo root: {ROOT}")
        print(f"  Test page:         {url}")
        print(f"  Press Ctrl+C to stop.\n")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
