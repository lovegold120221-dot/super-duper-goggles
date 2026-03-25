#!/usr/bin/env python3
"""
Simple API Proxy Server for Eburon Voice Core Frontend
Routes frontend API calls to appropriate backend services
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import json
from urllib.error import URLError, HTTPError

class APIProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            # Serve the working dashboard by default
            if self.path == '/':
                self.path = '/working_dashboard.html'
                try:
                    super().do_GET()
                except:
                    # Fallback to index.html if working_dashboard doesn't exist
                    self.path = '/index.html'
                    super().do_GET()
            else:
                super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_error(404, "Not Found")
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def handle_api_request(self):
        """Proxy API requests to backend services"""
        try:
            # Map API paths to backend services
            backend_url = self.map_api_to_backend(self.path)
            if not backend_url:
                self.send_error(404, f"API endpoint not found: {self.path}")
                return
            
            print(f"Proxying {self.command} {self.path} -> {backend_url}")
            
            # Prepare request
            if self.command == 'POST':
                # Read POST data
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length) if content_length > 0 else None
                
                # Create request with headers
                req = urllib.request.Request(backend_url, post_data)
                for header, value in self.headers.items():
                    if header.lower() not in ['host', 'content-length']:
                        req.add_header(header, value)
            else:
                req = urllib.request.Request(backend_url)
                for header, value in self.headers.items():
                    if header.lower() not in ['host']:
                        req.add_header(header, value)
            
            # Make request to backend
            try:
                response = urllib.request.urlopen(req, timeout=10)
            except HTTPError as e:
                self.send_response(e.code)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_msg = {"error": f"Backend error: {e.code} {e.reason}"}
                self.wfile.write(json.dumps(error_msg).encode())
                return
            except URLError as e:
                self.send_response(503)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_msg = {"error": f"Backend unavailable: {str(e)}"}
                self.wfile.write(json.dumps(error_msg).encode())
                return
            
            # Forward response back to client
            self.send_response(response.getcode())
            for header, value in response.headers.items():
                if header.lower() not in ['server', 'date', 'connection', 'transfer-encoding']:
                    self.send_header(header, value)
            
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            
            content_type = response.headers.get('Content-Type', 'application/json')
            self.send_header('Content-Type', content_type)
            self.end_headers()
            
            # Stream response
            data = response.read()
            self.wfile.write(data)
            
        except Exception as e:
            print(f"Proxy error: {e}")
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_msg = {"error": f"Proxy error: {str(e)}"}
            self.wfile.write(json.dumps(error_msg).encode())
    
    def map_api_to_backend(self, path):
        """Map frontend API paths to backend service URLs"""
        # SIP Gateway APIs
        if path.startswith('/api/sip/status'):
            return 'http://localhost:5060/api/status'
        elif path.startswith('/api/sip/call'):
            return 'http://localhost:5060/api/call'
        
        # TTS Server APIs  
        elif path.startswith('/api/tts/tts'):
            return 'http://localhost:8002/api/tts'
        elif path.startswith('/api/tts/health'):
            return 'http://localhost:8002/health'
        
        # Ollama LLM APIs
        elif path.startswith('/api/ollama/tags'):
            return 'http://localhost:11434/api/tags'
        elif path.startswith('/api/ollama/generate'):
            return 'http://localhost:11434/api/generate'
        
        # Unknown API path
        else:
            return None
    
    def log_message(self, format, *args):
        """Custom log messages"""
        print(f"[{self.address_string()}] {format % args}")

def main():
    PORT = 3004
    print(f"🚀 Starting Eburon Voice API Proxy Server")
    print(f"📡 Frontend: http://localhost:{PORT}")
    print(f"🔗 Backend APIs:")
    print(f"   - SIP Gateway: http://localhost:5060")
    print(f"   - TTS Server:  http://localhost:8002") 
    print(f"   - Ollama LLM:   http://localhost:11434")
    print(f"✨ Ready to serve!")
    
    with socketserver.TCPServer(('', PORT), APIProxyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
            httpd.shutdown()

if __name__ == '__main__':
    main()
