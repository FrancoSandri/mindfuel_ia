import React, { useState } from 'react';

function App() {
  const [recomendacion, setRecomendacion] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('/recomendar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tareas: event.target.tareas.value }),
      });

      if (!response.ok) {
        throw new Error('Error en la solicitud');
      }

      const data = await response.json();
      setRecomendacion(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="recomendar">
      <h2>Recomendar tareas</h2>
      <p>Introduce el nombre de la tarea</p>
      <form onSubmit={handleSubmit}>
        <input type="text" name="tareas" placeholder="Tarea" required />
        <button type="submit" className="btn btn-primary btn-block btn-large">
          Recomendar
        </button>
      </form>
      <ul>
        {recomendacion.map((item, index) => (
          <li key={index}>{item.Tareas}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;