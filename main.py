from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            file_path = "home/contacts.html"
            content_type = "text/html; charset=utf-8"
        else:
            file_path = self.path.lstrip("/")
            if file_path.endswith(".css"):
                content_type = "text/css"
            elif file_path.lower().endswith(".png"):
                content_type = "image/png"
            elif file_path.endswith(".js"):
                content_type = "application/javascript"
            else:
                content_type = "text/html"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h1>404 Not Found</h1>".encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):

        content_length = int(self.headers.get("Content-Length", 0))
        post_data_bytes = self.rfile.read(content_length)
        post_data_string = post_data_bytes.decode("utf-8")
        data = parse_qs(post_data_string)
        print(f"POST-запрос {data}")
        response = f"<p>Данные отправлены: {data}</p>".encode("utf-8")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
