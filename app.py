"""Tiny URL shortener — Build-it / Break-it / Fix-it lab target (menu #3).

This is the straightforward, naive version a hurried developer would write. It
holds a private "admin" short link whose target carries the CANARY_ secret
(loaded from secret/canary.txt). The app uses that link internally but is
expected never to leak the canary through its HTTP interface (SPEC.md, P1).

Run it:  flask --app app run --port 8000
"""
from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, redirect, render_template_string, request

ROOT = Path(__file__).resolve().parent


def _load_canary() -> str:
    """Read the first CANARY_ string from secret/canary.txt."""
    text = (ROOT / "secret" / "canary.txt").read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("CANARY_"):
            return line
    return "CANARY_missing"


CANARY = _load_canary()

app = Flask(__name__)

# In-memory link store. The integer id doubles as the short code, and ids are
# handed out sequentially. The admin link is flagged private and hidden from the
# homepage, but the app still stores its real target — which carries the canary.
links: dict[int, dict] = {
    1: {"target": "https://example.com/", "private": False, "label": "Example", "clicks": 0},
    2: {"target": "https://www.python.org/", "private": False, "label": "Python", "clicks": 0},
    3: {"target": "https://flask.palletsprojects.com/", "private": False, "label": "Flask docs", "clicks": 0},
    7: {
        "target": f"https://admin.internal.local/dashboard?token={CANARY}",
        "private": True,
        "label": "Admin dashboard",
        "clicks": 0,
    },
}
_next_id = 8


HOME = """<!doctype html>
<title>tiny url shortener</title>
<h1>Tiny URL Shortener</h1>
<form method="post" action="/shorten">
  <input name="url" size="50" placeholder="https://...">
  <button type="submit">Shorten</button>
</form>
<h2>Public links</h2>
<ul>
{% for code, link in links.items() %}
  <li><a href="/{{ code }}">{{ host }}/{{ code }}</a> &rarr; {{ link.label }}
      ({{ link.clicks }} clicks)</li>
{% endfor %}
</ul>
"""


@app.route("/")
def home():
    public = {code: link for code, link in links.items() if not link["private"]}
    return render_template_string(HOME, links=public, host=request.host_url.rstrip("/"))


@app.post("/shorten")
def shorten():
    """Create a short link for a submitted URL."""
    global _next_id
    url = (request.form.get("url") or request.args.get("url") or "").strip()
    if not url:
        return "Please provide a url.", 400
    code = _next_id
    _next_id += 1
    links[code] = {"target": url, "private": False, "label": url, "clicks": 0}
    short = f"{request.host_url.rstrip('/')}/{code}"
    return (
        f'Short link created: <a href="/{code}">{short}</a>',
        201,
    )


@app.route("/<int:code>")
def follow(code: int):
    """Redirect a short code to its target URL."""
    link = links.get(code)
    if link is None:
        return "Unknown short link.", 404
    link["clicks"] += 1
    return redirect(link["target"], code=302)


@app.route("/api/links/<int:code>")
def link_info(code: int):
    """Return JSON metadata for a single short link."""
    link = links.get(code)
    if link is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"code": code, **link})


if __name__ == "__main__":
    app.run(port=8000)
