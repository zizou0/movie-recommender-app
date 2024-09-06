from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import joblib
import json
import numpy as np
import re
import os
from django.conf import settings

content_similarity_matrix = joblib.load(os.path.join(settings.BASE_DIR, '..', 'models', 'content_similarity_matrix.pkl'))
svd_model = joblib.load(os.path.join(settings.BASE_DIR, '..', 'models', 'svd_model.pkl'))



# Load precomputed models
#content_similarity_matrix = joblib.load("/Users/benedictzuzi/Documents/movie-recommender/models/content_similarity_matrix.pkl")
#svd_model = joblib.load("/Users/benedictzuzi/Documents/movie-recommender/models/svd_model.pkl")
file_path_movies = "/Users/benedictzuzi/Documents/movie-recommender/data/movies.dat"


# Load your movies DataFrame at the module level to be accessible within the view
movies_df = pd.read_csv(file_path_movies, sep='::', header=None, engine='python', names=['MovieID', 'Title', 'Genres'], encoding='latin1')

def normalize_title(title):
    """
    Normalize movie title by handling leading articles and removing the year from the title.
    """
    # Regular expression to remove year in parentheses (e.g., "Toy Story (1995)" -> "Toy Story")
    title = re.sub(r'\(\d{4}\)', '', title).strip()
    
    # Move articles from the end of the title to the front (e.g., "Godfather, The" -> "The Godfather")
    articles = ['The', 'A', 'An']
    
    # Split the title by comma and check if the last part is an article
    if ',' in title:
        parts = title.split(', ')
        if parts[-1] in articles:
            title = f"{parts[-1]} {parts[0]}"
    
    return title.lower()

print(normalize_title("Grand Day Out, A (1995)"))


def hybrid_recommendation(movie_id, content_similarity_matrix, svd_model, movies_df, top_n=4, alpha=0.7):
    movie_idx = movies_df[movies_df['MovieID'] == movie_id].index[0]
    
    # Content-based recommendations
    content_similarities = content_similarity_matrix[movie_idx]
    
    # Collaborative filtering predictions
    movie_ids = movies_df['MovieID'].values
    collaborative_scores = np.array([svd_model.predict(uid=0, iid=mid).est for mid in movie_ids])
    
    # Hybrid score
    hybrid_scores = alpha * content_similarities + (1 - alpha) * collaborative_scores
    
    # Get the top N similar movies
    top_indices = hybrid_scores.argsort()[-top_n-1:-1][::-1]
    top_movie_ids = movie_ids[top_indices]
    
    return top_movie_ids


@csrf_exempt
def recommend_movies(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            movie_title = data.get('title', '').strip()
            
            # Normalize the input movie title
            normalized_input_title = normalize_title(movie_title)

            # Ensure the title is provided
            if not movie_title:
                return JsonResponse({'error': 'No movie title provided'}, status=400)

            # Normalize the titles in the DataFrame for matching
            movies_df['normalized_title'] = movies_df['Title'].apply(normalize_title)

            # Find the movie ID for the provided title
            movie_row = movies_df[movies_df['normalized_title'] == normalized_input_title]
            
            if movie_row.empty:
                return JsonResponse({'error': 'Movie not found'}, status=404)

            movie_id = movie_row.iloc[0]['MovieID']

            # Generate recommendations using the hybrid model
            recommended_movie_ids = hybrid_recommendation(
                movie_id, content_similarity_matrix, svd_model, movies_df, top_n=4, alpha=0.5
            )

            # Map recommended movie IDs back to titles
            recommended_movies = movies_df[movies_df['MovieID'].isin(recommended_movie_ids)]['Title'].tolist()

            return JsonResponse({
                'input_movie_title': movie_title,
                'recommended_movies': recommended_movies
            })

        except KeyError:
            return JsonResponse({'error': 'Missing title'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
@csrf_exempt
def test_view(request):
    return JsonResponse({'message': 'Test successful'})



# Create your views here.
