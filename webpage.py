import os
import sys
import time
import datetime
import fastapi
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Response

app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def generate_page_layout(title_text: str, content_html: str = "") -> str:
    """Generates a consistent layout wrapper with navigation buttons and content."""
    timestamp = int(time.time())
    return f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Flight Tracker</title>
    <link href="/static/output.css?v={timestamp}" rel="stylesheet">
    
    <!-- Using a robust native JavaScript reloader function to bypass firewalls -->
    <script>
    async function refreshFlightTable() {{
        try {{
            const res = await fetch('/api/dashboard-table');
            if (res.ok) {{
                const freshRows = await res.text();
                const tbody = document.getElementById('flight-rows');
                if (tbody) {{
                    tbody.innerHTML = freshRows;
                }}
            }}
        }} catch (err) {{
            console.error("Auto-refresh connection failed:", err);
        }}
    }}
    
    // Fire the automatic update interval worker once every 5000ms (5 seconds)
    setInterval(refreshFlightTable, 5000);
    </script>
</head>
<body class="p-8 font-sans bg-cyan-950 text-white">
    
    <!-- Top Navigation Bar Container -->
    <div class="relative flex items-center justify-center min-h-[64px] mb-8">
        <button type="button" onclick="location.href='/'" class="absolute left-0 p-2 hover:bg-cyan-900 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
            <img class="w-8 h-8 object-scale-down" src="/static/images/airplane-svgrepo-com.svg" alt="Home Dashboard">
        </button>

        <button type="button" onclick="location.href='/statistics'" class="absolute left-14 p-2 hover:bg-cyan-900 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
             <img class="w-8 h-8 object-scale-down" src="/static/images/statistics-svgrepo-com.svg" alt="Statistics View">
        </button>

        <h1 class="text-3xl font-bold tracking-wide">{title_text}</h1>

        <button type="button" onclick="location.href='/settings'" class="absolute right-0 p-2 hover:bg-cyan-900 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
            <img class="w-6 h-6 object-scale-down" src="/static/images/settings-svgrepo-com.svg" alt="Settings Configuration">
        </button>
    </div>

    <!-- Main Body Content Grid Wrapper -->
    <main class="max-w-7xl mx-auto">
        {content_html}
    </main>

</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def read_root():
    url = "http://192.168.1.103/tar1090/data/aircraft.json"
    try:
        response = requests.get(url, timeout=1)
        aircraft_data = response.json()
    except Exception:
        aircraft_data = {"aircraft": []}

    rows_html = ""
    for a in aircraft_data["aircraft"]:
        flight = a.get("flight", "-").strip()
        aircraft = a.get("t", a.get("hex", "-"))
        speed = a.get("gs", "-")
        altitude = a.get("alt_baro", "-")

        rows_html += f"""
        <tr class="hover:bg-cyan-950/50 transition-colors border-b border-cyan-950/50">
            <td class="p-4">{flight}</td>
            <td class="p-4">{aircraft}</td>
            <td class="p-4">{speed} kt</td>
            <td class="p-4">{altitude} ft</td>
            <td class="p-4 text-indigo-400 hover:text-indigo-300">
                <a href="/aircraft/{a.get('hex')}" class="underline">View Details</a>
            </td>
        </tr>
        """

    if not aircraft_data["aircraft"]:
        rows_html = """
        <tr>
            <td colspan="5" class="p-4 text-center text-cyan-400">
                No active aircraft tracked at this moment.
            </td>
        </tr>
        """

    # Added the id="flight-rows" marker so our script knows where to insert the table items
    table_content = f"""
    <div class="overflow-x-auto rounded-xl border border-cyan-950 bg-cyan-900/50 shadow-md">
        <table class="w-full text-left border-collapse">
            <thead class="bg-cyan-950 text-gray-300">
                <tr>
                    <th class="p-4 font-semibold">Flight Number</th>
                    <th class="p-4 font-semibold">Aircraft</th>
                    <th class="p-4 font-semibold">Speed</th>
                    <th class="p-4 font-semibold">Altitude</th>
                    <th class="p-4 font-semibold">More Info</th>
                </tr>
            </thead>
            <tbody id="flight-rows">
                {rows_html}
            </tbody>
        </table>
    </div>
    """

    return generate_page_layout(
        title_text="Aircraft Dashboard", content_html=table_content
    )


@app.get("/settings", response_class=HTMLResponse)
def read_settings():
    settings_content = """<div class="text-cyan-400">Settings panel configuration context.</div>"""
    return generate_page_layout(title_text="Settings", content_html=settings_content)


@app.get("/statistics", response_class=HTMLResponse)
def read_statistics():
    statistics_content = """<div class="text-cyan-400">Statistics data dashboard logs.</div>"""
    return generate_page_layout(title_text="Statistics", content_html=statistics_content)


@app.get("/api/dashboard-table")
def get_dashboard_table(response: Response):
    # Enforce anti-caching response headers strictly
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    url = "http://192.168.1.103/tar1090/data/aircraft.json"
    try:
        api_response = requests.get(url, timeout=1)
        aircraft_data = api_response.json()
    except Exception:
        aircraft_data = {"aircraft": []}

    rows_html = ""
    for a in aircraft_data["aircraft"]:
        flight = a.get("flight", "-").strip()
        aircraft = a.get("t", a.get("hex", "-"))
        speed = a.get("gs", "-")
        altitude = a.get("alt_baro", "-")

        rows_html += f"""
        <tr class="hover:bg-cyan-950/50 transition-colors border-b border-cyan-950">
            <td class="p-4">{flight}</td>
            <td class="p-4">{aircraft}</td>
            <td class="p-4">{speed} kt</td>
            <td class="p-4">{altitude} ft</td>
            <td class="p-4 text-indigo-400 hover:text-indigo-300">
                <a href="/aircraft/{a.get('hex')}" class="underline">View Details</a>
            </td>
        </tr>
        """

    if not aircraft_data["aircraft"]:
        rows_html = """
        <tr>
            <td colspan="5" class="p-4 text-center text-cyan-400">
                No active aircraft tracked at this moment.
            </td>
        </tr>
        """
        
    return HTMLResponse(content=rows_html)
