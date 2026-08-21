#!/usr/bin/env python3
"""Tiny static file server for the local build (chdir before anything
that touches the inherited working directory)."""
import functools, os, sys

# Serves this folder by default; pass a directory to serve something else
# (e.g. `python3 decathlon-sale/serve.py 4321 .` for the whole portfolio).
ROOT = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4321

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        SimpleHTTPRequestHandler.end_headers(self)
    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

httpd = ThreadingHTTPServer(("127.0.0.1", PORT), functools.partial(Handler, directory=ROOT))
print("serving %s at http://localhost:%d/" % (ROOT, PORT), flush=True)
httpd.serve_forever()
