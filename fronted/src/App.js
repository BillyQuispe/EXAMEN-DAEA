import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [skill, setSkill] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const fetchRecommendations = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/recomendacion/${skill}`);
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  return (
    <div className="App">
      <h1>Recomendador de Habilidades</h1>
      <input
        type="text"
        value={skill}
        onChange={(e) => setSkill(e.target.value)}
        placeholder="Ingrese una habilidad"
      />
      <button onClick={fetchRecommendations}>Buscar</button>

      <div>
        <h2>Recomendaciones</h2>
        <ul>
          {recommendations.map((rec, index) => (
            <li key={index}>
              <strong>Usuario:</strong> {rec.Usuario} <br />
              <strong>Habilidad:</strong> {rec.Skill} <br />
              <strong>Puntuación:</strong> {rec.Puntuacion}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
