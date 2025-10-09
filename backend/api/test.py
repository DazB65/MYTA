"""
MYTA Backend - Vercel Serverless Function
Basic HTTP handler that works reliably on Vercel
"""

from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Route handling
        if self.path == '/health':
            response = {
                "status": "healthy",
                "service": "MYTA Backend",
                "version": "1.0.0"
            }
        else:
            response = {
                "status": "ok",
                "message": "MYTA Backend is running on Vercel!",
                "note": "FastAPI integration coming soon - basic handler working",
                "path": self.path
            }

        self.wfile.write(json.dumps(response).encode())
        return

