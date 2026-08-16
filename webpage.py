import os
import sys
import time
import datetime
import fastapi
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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
    
    <!-- 2. Added a dynamic title tag to resolve the missing title error -->
    <title>{title_text} - Flight Tracker</title>
    
    <link href="/static/output.css?v={timestamp}" rel="stylesheet">
</head>
<body class=" p-8 font-sans">
    
    <!-- Top Navigation Bar Container -->
    <div class="relative flex items-center justify-center min-h-[64px] mb-8">

        <button type="button" onclick="location.href='/'" class="absolute left-0 p-2 hover:bg-slate-800 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
            <img class="w-8 h-8 object-scale-down" src="/static/images/airplane-svgrepo-com.svg" alt="Home Dashboard">
        </button>

        <button type="button" onclick="location.href='/statistics'" class="absolute left-14 p-2 hover:bg-slate-800 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
             <img class="w-8 h-8 object-scale-down" src="/static/images/statistics-svgrepo-com.svg" alt="Statistics View">
        </button>

        <h1 class="text-3xl font-bold tracking-wide">{title_text}</h1>

        <button type="button" onclick="location.href='/settings'" class="absolute right-0 p-2 hover:bg-slate-800 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
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
        <tr class="hover:bg-slate-300 transition-colors border-b border-slate-500">
            <td>{flight}</td>
            <td>{aircraft}</td>
            <td>{speed} kt</td>
            <td>{altitude} ft</td>
            <td class="p-4 text-indigo-500 hover:text-indigo-400">
                <a href="/aircraft/{a.get('hex')}" class="underline">View Details</a>
            </td>
        </tr>
        """

    if not aircraft_data["aircraft"]:
        rows_html = """
        <tr>
            <td colspan="5" class="p-4 text-center-left ">
                No active aircraft tracked at this moment.
            </td>
        </tr>
        """

    table_content = f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title_text} - Flight Tracker</title>
        <link href="/static/output.css?v={timestamp}" rel="stylesheet">
        <script>
        async function updateDashboard() {{
            try {{
                const response = await fetch('/api/dashboard-stats');
                const data = await response.json();
                
                document.getElementById('stats-container').innerText = `Active Planes: ${{data.active_planes}}`;
            }} catch (error) {{
                console.error("Failed to fetch dashboard updates:", error);
            }}
        }}

        updateDashboard();
        setInterval(updateDashboard, 5000);
        </script>
    </head>


    <div class="overflow-x-auto rounded-xl border border-slate-700 bg-slate-800/50 shadow-md">
        <table class="w-full text-left border-collapse">
            <thead class="bg-slate-700 text-gray-300">
                <tr>
                    <th class="p-4 font-semibold">Flight Number</th>
                    <th class="p-4 font-semibold">Aircraft</th>
                    <th class="p-4 font-semibold">Speed</th>
                    <th class="p-4 font-semibold">Altitude</th>
                    <th class="p-4 font-semibold">More Info</th>
                </tr>
            </thead>
            <tbody>
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
    settings_content = """
    
    """
    return generate_page_layout(title_text="Settings", content_html=settings_content)


@app.get("/statistics", response_class=HTMLResponse)
def read_statistics():
    statistics_content = """
    <div">
    
    </div>
    """
    return generate_page_layout(
        title_text="Statistics", content_html=statistics_content
    )

@app.get("/api/dashboard-stats")
def get_stats():
    url = "http://192.168.1.103/tar1090/data/aircraft.json"
    try:
        response = requests.get(url, timeout=1)
        aircraft_data = response.json()
        status = "nominal" if response.status_code == 200 else "error"
    
    except Exception:
        aircraft_data = {"aircraft": []}
        status = "error"
    
    return {
        "active_planes": len(aircraft_data["aircraft"]),
        "status": status
    }
