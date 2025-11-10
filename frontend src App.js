import React from 'react';
import Dashboard from './Dashboard';

function App() {
  return (
    <div className="App">
      <header style={{ padding: '20px', background: '#282c34' }}>
        <h1 style={{ color: 'white' }}>EcoSenseAI Dashboard</h1>
      </header>
      <Dashboard />
    </div>
  );
}

export default App;