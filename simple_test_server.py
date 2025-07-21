#!/usr/bin/env python3
"""
Simple HTTP server to test connectivity
"""
import http.server
import socketserver
import threading
import time

PORT = 8890

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Test server is working!</h1></body></html>')

def start_server():
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"Server running on http://localhost:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server failed: {e}")

if __name__ == "__main__":
    start_server()