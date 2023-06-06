import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchRecomendar();
  }, []);

  const fetchRecomendar = async () => {
    try {
      const response = await fetch('/recomendar', {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Error en la solicitud');
      }

      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <div className="recomendar">
        <h2>Recomendar tareas</h2>
        <p>Introduce el nombre de la tarea</p>
        <form action="/recomendar" method="post">
          <input type="text" name="tareas" placeholder="Tarea" required />
          <button type="submit" className="btn btn-primary btn-block btn-large">
            Recomendar
          </button>
        </form>
      </div>
      <div>{JSON.stringify(data)}</div>
    </>
  );
}

export default App;