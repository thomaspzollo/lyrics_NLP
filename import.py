import pandas as pd
import numpy as np
from numpy import mean
from numpy import std

import csv
import sys
import string
import re
import os

from sentence_transformers import SentenceTransformer
import lyricsgenius


genius = lyricsgenius.Genius(GTOKEN)

artists = ["Eminem","DaBaby","Travis Scott","Drake","Nicki Minaj","Cardi B","Lil Baby","Post Malone","Kendrick Lamar"]


### Import Songs for each artist
for a in artists:
  artist = genius.search_artist(a, max_songs=200, sort='popularity')
  songs = artist.songs

  for s in songs:

    new_row = {"Artist":s.artist, "Title":s.title, "Lyrics":s.lyrics}
    lyrics_df = lyrics_df.append(new_row, ignore_index=True)

lines = []
targets = []
counts = {}

### ITERATE BY SONG, split lyrics into blocks of 4 lines
for i in range( lyrics_df.shape[0] ):
  row = lyrics_df.iloc[i]
  text = row['Lyrics'].split('\n')

  j = 0
  
  while j < len(text):

    count = 0
    if (text[j] != '' and text[j][0] == '['): 
      next = ""
    else:
      next = text[j]
      count = 1

    while j < len(text)-1 and count < 4:
      j += 1
      if (text[j] != '' and text[j][0] != '['): 
        next += " " + text[j]
        count += 1
    
    lines.append(next.lstrip(' '))
    targets.append(row['Artist'])
    counts[row['Artist']] = counts.get(row['Artist'],0) + 1
    j += 1

df = pd.DataFrame()
df['Lyric'] = lines
df['Artist'] = targets

df.drop_duplicates(keep = 'first', inplace = True)

train_bal = pd.DataFrame(columns=['Lyric','Artist'])
val_bal = pd.DataFrame(columns=['Lyric','Artist'])
test_bal = pd.DataFrame(columns=['Lyric','Artist'])

art2idx = {}
count = 0

for artist in artists:

  results = df[(df['Artist'] == artist)]

  print(artist)
  print(results.shape[0])
  if results.shape[0] > 2200:
  
    art2idx[artist] = count
    count += 1

    results = results.sample(frac=1)

    tr_batch = results.iloc[:1600,:]
    train_bal = pd.concat([train_bal, tr_batch])  

    v_batch = results.iloc[1600:1900,:]
    val_bal = pd.concat([val_bal, v_batch])

    te_batch = results.iloc[1900:2200,:]
    test_bal = pd.concat([test_bal, te_batch])

n_artists = count

train_df = train_bal
val_df = val_bal
test_df = test_bal

if n_artists == 2:

	train_df.to_csv('train_df_b.csv')
	files.download('train_df_b.csv')

	val_df.to_csv('val_df_b.csv')
	files.download('val_df_b.csv')

	test_df.to_csv('test_df_b.csv')
	files.download('test_df_b.csv')

else:

	train_df.to_csv('train_df_m.csv')
	files.download('train_df_m.csv')

	val_df.to_csv('val_df_m.csv')
	files.download('val_df_m.csv')

	test_df.to_csv('test_df_m.csv')
	files.download('test_df_m.csv')

print(train_df)
print(val_df)
print(test_df)