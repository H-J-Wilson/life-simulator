import html
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
URL = "http://192.168.1.103/tar1090/data/aircraft.json"


def generate_page_layout(title_text: str, content_html: str = "") -> str:
    """Generates a consistent layout wrapper with navigation buttons, content, and footer."""
    timestamp = int(time.time())
    return f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Flight Tracker</title>
    <link href="/static/output.css?v={timestamp}" rel="stylesheet">
    

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
<body>
    
    <div class="p-8 font-sans bg-cyan-950 text-white min-h-screen flex flex-col justify-between">

        <div class="relative flex items-center justify-center min-h-[64px] mb-8">
            <button type="button" onclick="location.href='/'" class="absolute left-0 p-2 hover:bg-cyan-900 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
                <img class="w-8 h-8 object-scale-down" src="/static/images/airplane-svgrepo-com.svg" alt="Home Dashboard">
            </button>

            <button type="button" onclick="location.href='/statistics'" class="absolute left-14 p-2 hover:bg-cyan-900 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
                 <img class="w-8 h-8 object-scale-down" src="/static/images/statistics-svgrepo-com.svg" alt="Statistics View">
            </button>

            <h1 class="text-3xl font-bold tracking-wide">{title_text}</h1>

            <button type="button" onclick="location.href='/about'" class="absolute right-28 p-2 hover:bg-cyan-900 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
                <h2 class="text-lg font-semibold">About</h2>
            </button>

            <button type="button" onclick="location.href='/settings'" class="absolute right-0 p-2 hover:bg-cyan-900 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
                <img class="w-6 h-6 object-scale-down" src="/static/images/settings-svgrepo-com.svg" alt="Settings Configuration">
            </button>
        </div>

        
        <main class="max-w-7xl mx-auto w-full">
            {content_html}
        </main>
    </div>

    
    <footer>
        <div class="p-8 font-sans bg-teal-950 text-left flex flex-row">
            <div class="flex-col">
                <div>
                    <button type="button" onclick="location.href='https://github.com/H-J-Wilson/planes'" class="text-cyan-400 hover:text-cyan-300 font-medium underline cursor-pointer transition-colors">
                        GitHub Repository
                    </button>

                </div>
                <div>
                    <button type="button" onclick="location.href='https://github.com/wiedehopf/tar1090'" class="text-cyan-400 hover:text-cyan-300 font-medium underline cursor-pointer transition-colors" target="_blank">
                        tar1090 Project
                    </button>
                </div>
                <div>
                    <br>
                </div>
                <div>
                    <span class="text-slate-400 text-sm block">© 2026 Harry J. Wilson</span>
                </div>
                <div class="flex-row">
                    <div>
                        <span class="text-slate-400 text-sm block">Last Updated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
                    </div>
                    <div>
                        <span class="text-slate-400 text-sm block">Version: v0.0.2 16.08.2026</span>
                    </div>
                </div>
            </div>
            <div class="flex-col">
                <div class="inline-flex items-center gap-2 text-sm">
    
                    <button type="button" onclick="location.href='/contact'" class="text-cyan-400 hover:text-cyan-300 font-medium underline cursor-pointer transition-colors">
                        Contact Me:
                    </button>
    
    
                    <span class="text-slate-400">harry1318945@gmail.com</span>
                </div>
                <div>
                    <button type="button" onclick="location.href='{{ URL }}'" class="text-cyan-400 hover:text-cyan-300 font-medium underline cursor-pointer transition-colors">
                        Live data
                    </button>

                </div>
            </div>

            <button type="button" onclick="location.href='/'" class="absolute right-0 p-2 hover:bg-cyan-900 rounded-lg transition-colors cursor-pointer text-slate-400 hover:text-white">
                <img class="w-8 h-8 object-scale-down" src="/static/images/airplane-svgrepo-com.svg" alt="Home Dashboard">
            </button>
        </div>
    </footer>

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
    <h2>Number of Aircraft: {len(aircraft_data['aircraft'])}</h2>
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
    settings_content = (
        """<div class="text-cyan-400">Settings panel configuration context.</div>"""
    )
    return generate_page_layout(title_text="Settings", content_html=settings_content)


@app.get("/statistics", response_class=HTMLResponse)
def read_statistics():
    statistics_content = (
        """<div class="text-cyan-400">Statistics data dashboard logs.</div>"""
    )
    return generate_page_layout(
        title_text="Statistics", content_html=statistics_content
    )


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


