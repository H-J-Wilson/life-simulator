#SkyGrid Ultimate 22092025
#22092025 Try hard coded user location to fix map Line 105
#         Print out starting conditions after menu input

import sys
import os
import sqlite3
import requests
import time
from datetime import datetime, timedelta
import folium
from folium.plugins import MarkerCluster
import webbrowser
import json

DB_PATH = "skygrid_ultimate.db"
DEFAULT_REFRESH = 5  # seconds
MILITARY_COOLDOWN_HOURS = 24

# --- Database Initialization ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS aircraft (
        icao TEXT PRIMARY KEY,
        callsign TEXT,
        latitude REAL,
        longitude REAL,
        military INTEGER,
        last_seen TIMESTAMP
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP,
        message TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS analytics (
        feed_url TEXT PRIMARY KEY,
        total_aircraft INTEGER,
        military_count INTEGER,
        civilian_count INTEGER,
        last_update TIMESTAMP
    )""")
    conn.commit()
    conn.close()

# --- Logging ---
def log_error(message):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO logs (timestamp, message) VALUES (?, ?)", (datetime.utcnow(), message))
    conn.commit()
    conn.close()
    print(message)

# --- Log Military Aircraft ---
def log_military(icao):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now = datetime.utcnow()
    cur.execute("SELECT last_seen FROM aircraft WHERE icao=? AND military=1", (icao,))
    row = cur.fetchone()
    if row:
        last_seen = datetime.fromisoformat(row[0])
        if now - last_seen < timedelta(hours=MILITARY_COOLDOWN_HOURS):
            conn.close()
            return
    cur.execute("INSERT OR REPLACE INTO aircraft (icao, callsign, latitude, longitude, military, last_seen) VALUES (?,?,?,?,?,?)",
                (icao, '', 0, 0, 1, now))
    conn.commit()
    conn.close()

# --- Fetch Aircraft Data ---
def fetch_aircraft(url):
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        return data.get('aircraft', [])
    except Exception as e:
        log_error(f"Failed to fetch {url}: {e}")
        return []

# --- Detect Local tar1090 Feed ---
def detect_local_feed():
    potential_feeds = [
#      "http://127.0.0.1:8080/data/aircraft.json",
#      "http://localhost:8080/data/aircraft.json",
        "http://127.0.0.1/data/aircraft.json",
        "http://localhost/data/aircraft.json",     
        "http://192.168.0.183/tar1090/data/aircraft.json",
        "http://192.168.1.105/tar1090/data/aircraft.json"      
    ]
    valid_feeds = []
    for url in potential_feeds:
        try:
            resp = requests.get(url, timeout=2)
            if resp.status_code == 200:
                valid_feeds.append(url)
        except:
            continue
    return valid_feeds

# --- Update Map and Analytics ---
def update_map(feeds, user_location=None):
#    fmap = folium.Map(location=user_location if user_location else [20,0], zoom_start=2)
    fmap = folium.Map(location=user_location if user_location else [51.5103,-1.53611], zoom_start=10)
    marker_cluster = MarkerCluster().add_to(fmap)

    for feed in feeds:
        aircraft_list = fetch_aircraft(feed)
        military_count = 0
        civilian_count = 0
        for ac in aircraft_list:
            icao = ac.get('icao','-')
            callsign = ac.get('callsign','-')
            lat = ac.get('latitude', 0)
            lon = ac.get('longitude', 0)
            military = ac.get('military', False)
#            dbFlag = ac.get('military', False)
            print("icao: {icao} callsign: {callsign} lat: {lat} lon: {lon}".format(icao=icao, callsign=callsign, lat=lat, lon=lon, ),)

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("INSERT OR REPLACE INTO aircraft (icao, callsign, latitude, longitude, military, last_seen) VALUES (?,?,?,?,?,?)",
                        (icao, callsign, lat, lon, int(military), datetime.utcnow()))
            conn.commit()
            conn.close()

            if military:
                log_military(icao)
                military_count += 1
            else:
                civilian_count += 1

            color = 'purple' if military else 'blue'
            folium.CircleMarker(location=[lat, lon], radius=5, color=color, fill=True, fill_color=color,
                                popup=f"{callsign} ({icao})").add_to(marker_cluster)

        # Update analytics
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO analytics (feed_url, total_aircraft, military_count, civilian_count, last_update)
        VALUES (?,?,?,?,?)
        """, (feed, len(aircraft_list), military_count, civilian_count, datetime.utcnow()))
        conn.commit()
        conn.close()

    map_path = os.path.join(os.getcwd(), "skygrid_map.html")
    fmap.save(map_path)
    print(f"Map updated and saved to {map_path}")

    # Auto-open browser if first run
    if not hasattr(update_map, 'opened'):
        webbrowser.open(f'file://{map_path}', new=2)
        update_map.opened = True

# --- Start Menu ---
def start_menu():
    print("=== Welcome to SkyGrid Ultimate ===")
    feeds = detect_local_feed()
    refresh_rate = DEFAULT_REFRESH
    user_location = [20,0]

    while True:
        print("\n--- Menu ---")
        print("1. Set refresh rate")
        print("2. Add feed URL")
        print("3. Set your location")
        print("4. Show analytics")
        print("5. Start tracking")
        print("6. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                refresh_rate = int(input("Enter refresh rate in seconds: "))
                print(f"Refresh rate set to {refresh_rate}s")
            except:
                print("Invalid input")
        elif choice == "2":
            url = input("Enter feed URL: ").strip()
            if url:
                feeds.append(url)
                print(f"Feed URL set to {url}")
        elif choice == "3":
            try:
                lat = float(input("Enter your latitude: "))
                lon = float(input("Enter your longitude: "))
                user_location = [lat, lon]
                print(f"Location set to {user_location}")
            except:
                print("Invalid location input")
        elif choice == "4":
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT feed_url, total_aircraft, military_count, civilian_count, last_update FROM analytics")
            rows = cur.fetchall()
            conn.close()
            print("\n--- Analytics ---")
            for r in rows:
                print(f"Feed: {r[0]} | Total: {r[1]} | Military: {r[2]} | Civilian: {r[3]} | Last Update: {r[4]}")
        elif choice == "5":
            print(f"Refresh rate set to {refresh_rate}s")
            print(f"Feed URL set to {url}")
            print(f"Location set to {user_location}")
            print("Starting SkyGrid Ultimate tracking. Press Ctrl+C to exit.")
            try:
                while True:
                    update_map(feeds, user_location)
                    time.sleep(refresh_rate)
            except KeyboardInterrupt:
                print("Exiting SkyGrid Ultimate.")
                break
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    init_db()
    start_menu()
