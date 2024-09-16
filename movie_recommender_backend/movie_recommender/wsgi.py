"""
WSGI config for movie_recommender project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Add your project directory to the sys.path
sys.path.append('/app/movie-recommender/movie_recommender_backend')

os.environ.setdefault("DJANGO_SETTINGS_MODULE",  "movie-recommender.movie_recommender_backend.movie_recommender.settings")

application = get_wsgi_application()
