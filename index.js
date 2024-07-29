import express from 'express';
import mysql from 'mysql2/promise';
import path from 'path';
import ejs from 'ejs';

const app = express();
const port = 3000;

// Configura el motor de plantillas EJS
app.set('view engine', 'ejs');
app.set('views', path.join('/Users/mariafernandamanriquezangeles/Desktop/Escuela/SS/dashboardUAM/', 'views'));

// Conexión a la base de datos
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: '15122121B',
  database: 'covid19'
});

// Ruta para obtener los datos de la base de datos y renderizar la vista
app.get('/', async (req, res) => {
  try {
    const [rows] = await pool.execute('SELECT count(*) as num FROM covid19.caso;');
    res.render('index', { casos: rows });
  } catch (error) {
    console.error('Error al obtener los casos:', error);
    res.status(500).send('Error en el servidor');
  }
});

app.listen(port, () => {
  console.log(`Servidor escuchando en el puerto ${port}`);
});
