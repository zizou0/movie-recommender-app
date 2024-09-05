import React, { useState } from 'react';
import axios from 'axios';

function MovieRecommender() {
    const [title, setTitle] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [error, setError] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();

        setError('');  // Clear any previous error messages
        setRecommendations([]);  // Clear previous recommendations
        
        // Make a POST request to the Django API
        axios.post('http://127.0.0.1:8000/api/recommend/', { title })
            .then ((response) => {
                if (response.data.recommended_movies.length === 0) {
                    setError('No recommendations found for this movie.');
                } else {
                    setRecommendations(response.data.recommended_movies);  // Set the recommendations state
                }
            })
            .catch((error) => {
                if (error.response && error.response.status === 404) {
                    setError('Movie not yet in our database');  // Custom error message
                } else {
                    console.error('Error fetching recommendations:', error);
                    setError('An error occurred. Please try again later.');  // General error message
                  }
            });

            
    };

    

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Enter movie title"
                />
                <button type="submit">Get Recommendations</button>
            </form>

            {/* Display Error Message if Exists */}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {recommendations.length > 0 && (
                <div>
                    <h2>Recommendations for "{title}"</h2>
                    <ul>
                        {recommendations.map((movie, index) => (
                            <li key={index}>{movie}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default MovieRecommender;
