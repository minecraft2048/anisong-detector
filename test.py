# coding: utf-8
import parse
from mal import Anime
import sqlite3
from random import randint
from time import sleep
import sys

conn = sqlite3.connect('anisong.db')
c = conn.cursor()

anime = Anime(6702)

if anime.ending_themes  is not None:
    for song1 in anime.ending_themes:
        song1 = song1.lstrip()
        ans = parse.parse('"{title_en} ({title_jp})" by {artist} (eps {start_ep}-{end_ep})', song1)
        if ans is None:
            ans = parse.parse('"{title_en}" by {artist} (eps {start_ep}-{end_ep})', song1)
        if ans is None:
            ans = parse.parse('"{title_en} ({title_jp})" by {artist} (ep {start_ep})', song1)
        if ans is None: 
            ans = parse.parse('"{title_en}" by {artist} (ep {start_ep})', song1)
        if ans is not None:
            ans = ans.named
            print(ans)
            try:
                c.execute("INSERT INTO anisong VALUES (?,?,?,?,?,?,?)",(ans.get("title_en"),ans.get("title_jp"),ans.get("artist"),anime.title,"ending",ans.get("start_ep"),ans.get("end_ep")))
            except sqlite3.IntegrityError:
                print('exist')
        else:
            print(song1)
if anime.opening_themes is not None:        
    for song2 in anime.opening_themes:
        song2 = song2.lstrip()
        ans = parse.parse('"{title_en} ({title_jp})" by {artist} (eps {start_ep}-{end_ep})', song2)
        if ans is None:
            ans = parse.parse('"{title_en}" by {artist} (eps {start_ep}-{end_ep})', song2)
        if ans is None:
            ans = parse.parse('"{title_en} ({title_jp})" by {artist} (ep {start_ep})', song2)
        if ans is None: 
            ans = parse.parse('"{title_en}" by {artist} (ep {start_ep})', song2)
        if ans is not None:
            ans = ans.named
            print(ans)
            try:
                c.execute("INSERT INTO anisong VALUES (?,?,?,?,?,?,?)",(ans.get("title_en"),ans.get("title_jp"),ans.get("artist"),anime.title,"opening",ans.get("start_ep"),ans.get("end_ep")))
            except sqlite3.IntegrityError:
                print('exist')
        else:
            print(song2)
conn.commit()
sleep(1)
