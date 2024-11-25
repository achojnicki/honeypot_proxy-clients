from honeypot_proxy_client import honeypot_proxy_client

import http.server
import socketserver


proxy=honeypot_proxy_client()

# Define the handler for the proxy
class SimpleHTTPProxy(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract the URL from the request
        target_url = self.path
        
        print(f"Proxying GET request to: {target_url}")
        
        # Make a request to the target server
        response = proxy.get(target_url)

        # Forward the response back to the client
        self.send_response(200)
        #for header, value in response.headers.items():
        #    self.send_header(header, value)

        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
        


# Run the proxy server
def run_proxy_server(port=1234):
    with socketserver.ThreadingTCPServer(('', port), SimpleHTTPProxy) as httpd:
        print(f"Serving HTTP proxy on port {port}...")
        httpd.serve_forever()

if __name__ == "__main__":
    run_proxy_server()