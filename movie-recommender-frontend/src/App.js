import React from 'react';
import MovieForm from './MovieForm';
import './App.css'; 

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the Movie Recommender App!</h1>
        {/* Render the MovieForm component */}
        <MovieForm />
      </header>
    </div>
  );
}

export default App;