import mysql from 'mysql2/promise';

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: '15122121B',
  database: 'covid19'
});

async function obtenerCasosCovid() {
  try {
    const [rows] = await pool.execute('SELECT * FROM caso limit 2');
    return rows;
  } catch (error) {
    console.error('Error al obtener los casos:', error);
    return []; // Or handle the error differently
  }
}

// Export the function for access from other files
export default obtenerCasosCovid;


