
from gi.repository import GLib
from time import sleep

loop = GLib.MainLoop()
from pydbus import SessionBus

b = SessionBus()
m = b.get("org.mpris.MediaPlayer2.plasma-browser-integration", "/org/mpris/MediaPlayer2")
notifications = b.get('.Notifications')

prev_title = ""

while True:
    title = m.Metadata['xesam:title']
    if title != prev_title:
        notifications.Notify('anisong_detector', 0, 'dialog-information', title, "pydbus works :)", [], {}, 5000)
        prev_title = title
    sleep(0.1)