from django.urls import path
from .views import recommend_movies
from .views import test_view

urlpatterns = [
    path('api/recommend/', recommend_movies, name='recommend_movies'),
    path('api/test/', test_view, name='test_view')
]

# Maps the /recommend/ URL to the recommend_movies view.
