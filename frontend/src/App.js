import React, { useState } from 'react';
import axios from 'axios';
import './App.css';  // Importar el archivo CSS

const skills = [
  { id: 1, name: "Backend_Programming", spanish: "Programación Backend" },
  { id: 2, name: "Frontend_Programming", spanish: "Programación Frontend" },
  { id: 3, name: "Mobile_Programming", spanish: "Programación Móvil" },
  { id: 4, name: "Graphic_Design", spanish: "Diseño Gráfico" },
  { id: 5, name: "Project_Management", spanish: "Gestión de Proyectos" },
  { id: 6, name: "Service_Management", spanish: "Gestión de Servicios" },
  { id: 7, name: "Data_Analysis", spanish: "Análisis de Datos" },
  { id: 8, name: "Digital_Marketing", spanish: "Marketing Digital" },
  { id: 9, name: "Artificial_Intelligence", spanish: "Inteligencia Artificial" },
  { id: 10, name: "Cybersecurity", spanish: "Ciberseguridad" },
  { id: 11, name: "Machine_Learning", spanish: "Aprendizaje Automático" },
  { id: 12, name: "Deep_Learning", spanish: "Aprendizaje Profundo" },
  { id: 13, name: "Computer_Vision", spanish: "Visión por Computadora" },
  { id: 14, name: "Natural_Language_Processing", spanish: "Procesamiento del Lenguaje Natural" },
  { id: 15, name: "Cloud_Computing", spanish: "Computación en la Nube" },
  { id: 16, name: "DevOps", spanish: "DevOps" },
  { id: 17, name: "Database_Administration", spanish: "Administración de Bases de Datos" },
  { id: 18, name: "Networking", spanish: "Redes" },
  { id: 19, name: "Software_Architecture", spanish: "Arquitectura de Software" },
  { id: 20, name: "UI_UX_Design", spanish: "Diseño UI/UX" },
  { id: 21, name: "Blockchain_Technology", spanish: "Tecnología Blockchain" },
  { id: 22, name: "Big_Data", spanish: "Big Data" },
  { id: 23, name: "IoT_Development", spanish: "Desarrollo IoT" },
  { id: 24, name: "Game_Development", spanish: "Desarrollo de Videojuegos" },
  { id: 25, name: "Quality_Assurance", spanish: "Aseguramiento de Calidad" },
  { id: 26, name: "Business_Analysis", spanish: "Análisis de Negocios" },
  { id: 27, name: "IT_Support", spanish: "Soporte IT" },
  { id: 28, name: "System_Administration", spanish: "Administración de Sistemas" },
  { id: 29, name: "Information_Security", spanish: "Seguridad de la Información" },
  { id: 30, name: "Enterprise_Architecture", spanish: "Arquitectura Empresarial" },
];

function App() {
  const [recommendations, setRecommendations] = useState([]);

  const fetchRecommendations = async (skill) => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/recomendacion/${skill}`);
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  const getSpanishSkill = (skillName) => {
    const skill = skills.find(skill => skill.name === skillName);
    return skill ? skill.spanish : skillName;
  };

  return (
    <div className="App">
      <h1>Recomendador de Habilidades</h1>
      <div className="skills-grid">
        {skills.map((skill) => (
          <div
            key={skill.id}
            className="skill-card"
            onClick={() => fetchRecommendations(skill.name)}
          >
            {skill.spanish}
          </div>
        ))}
      </div>
      <div className="recommendations">
        <h2>Recomendaciones</h2>
        <div className="recommendation-cards">
          {recommendations.map((rec, index) => (
            <div key={index} className="recommendation-card">
              <strong className="user-name">{rec.Usuario.replace(/_/g, ' ')}</strong>
              <p className="user-skill">{getSpanishSkill(rec.Skill)}</p>
              <p className="user-score">{rec.Puntuacion}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
