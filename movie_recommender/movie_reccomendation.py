import pandas as pd
import matplotlib.pyplot as plt
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def dict_to_str(row):
    genres = json.loads(row['genres'])
    genres = ' '.join(''.join(i['name'].split()) for i in genres)

    key = json.loads(row['keywords'])
    key = ' '.join(''.join(i['name'].split()) for i in key)

    retstr = genres + " " + key

    return retstr

df = pd.read_csv("tmdb_5000_movies.csv")
df['title'] = df['title'].str.lower()

df['string'] = df.apply(dict_to_str, axis=1)

tfidf = TfidfVectorizer(max_features=2000) #object
x = tfidf.fit_transform(df['string'])

movieind = pd.Series(df.index, index=df['title'])

def getrec(name):
    ind = movieind[name]
    query = x[ind]

    scores = cosine_similarity(query, x)

    scores = scores.flatten()
    scores = (-scores).argsort()

    rec = scores[1:6]
    ret = df['original_title'].iloc[rec]
    return ret

moviename = input("movie you watched: ")
moviename = moviename.lower()

if (df['title'].eq(moviename).any() == False):
    print("movie not in database")

else:
    print("reccomended titles: ")
    print(getrec(moviename))