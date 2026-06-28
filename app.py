from __future__ import annotations

import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

from src.filter import classify


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Vietnamese AI Safety Filter</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 16px; }}
    textarea {{ width: 100%; min-height: 110px; font: inherit; padding: 12px; }}
    button {{ margin-top: 12px; padding: 10px 14px; font: inherit; }}
    pre {{ background: #f4f4f4; padding: 14px; white-space: pre-wrap; }}
  </style>
</head>
<body>
  <h1>Vietnamese AI Safety Filter</h1>
  <form method="post">
    <textarea name="text" placeholder="Nhap prompt tieng Viet de kiem tra...">{text}</textarea>
    <br>
    <button>Classify</button>
  </form>
  {result}
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self._send(PAGE.format(text="", result=""))

    def do_POST(self) -> None:
        length = int(self.headers.get("content-length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        text = parse_qs(body).get("text", [""])[0]
        decision = classify(text).to_dict()
        result = "<h2>Decision</h2><pre>{}</pre>".format(
            html.escape(json.dumps(decision, ensure_ascii=False, indent=2))
        )
        self._send(PAGE.format(text=html.escape(text), result=result))

    def _send(self, content: str) -> None:
        data = content.encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("open http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
