# coding: utf-8

from fuzzywuzzy import process
import sqlite3
from gi.repository import GLib
from pydbus import SessionBus
from time import sleep
import subprocess


conn = sqlite3.connect("anisong.db")

def identify_anisong(title,artist=None):
    #fuzzy match title with song titles from database using Levenshtein distance: https://en.wikipedia.org/wiki/Levenshtein_distance
    if artist is not None:
        pass
    else:
        #fuzzy match title with song titles from database using Levenshtein distance: https://en.wikipedia.org/wiki/Levenshtein_distance
        song = process.extractOne(title, conn.execute("select title_en from anisong"),score_cutoff=85) 
        if song is None:
            return None
        return conn.execute("select anime,type,start_ep,end_ep from anisong where title_en = ?",song[0]).fetchone() + (song[1],)

def change_wallpaper(title):
    #todo: change this to use dbus interface instead of running another program
    cmd = f' var allDesktops = desktops(); print (allDesktops); for (i=0;i<allDesktops.length;i++) {{{{ d = allDesktops[i]; d.wallpaperPlugin = "org.kde.image"; d.currentConfigGroup = Array("Wallpaper","org.kde.image", "General"); d.writeConfig("Image", "file:///home/minato/Development/anisong/wallpaper/{title}.jpg")}}}}' 
    subprocess.run(["qdbus","org.kde.plasmashell","/PlasmaShell","org.kde.PlasmaShell.evaluateScript",cmd])
                                      


b = SessionBus()
m = b.get("org.mpris.MediaPlayer2.plasma-browser-integration", "/org/mpris/MediaPlayer2")
notifications = b.get('.Notifications')

prev_title = ""

while True:
    title = m.Metadata['xesam:title']
    if title != prev_title:
        try:
            anime,song_type,start_ep,end_ep,confidence = identify_anisong(title)
            print(f"{title} : {anime} {song_type} eps {start_ep}-{end_ep} confidence:{confidence}")
            notifications.Notify('anisong_detector', 0, 'dialog-information', title, f"{anime} {song_type} eps {start_ep}-{end_ep}", [], {}, 5000)
            change_wallpaper(anime)
            sleep(1)
        except TypeError:
            pass
        prev_title = title
    sleep(0.1)