@app.get("/aircraft/{hex_code}", response_class=HTMLResponse)
def read_aircraft_details(hex_code: str):

    about_content = f"""
    <div class="bg-slate-800/50 border border-cyan-800 rounded-xl p-8 max-w-2xl mx-auto shadow-lg">

        <div id="live-details">
            <div class="text-center p-4 text-slate-400 animate-pulse">Loading live aircraft parameters...</div>
        </div>
        
        <div class="mt-8 pt-4 border-t border-slate-700 text-right">
            <a href="/" class="text-cyan-400 hover:text-cyan-300 font-semibold underline">← Back to Dashboard</a>
        </div>
    </div>


    <script>
    async function refreshAircraftStats() {{
        try {{
            const res = await fetch('/api/aircraft/{hex_code}');
            if (res.ok) {{
                const freshHtml = await res.text();
                const container = document.getElementById('live-details');
                if (container) {{
                    container.innerHTML = freshHtml;
                }}
            }}
        }} catch (err) {{
            console.error("Aircraft stats connection dropped:", err);
        }}
    }}
    
    // Initial fetch to load instantly, then establish a 5-second interval timer loop
    refreshAircraftStats();
    setInterval(refreshAircraftStats, 5000);
    </script>
    """
    return generate_page_layout(
        title_text="Aircraft Details", content_html=about_content
    )


@app.get("/api/aircraft/{hex_code}", response_class=HTMLResponse)
def get_aircraft_details_fragment(hex_code: str, response: Response):
    # Enforce strict anti-caching headers so browser tracking values update correctly
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    url = "http://192.168.1.103/tar1090/data/aircraft.json"
    target_plane = None
    try:
        api_res = requests.get(url, timeout=1)
        aircraft_data = api_res.json()

        for plane in aircraft_data.get("aircraft", []):
            if plane.get("hex") == hex_code:
                target_plane = plane
                break
    except Exception:
        pass

    if not target_plane:
        return f"""
        <div class="text-center p-4">
            <p class="text-xl text-red-400 font-medium">Aircraft ({hex_code.upper()}) has flown out of range or landed.</p>
        </div>
        """

    flight = target_plane.get("flight", "Unknown").strip()
    aircraft_type = target_plane.get("desc", "Unknown Type")
    speed = target_plane.get("gs", "N/A")
    altitude = target_plane.get("alt_baro", "N/A")
    squawk = target_plane.get("squawk", "N/A")
    lat = target_plane.get("lat", "N/A")
    lon = target_plane.get("lon", "N/A")
    dst = target_plane.get("r_dst", "N/A")
    dir_h = target_plane.get("r_dir", "N/A")

    clean_hex = hex_code.upper()

    # Return only the inner content fragment text that the script drops inside 'live-details'
    return f"""
    <h2 class="text-2xl font-bold border-b border-cyan-800 pb-4 mb-6 text-cyan-400">
        Flight: {flight} ({clean_hex})
    </h2>
    
    <div class="grid grid-cols-2 gap-6 text-lg">
        <div><span class="text-slate-400 text-sm block">Aircraft Type</span> <strong class="text-white">{aircraft_type}</strong></div>
        <div><span class="text-slate-400 text-sm block">Squawk Code</span> <strong class="text-white">{squawk}</strong></div>
        <div><span class="text-slate-400 text-sm block">Ground Speed</span> <strong class="text-white">{speed} kt</strong></div>
        <div><span class="text-slate-400 text-sm block">Barometric Altitude</span> <strong class="text-white">{altitude} ft</strong></div>
        <div><span class="text-slate-400 text-sm block">Latitude</span> <strong class="text-white">{lat}</strong></div>
        <div><span class="text-slate-400 text-sm block">Longitude</span> <strong class="text-white">{lon}</strong></div>
        <div><span class="text-slate-400 text-sm block">Distance</span> <strong class="text-white">{dst}Nm</strong></div>
        <div><span class="text-slate-400 text-sm block">Bearing</span> <strong class="text-white">{dir_h}°</strong></div>
    """


@app.get("/about", response_class=HTMLResponse)
def read_about():
    about_content = f"""
    
    """
    return generate_page_layout(title_text="About", content_html=about_content)

@app.get("/contact", response_class=HTMLResponse)
def read_contact():
    contact_content = f"""
    
    """
    return generate_page_layout(title_text="Contact", content_html=contact_content)
