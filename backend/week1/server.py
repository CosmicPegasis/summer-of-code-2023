# webapp.py

from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
from routes import routes
import re
import sqlite3
from db_handler import LinksDatabaseHandler



class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))


    def do_GET(self):
        redirect_path = re.search("/redirect/(.*)", self.url.path)
        if redirect_path:
            try:
                path = LinksDatabaseHandler.read_link(redirect_path.group(1))
                self.send_response(302)
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Location", "http://{}".format(path))
                self.end_headers()
            except KeyError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("Not Found".encode("utf-8")))

            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("Not Found".encode("utf-8")))
                print("[ERROR]: Table not created")

    def do_POST(self):
        create_new_path = re.search("/create/(.*)/(.*)", self.url.path)
        if create_new_path:
            self.send_response(201)
            self.end_headers()
            LinksDatabaseHandler.create_link(create_new_path.group(1), create_new_path.group(2))

    def get_response(self):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    print("Server running at 8000")
    server.serve_forever()