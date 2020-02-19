
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
conn = sqlite3.connect("anisong.db")
conn.row_factory = lambda cursor, row: row[0]

songs = conn.execute("select title_en from anisong").fetchall()

def ngrams(string, n=4):
    try:
        string = (re.sub(r'[,-./]|\sBD',r'', string)).upper()
        ngrams = zip(*[string[i:] for i in range(n)])
        return [''.join(ngram) for ngram in ngrams]
    except TypeError:
        print(string)
        raise

vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
tf_idf_matrix_songs = vectorizer.fit_transform(songs)

test_vector = [
    ("Home Made Kazoku - Thank You!!","Thank You!!"),
    ("Rie Fu - Life is Like a Boat [HD]","Life is Like a Boat")
]

print(f"|{'Input text': ^34}|{'Expected match': ^34}|{'Levenshtein': ^34}|% |{'TF-IDF': ^34}|% |")

for test in test_vector:
    matched_song = process.extractOne(test[0], conn.execute("select title_en from anisong"),score_cutoff=85)
    tf_idf_matrix_test = vectorizer.transform([test[0]])
    matches = awesome_cossim_topn(tf_idf_matrix_test, tf_idf_matrix_songs.transpose(), 1, 0)
    song2 = songs[matches.nonzero()[1][0]]
    certainty = int(matches.data[0]*100)
    print(f"|{test[0]: <34}|{test[1]: <34}|{matched_song[0]: <34}|{matched_song[1]:2}|{song2: <34}|{certainty:2}|")
