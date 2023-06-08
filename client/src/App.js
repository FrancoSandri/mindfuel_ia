import React, { useState } from 'react';

function App() {
  const [recomendacion, setRecomendacion] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(event.target.tareas.value)
    try {
      const formData = new FormData();
      formData.append('tareas', event.target.tareas.value);

      const response = await fetch('http://127.0.0.1:5000/recomendar', {
        method: 'POST',
        body: formData,
      });
    
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setRecomendacion(data);
      } else {
        console.log('Error:', response.status);
      }

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