import React from 'react';
import MovieForm from './MovieForm.js';
import './App.css'; 

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to my Movie Recommender App!</h1>
        <MovieForm />
      </header>
    </div>
  );
}

export default App;