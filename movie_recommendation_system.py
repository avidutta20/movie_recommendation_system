# -*- coding: utf-8 -*-
"""Movie_Recommendation_System.ipynb

## Using Collaborative Filtering
"""


# importing libraries
import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
 %matplotlib inline

#importing movie dataset from GroupLens
try:
  !wget -o ml-latest-small.zip http://files.grouplens.org/datasets/movielens/ml-latest-small.zip
  print('Downloaded!')
  print('Unzipping')
  !unzip -o -j '/content/ml-latest-small.zip.1'
  print('Dataset Successfully Processed!')
except:
  print('Unable to get the Movie Dataset!')

# Creating Path
path = '/content/'
csv_links = path + 'links.csv'
csv_movies = path + 'movies.csv'
csv_ratings = path + 'ratings.csv'
csv_tags = path + 'tags.csv'

#Storing the movie information into a pandas dataframe
movies_df = pd.read_csv(csv_movies)
#Storing the user information into a pandas dataframe
ratings_df = pd.read_csv(csv_ratings)


# Creating a separate column for Release Year
movies_df['year'] = movies_df.title.str.extract('(\(\d\d\d\d\))',expand = False)
# Removing Parenthesis from title
movies_df['year'] = movies_df.year.str.extract('(\d\d\d\d)', expand = False)

movies_df['title'] = movies_df.title.str.replace('(\(\d\d\d\d\))','')
# Removing any extra spaces
movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())
# Creating Genres
movies_df['genres_vector'] = movies_df['genres'].apply(lambda x: x.split('|'))


# Getting all Unique genres
movie_genre_list = list()

for index in movies_df.index:
  this_movie_genre_list = movies_df.iloc[index,4]
  for genre in this_movie_genre_list:
    if genre not in movie_genre_list:
      movie_genre_list.append(genre)
    else:
      continue
movie_genre_list

# Let's see movies with no genres listed
movies_df.loc[movies_df.genres.str.find('no genres listed')>0]

# Instantiating a user with customised Input
# It will vary as per user
userInput = [
            {'title':'Breakfast Club, The', 'rating':5},
            {'title':'Toy Story', 'rating':3.5},
            {'title':'Jumanji', 'rating':2},
            {'title':"Pulp Fiction", 'rating':5},
            {'title':'Akira', 'rating':4.5}
         ] 
inputMovies = pd.DataFrame(userInput)
inputMovies

# Getting all MovieIds of inputMovies
inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]
inputId

inputMovies = pd.merge(inputId, inputMovies)
inputMovies

inputMovies = inputMovies.drop('year', 1)
inputMovies

inputMovies['movieId'].tolist()

# Finding all users who have given Ratings i.e watched the above movies
userSubset = ratings_df[ratings_df['movieId'].isin(inputMovies['movieId'].tolist())]
userSubset

# Grouping users by userId groupby
userSubsetGroup =  userSubset.groupby(['userId'])

# Sorting so that users having highest number of movie in common with InputUser are in higher priority
userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

print(userSubsetGroup[0])



