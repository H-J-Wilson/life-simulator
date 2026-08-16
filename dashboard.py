import json
import requests
import time
from datetime import datetime


def python_dashboard():
    while True:
        url = "http://192.168.1.103/tar1090/data/aircraft.json"
        gap = 30  # Default gap between updates in seconds
        now = datetime.now()
        print("Time", now.strftime("%H:%M:%S"))
        planes(url)
        time.sleep(gap)


def planes(url):
    respones = requests.get(url)
    if respones.status_code == 200:
        aircraft_data = respones.json()
    else:
        print("error geting data")
        return

    print(f"Found {len(aircraft_data['aircraft'])} Aircraft\n")

    for a in aircraft_data["aircraft"]:
        hex = a.get("hex", "-")
        desc = a.get("desc", "-")
        flight = a.get("flight", "-")
        flight = flight.replace(" ", "")
        callsign = a.get("callsign", "-")
        r = a.get("reg", "-")
        t = a.get("type", "-")
        tas = a.get("tas", "-")
        alt_geom = a.get("alt_geom", "-")
        r_dst = a.get("r_dst", "-")
        r_dir = a.get("r_dir", "-")
        dbFlags = a.get("dbFlags")
        desc = a.get("desc", "-")
        track = a.get("track", "-")

        if dbFlags is not None:
            military = dbFlags & 1
            print(
                "Military Callsign: {callsign} Reg: {r} Type: {t} dbFlags: {dbFlags} Track: {track}".format(
                    callsign=callsign,
                    r=r,
                    t=t,
                    dbFlags=dbFlags,
                    track=track,
                ),
            )
            interesting = dbFlags & 2
            PIA = dbFlags & 4
            LADD = dbFlags & 8

        elif hex:
            print(
                "ID: {hex}, Flt: {flight}, Desc: {desc}, Speed: {tas}Ks, Altitude: {alt_geom}Ft, Distance: {r_dst}Nm, Bearing: {r_dir}°".format(
                    hex=hex,
                    flight=flight,
                    desc=desc,
                    tas=tas,
                    alt_geom=alt_geom,
                    r_dst=r_dst,
                    r_dir=r_dir,
                ),
            )
        else:
            print("Error fettching hex")

        print("\n")

    settings = input("Do you want to change the dashboard settings?: ")
    while settings is True:
        py_dashboard_settings(settings)


def py_dashboard_settings(settings):
    while settings is True:
        print("Dashboard settings")
        gap_try = input("Enter gap between updates (seconds): ")

        try:
            gap = int(gap_try)
            print(f"Gap between updates set to {gap} seconds")
            settings = False
        except ValueError:
            print("Invalid input. Please enter a valid integer for the gap.")
            settings = True