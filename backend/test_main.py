"""
Ultra minimal test for Vercel deployment
"""

def app(environ, start_response):
    """WSGI application"""
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)
    return [b'{"status": "working", "message": "Ultra minimal backend is running!"}']
