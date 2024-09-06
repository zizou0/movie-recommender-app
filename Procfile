web: PYTHONPATH=/movie_recommender_backend gunicorn movie_recommender_backend.movie_recommender.wsgi:application 
--log-file -
release: PYTHONPATH=/movie_recommender_backend  python movie_recommender_backend/manage.py migrate

