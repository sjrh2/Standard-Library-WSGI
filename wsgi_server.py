"""
Simple WSGI Server

This runs your WSGI web application using Python's built-in server.
"""

from wsgiref.simple_server import make_server
from simple_wsgi_app import application

def run_server(host='localhost', port=8000):
    """Run the WSGI server"""
    print(f"🚀 Starting WSGI server on http://{host}:{port}")
    print("📱 Open your browser and visit the URL above")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    # Create and start the WSGI server
    with make_server(host, port, application) as httpd:
        print(f"✅ Server running on port {port}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped!")

if __name__ == '__main__':
    run_server()
