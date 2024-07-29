import express from "express";
import path from 'path';

const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.sendFile(path.join('/Users/mariafernandamanriquezangeles/Desktop/Escuela/SS/nodeWOmysql/index.html'));
});

app.listen(port, () => {
    console.log(`Server running at port ${port}.`);
});