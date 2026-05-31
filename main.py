from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random, math
from datetime import datetime, timedelta

app = FastAPI(title="SysWatch — IT Monitoring Dashboard")
templates = Jinja2Templates(directory="templates")

random.seed(42)

SERVERS = [
    {"id": "WEB-01", "name": "Web Server",       "ip": "192.168.1.10", "role": "nginx"},
    {"id": "DB-01",  "name": "Database Server",   "ip": "192.168.1.11", "role": "mysql"},
    {"id": "API-01", "name": "API Gateway",        "ip": "192.168.1.12", "role": "fastapi"},
    {"id": "FS-01",  "name": "File Storage",       "ip": "192.168.1.13", "role": "samba"},
    {"id": "MAIL-01","name": "Mail Server",        "ip": "192.168.1.14", "role": "postfix"},
]

def gen_uptime():
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    data = {}
    for s in SERVERS:
        vals = []
        for i in range(12):
            base = 99.2 if s["role"] in ("nginx","mysql") else 98.5
            v = base - random.uniform(0, 1.5) + math.sin(i * 0.5) * 0.3
            vals.append(round(min(99.99, v), 2))
        data[s["id"]] = vals
    return {"months": months, "series": data}

def gen_tickets():
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    opened, resolved, escalated = [], [], []
    for i in range(12):
        o = random.randint(18, 42)
        r = random.randint(int(o * 0.75), o)
        e = random.randint(1, 4)
        opened.append(o); resolved.append(r); escalated.append(e)
    return {"months": months, "opened": opened, "resolved": resolved, "escalated": escalated}

def gen_network():
    labels, inbound, outbound = [], [], []
    base = datetime(2024, 3, 1)
    for i in range(30):
        d = base + timedelta(days=i)
        labels.append(d.strftime("%b %d"))
        hour_factor = 1 + 0.3 * math.sin(i * 0.4)
        inbound.append(round(random.uniform(120, 280) * hour_factor, 1))
        outbound.append(round(random.uniform(60, 160) * hour_factor, 1))
    return {"labels": labels, "inbound": inbound, "outbound": outbound}

def gen_alerts():
    cats = ["CPU Spike","Disk Usage","Memory","Network Timeout","Service Down","Auth Failure"]
    severities = ["low","medium","high","critical"]
    sev_weights = [0.4, 0.35, 0.18, 0.07]
    alerts = []
    base = datetime(2024, 2, 1)
    for i in range(40):
        sev = random.choices(severities, sev_weights)[0]
        dt = base + timedelta(days=random.randint(0, 58), hours=random.randint(0,23), minutes=random.randint(0,59))
        server = random.choice(SERVERS)
        alerts.append({
            "id": i + 1,
            "time": dt.strftime("%Y-%m-%d %H:%M"),
            "server": server["id"],
            "category": random.choice(cats),
            "severity": sev,
            "resolved": random.random() > 0.15
        })
    alerts.sort(key=lambda x: x["time"], reverse=True)
    return alerts[:20]

def gen_health():
    health = []
    for s in SERVERS:
        cpu = random.randint(12, 68)
        mem = random.randint(30, 78)
        disk = random.randint(25, 72)
        status = "online" if random.random() > 0.07 else "warning"
        health.append({**s, "cpu": cpu, "memory": mem, "disk": disk, "status": status,
                        "uptime_days": random.randint(40, 180)})
    return health


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/uptime")
def api_uptime():      return gen_uptime()

@app.get("/api/tickets")
def api_tickets():     return gen_tickets()

@app.get("/api/network")
def api_network():     return gen_network()

@app.get("/api/alerts")
def api_alerts():      return gen_alerts()

@app.get("/api/health")
def api_health():      return gen_health()

@app.get("/api/summary")
def api_summary():
    return {
        "total_servers": len(SERVERS),
        "online": 4, "warnings": 1, "offline": 0,
        "open_tickets": 9, "avg_uptime": 99.1,
        "alerts_today": 3, "resolved_today": 2
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
