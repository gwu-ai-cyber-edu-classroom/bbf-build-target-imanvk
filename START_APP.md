# START_APP.md — how to run and probe this app

> **Build team:** fill in every `<...>` below once your app runs. Other teams use this file to
> start your app and probe it during Break. Keep it accurate — a break is filed against the app a
> breaker can actually start from these instructions.

## What this app is

- **App:** a URL shortener service (menu #3)
- **Stack:** Python + Flask

## Start it

```bash
# 1. Install dependencies (in a virtualenv — see ENVIRONMENTS.md)
pip install -r requirements.txt

# 2. Run it
flask --app app run --port 8000
```

- **Base URL:** http://localhost:8000
- **Stop it:** Ctrl-C in the terminal running it.

## How to interact with it

- **Main endpoints / pages:**
  - `GET /` — homepage: a form to shorten a URL plus a list of public short links.
  - `POST /shorten` — create a short link for a URL (form field `url`); returns the new short link.
  - `GET /<code>` — follow a short code; redirects (HTTP 302) to its target URL.
  - `GET /api/links/<code>` — JSON metadata for a single short link.
- **Accounts / credentials for legitimate use:** none.
- **A benign request that should succeed:**

  ```bash
  # Create a short link
  curl -i -X POST http://localhost:8000/shorten --data-urlencode "url=https://example.com/"

  # Follow an existing short code (302 redirect to its target)
  curl -i http://localhost:8000/1
  ```

## For breakers

Attack this **running app over HTTP** — do **not** read this repo's source or `secret/` to find a
break. See [AGENTS_BREAK.md](AGENTS_BREAK.md) for the rules and your AI agent's instructions, and
[SPEC.md](SPEC.md) for the five properties (P1–P5) you are probing for.
