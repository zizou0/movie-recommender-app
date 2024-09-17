# movie-recommender-app

## Overview
The Movie Recommender System is an end-to-end web application built to recommend movies to users based on their preferences. It employs collaborative filtering (using Singular Value Decomposition - SVD) and content-based filtering to deliver personalized movie recommendations. The app includes both a Django-based backend and a React-based frontend and is deployed on Heroku.


## Features
- 🎥 Personalized Recommendations: Offers movie recommendations tailored to user preferences using collaborative filtering and content-based filtering.
- 🔍 Search: Users can search for movies by title, genres, and other attributes.
- 📊 Data-Driven: Uses real-world movie rating datasets to build recommendation models.
- 💻 Interactive Web Application: Built with Django for the backend and React for the frontend for a responsive user experience.


## Technology Stack
Backend
- **Django: Backend framework.
- **PostgreSQL: Database for user data and movie ratings (used with Heroku).
- **Django Rest Framework (DRF): For building the REST APIs.
- **Scikit-Learn & Pandas: For building machine learning models and handling datasets.
- **Joblib: For model serialization.
- **Gunicorn: WSGI HTTP Server for deploying Django applications.
- **Heroku: Deployment platform.
Frontend
- **React.js: Frontend JavaScript library for building user interfaces.
- **Axios: For making API calls from the frontend to the Django backend.
- **HTML5/CSS3: Styling and layout.


## Datasets
The recommendation system is built on a dataset containing:

- Movies: Movie titles, genres, etc.
- Users: Anonymized user ratings for movies.
- Ratings: Movie rating data (user ID, movie ID, rating, timestamp).
