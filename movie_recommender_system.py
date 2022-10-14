# -*- coding: utf-8 -*-
"""Movie recommender system.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ju1aDP8xnQ_o5rDzjzqo-eqqoKY30tFe
"""

import numpy as np
import pandas as pd

movies=pd.read_csv('/content/tmdb_5000_movies.csv')
credits=pd.read_csv('/content/tmdb_5000_credits.csv')

movies.head()

credits.head(1)

credits.head(1)['cast'].values

movies.merge(credits,on='title')

movies.shape

movies=movies.merge(credits,on='title')

movies.head()

movies.info()

#id
#Title
#genres
#keywords
#overview
#cast
#crew
movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.head()

movies.isnull().sum()

movies.dropna(inplace=True)

movies.duplicated().sum()

movies.iloc[0].genres

import ast
def convert(obj):
  l=[]
  for i in ast.literal_eval(obj):
    l.append(i['name'])
  return l

movies['genres']=movies['genres'].apply(convert)

movies['keywords']=movies['keywords'].apply(convert)

def convert3(obj):
  l=[]
  counter=0
  
  for i in ast.literal_eval(obj):
    if counter!=3:
       l.append(i['name'])
       counter+=1;
  return l

movies['cast']=movies['cast'].apply(convert3)

movies['crew'][0]

def fetch_director(obj):
  l=[]
  for i in ast.literal_eval(obj):
    if i['job']=='Director':
      l.append(i['name'])
      break
  return l

movies['crew']=movies['crew'].apply(fetch_director)

movies.head()

movies['overview']=movies['overview'].apply(lambda x:x.split())

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

new_df=movies[['movie_id','title','tags']]

new_df.head()

new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))

new_df['tags'][0]

new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
  l=[]
  for i in text.split():
    l.append(ps.stem(i))
  return " ".join(l)

new_df['tags']=new_df['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')

vectors=cv.fit_transform(new_df['tags']).toarray()

vectors[0]

cv.get_feature_names()



from sklearn.metrics.pairwise import cosine_similarity

similarity=cosine_similarity(vectors)

movie_list=sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]

def recommend(movie):
   movie_index=new_df[new_df['title']==movie].index[0]
   distance=similarity[movie_index]
   movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
   
   
   for i in movie_list:
    print(new_df.iloc[i[0]].title)

recommend('Avatar')

import pickle
pickle.dump(new_df,open('movies.pkl','wb'))

pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))

pickle.dump(similarity,open('similarity.pkl','wb'))