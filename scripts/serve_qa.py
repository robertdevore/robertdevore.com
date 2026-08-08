#!/usr/bin/env python3
"""Serve generated static output with the site's generated 404 document."""

from __future__ import annotations

import argparse
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


class StaticSiteHandler(SimpleHTTPRequestHandler):
    """Use output/404.html for paths with no static-file counterpart."""

    def __init__(self, *args, directory: str, **kwargs) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self) -> None:  # noqa: N802 (stdlib handler contract)
        requested = unquote(urlsplit(self.path).path).lstrip("/")
        root = Path(self.directory).resolve()
        candidate = (root / requested).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            candidate = root / "__outside-static-root__"
        if candidate.is_dir():
            candidate /= "index.html"
        if candidate.exists():
            super().do_GET()
            return

        not_found = Path(self.directory, "404.html")
        if not not_found.is_file():
            self.send_error(404, "Generated 404 document is missing")
            return

        payload = not_found.read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", default="output", help="Generated static-site directory.")
    parser.add_argument("--host", default="127.0.0.1", help="Loopback host to bind.")
    parser.add_argument("--port", default=4173, type=int, help="TCP port to bind.")
    args = parser.parse_args()

    directory = Path(args.directory).resolve()
    if not directory.is_dir():
        parser.error(f"static-site directory does not exist: {directory}")

    handler = lambda *a, **kw: StaticSiteHandler(*a, directory=os.fspath(directory), **kw)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving {directory} at http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
