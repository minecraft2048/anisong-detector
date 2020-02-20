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



#TF-IDF approach
import pandas as pd, numpy as np, re
from sparse_dot_topn import awesome_cossim_topn
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

songs = [None] * (conn.execute("select count(*) from anisong").fetchone()[0])
for song in conn.execute("select rowid,title_en,anime from anisong"):
    songs[song[0]-1] = song[1]

def ngrams(string, n=4):
    try:
        string = (re.sub(r'[,-./]|\sBD',r'', string)).upper()
        ngrams = zip(*[string[i:] for i in range(n)])
        return [''.join(ngram) for ngram in ngrams]
    except TypeError:
        print(string)
        raise

vectorizer = TfidfVectorizer(min_df=1, analyzer='char',ngram_range=(3,3))
print("Building TF-IDF matching matrix")
tf_idf_matrix_songs = vectorizer.fit_transform(songs)
print(f"Matrix size: {tf_idf_matrix_songs.data.nbytes + tf_idf_matrix_songs.indptr.nbytes + tf_idf_matrix_songs.indices.nbytes} bytes")
conn.row_factory = None

def identify_anisong_tf(title,artist=None):
    #fuzzy match title with song titles from database using cosine similarity over TF-IDF matrix
    #
    if artist is not None:
        pass
    else:
        tf_idf_matrix_test = vectorizer.transform([title])
        matches = awesome_cossim_topn(tf_idf_matrix_test, tf_idf_matrix_songs.transpose(), 1, 0)
        song2 = songs[matches.nonzero()[1][0]]
        confidence = int(matches.data[0]*100)
        #print(confidence)
        #print(song2)
        return conn.execute(f"select anime,type,start_ep,end_ep from anisong where rowid = {matches.nonzero()[1][0]}").fetchone() + (confidence,)



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
            anime,song_type,start_ep,end_ep,confidence = identify_anisong_tf(title)
            print(f"{title} : {anime} {song_type} eps {start_ep}-{end_ep} confidence:{confidence}")
            notifications.Notify('anisong_detector', 0, 'dialog-information', title, f"{anime} {song_type} eps {start_ep}-{end_ep}", [], {}, 5000)
            change_wallpaper(anime)
            sleep(1)
        except TypeError:
            pass
        prev_title = title
    sleep(0.1)