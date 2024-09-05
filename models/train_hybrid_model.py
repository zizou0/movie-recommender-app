import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.model_selection import cross_val_score, GridSearchCV
from surprise import SVD, Dataset, Reader
from surprise.model_selection import GridSearchCV
from surprise.model_selection import train_test_split
from surprise import accuracy
import os
import joblib


ratings = '../data/ratings.dat'
movies = '../data/movies.dat'
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path_ratings = os.path.join(script_dir, ratings)
file_path_movies = os.path.join(script_dir, movies)


ratings_df = pd.read_csv(file_path_ratings, sep='::', engine='python',  names=['UserID', 'MovieID', 'Rating', 'Timestamp'])

movies_df = pd.read_csv(file_path_movies, sep='::', engine='python', names=['MovieID', 'Title', 'Genres'], encoding='latin1')

# Extract the year using regex and create a new column 'Year'
movies_df['Year'] = movies_df['Title'].str.extract(r'\((\d{4})\)')

genres_list = [
    'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 
    'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 
    'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
]

# Splitting the genres into individual genre lists
movies_df['Genres'] = movies_df['Genres'].str.split('|')

# Initialize a DataFrame with zeros for each genre
for genre in genres_list:
    movies_df[genre] = 0

# Iterate through the DataFrame and set the appropriate genre column to 1
for index, row in movies_df.iterrows():
    for genre in row['Genres']:
        if genre in genres_list:
            movies_df.at[index, genre] = 1

# Optionally, drop the original 'Genres' column if it's no longer needed
movies_df.drop('Genres', axis=1, inplace=True)


# Step 3: Feature Engineering for Content-Based Filtering

# Vectorize the movie titles
title_vectorizer = TfidfVectorizer(max_features=100)

# Scale the year of release
scaler = StandardScaler()

# Combine genres, titles, and year into a single feature matrix
feature_union = FeatureUnion([
    ('genres', Pipeline([('dummy', None)])),  # This is a placeholder for genres (already one-hot encoded)
    ('titles', title_vectorizer),
    ('year', scaler)
])

content_features = np.hstack([
    movies_df[genres_list].values,  # One-hot encoded genres
    title_vectorizer.fit_transform(movies_df['Title']).toarray(),  # TF-IDF vectorized titles
    scaler.fit_transform(movies_df[['Year']])  # Scaled years
])

# Step 4: Compute Content Similarity Matrix

content_similarity_matrix = cosine_similarity(content_features)

# Step 5: Train the Collaborative Filtering Model

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['UserID', 'MovieID', 'Rating']], reader)

# Hyperparameter tuning for SVD
param_grid = {
    'n_factors': [50, 100, 150],
    'n_epochs': [20, 30, 40],
    'lr_all': [0.005, 0.010, 0.020],
    'reg_all': [0.02, 0.1, 0.4]
}

gs = GridSearchCV(SVD, {'n_factors': [50], 'n_epochs': [20],
    'lr_all': [.005],
    'reg_all': [.02]}, measures=['rmse'], cv=5)
gs.fit(data)

best_svd_model = gs.best_estimator['rmse']
# Now build the trainset from the data
trainset = data.build_full_trainset()


# Fit the best SVD model on the full trainset

best_svd_model.fit(trainset)

# Making a prediction without accessing trainset directly

# best_svd_model = SVD()

# trainset, testset = train_test_split(data, test_size=0.25)

# best_svd_model.fit(trainset)

# predictions = best_svd_model.test(testset)

# Calculate RMSE (Root Mean Square Error)
# rmse = accuracy.rmse(predictions)



# Step 6: Save the Models

joblib.dump(content_similarity_matrix,  os.path.join(script_dir, '../models/content_similarity_matrix.pkl'))
joblib.dump(best_svd_model, os.path.join(script_dir, '../models/svd_model.pkl'))









