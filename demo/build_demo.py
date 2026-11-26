"""Build the static GitHub Pages demo from templates/chat.html.

The web UI is rendered once with the example persona's name, and demo.js answers
the chat requests in the browser with canned replies. No model is called.

    python demo/build_demo.py   # writes site/index.html
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"

NOTE = """
    <div role="note" style="position:fixed;left:50%;bottom:12px;transform:translateX(-50%);z-index:50;
      max-width:calc(100vw - 24px);padding:7px 12px;border-radius:999px;background:rgba(28,25,22,.82);
      color:#f6f1e8;font:500 12px/1.3 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;text-align:center">
      Demo mode · canned sample replies, no model. Run it locally to train on a real chat.
    </div>
    <script src="demo.js"></script>
"""


def main() -> None:
    html = (ROOT / "templates" / "chat.html").read_text(encoding="utf-8")
    html = html.replace("{{ bot_name }}", "Momo")
    # demo.js must patch fetch before the page script runs, so load it in <head>.
    html = html.replace("<script src=\"demo.js\"></script>", "")
    icon = "<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💬</text></svg>\">"
    html = html.replace("</head>", f'    {icon}\n    <script src="demo.js"></script>\n</head>', 1)
    html = html.replace("</body>", NOTE.replace('    <script src="demo.js"></script>\n', "") + "</body>", 1)
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(html, encoding="utf-8")
    (OUT / "demo.js").write_text((ROOT / "demo" / "demo.js").read_text(encoding="utf-8"), encoding="utf-8")
    print(f"wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
