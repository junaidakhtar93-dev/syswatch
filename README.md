# SysWatch — IT Monitoring Dashboard

A demo IT-monitoring dashboard built with **FastAPI** and **Plotly.js**. It visualises server health, uptime trends, ticket flow, network throughput, and a recent-alerts feed across a small fleet of servers.

> Originally built during my tenure as System Support Officer at Mid-Chain Technologies (2024–2026); this is a cleaned-up version with mock data for public sharing.

> **Note:** This is a self-contained demo. The metrics are deterministically generated mock data (`random.seed(42)`), not a live feed — there's no database or real agent. It exists to showcase the dashboard UI and the FastAPI + Plotly data-flow.

## Features

- Server health cards (CPU / memory / disk / status / uptime)
- Uptime trend per server (12 months)
- Ticket flow — opened vs resolved vs escalated
- Network throughput — inbound / outbound over 30 days
- Recent alerts feed with severity levels

## API

| Endpoint        | Returns                                  |
| --------------- | ---------------------------------------- |
| `GET /`         | The dashboard (HTML)                     |
| `GET /api/summary` | Top-line counts                       |
| `GET /api/health`  | Per-server health snapshot            |
| `GET /api/uptime`  | Monthly uptime series                 |
| `GET /api/tickets` | Monthly ticket counts                 |
| `GET /api/network` | Daily network throughput              |
| `GET /api/alerts`  | Recent alerts                         |

## Run locally

```bash
# Isolates project dependencies from the system Python.
python3 -m venv .venv && source .venv/bin/activate

# Installs FastAPI, Uvicorn, and Jinja2 (pinned in requirements.txt).
pip install -r requirements.txt

# Starts the dev server with auto-reload at http://localhost:8000
uvicorn main:app --reload
```

Then open <http://localhost:8000>.

## Structure

- `main.py` — FastAPI app, mock-data generators, and JSON API
- `templates/index.html` — dashboard UI (Plotly charts, fetches the `/api/*` endpoints)
- `requirements.txt` — pinned dependencies

## Tech

Python 3.10+ · FastAPI · Uvicorn · Jinja2 · Plotly.js (CDN)

## License

[MIT](LICENSE) © Junaid Akhtar
