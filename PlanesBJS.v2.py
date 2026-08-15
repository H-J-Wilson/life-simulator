#READSB devlopment python 22092025 Barry
print("PlanesBJS.v2.py 22092025")

#Harry orig Planes working version
#13092025 BJS modified for tests reads distance & bearing, lat lon removed, extra lines removed
#15092025 Add military aircraft with reg, type, sound notification
#18092025 Add track to military
#22092025 Use - instead of default none
#09102025 Add Callsign to military to check SkyGrid

from urllib.request import urlopen, URLError
import json
import requests
import time
import pygame
pygame.init()
from datetime import datetime

my_sound = pygame.mixer.Sound('/usr/share/sounds/sound-icons/electric-piano-3.wav')

url="http://localhost/tar1090/data/aircraft.json"    

def planes():
    respones = requests.get(url)
    if respones.status_code == 200:
        aircraft_data=respones.json()
    else:
        print("error geting data")        
        return
        
    print(f"Found {len(aircraft_data['aircraft'])} Aircraft")  

    for a in aircraft_data['aircraft']:
       hex = a.get('hex', "-")
       desc = a.get('desc', "-")
       flight = a.get('flight', "-")
       callsign = a.get('callsign','-')
       r = a.get('reg', "-")
       t = a.get('type', "-")
       tas = a.get('tas', "-")
       alt_geom = a.get('alt_geom', "-")
       r_dst = a.get('r_dst', "-")
       r_dir = a.get('r_dir', "-")
       dbFlags = a.get('dbFlags')
       desc = a.get('desc', "-")
       track = a.get('track',"-")
       
       if hex:         
        print("ID: {hex} Flt: {flight} Desc: {desc} Speed: {tas}Ks Altitude: {alt_geom}Ft Distance: {r_dst}Nm Bearing: {r_dir}Deg".format(hex=hex, flight=flight, desc=desc, tas=tas, alt_geom=alt_geom, r_dst=r_dst, r_dir=r_dir, ),)
 
        if dbFlags is not None:
            military = dbFlags & 1;
            print("Military Callsign: {callsign} Reg: {r} Type: {t} dbFlags: {dbFlags} Track: {track}".format(callsign=callsign, r=r, t=t, dbFlags=dbFlags, track=track, ),)
            my_sound.play()
            interesting = dbFlags & 2
            PIA = dbFlags & 4;
            LADD = dbFlags & 8
#        else:
#           print("No military or interesting aircraft")
                          
if __name__ == "__main__":
    while True:
        now = datetime.now()
        print("Time", now.strftime("%H:%M:%S"))
        planes()
        time.sleep(30)
