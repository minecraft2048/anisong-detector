
from fuzzywuzzy import process
import sqlite3
from gi.repository import GLib
from pydbus import SessionBus
from time import sleep
import subprocess
import time


#TF-IDF approach
import pandas as pd, numpy as np, re
from sparse_dot_topn import awesome_cossim_topn
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

expected_song = "Thank You!!"
test_song = "Home Made Kazoku - Thank You!!"

def ngrams(string, n=4):
    try:
        string = (re.sub(r'[,-./]|\sBD',r'', string)).upper()
        ngrams = zip(*[string[i:] for i in range(n)])
        return [''.join(ngram) for ngram in ngrams]
    except TypeError:
        print(string)
        raise

conn = sqlite3.connect("anisong.db")
def identify_anisong(title,artist=None):
    if artist is not None:
        pass
    else:
        song = process.extractOne(title, conn.execute("select title_en from anisong"),score_cutoff=85) #fuzzy match title with song titles from database
        #if song is None:
        #   return None
        #return conn.execute("select anime,type,start_ep,end_ep from anisong where title_en = ?",song[0]).fetchone()
        
print("Levenshtein distance database access")
total = 0
for i in range(1,11):
    start = time.time()
    matched_song = process.extractOne(test_song, conn.execute("select title_en from anisong"),score_cutoff=85)
    end = time.time()
    duration = end - start
    total += duration
    print(f"Iteration {i}: {duration}")

print(f"Matched {matched_song} expected {expected_song}")
print(f"Avg duration: {total/10}")
time_lev_1 = total/10

print("Levenshtein distance python array")
songs = []
for song in conn.execute("select title_en from anisong"):
    songs.append(song[0])

total = 0
for i in range(1,11):
    start = time.time()
    matched_song = process.extractOne(test_song,songs,score_cutoff=85)
    end = time.time()
    duration = end - start
    total += duration
    print(f"Iteration {i}: {duration}")

print(f"Matched {matched_song} expected {expected_song}")
print(f"Avg duration: {total/10}")
time_lev_2 = total/10
print(f"Time saved over Levenshtein distance database: {time_lev_1 - time_lev_2}s ({time_lev_1/time_lev_2}x speedup)")


print("TF-IDF matching")

conn.row_factory = lambda cursor, row: row[0]
songs = conn.execute("select title_en from anisong").fetchall()

vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
tf_idf_matrix_songs = vectorizer.fit_transform(songs)



total = 0
for i in range(1,11):
    start = time.time()
    tf_idf_matrix_test = vectorizer.transform([test_song])
    matches = awesome_cossim_topn(tf_idf_matrix_test, tf_idf_matrix_songs.transpose(), 1, 0)
    print(matches)
    end = time.time()
    duration = end - start
    total += duration
    print(f"Iteration {i}: {duration}")


song2 = songs[matches.nonzero()[1][0]]
print(f"Matched {song2} expected {expected_song} certainty {matches.data[0]}")

print(f"Avg duration: {total/10}")
time_tf = total/10
#print(f"Time saved over Levenshtein distance: {time_lev_2 - time_tf}s ({time_lev_2/time_tf}x speedup)")