-- Inserciones de 'profesor'
INSERT INTO profesor (nombre, reconocido, rfid, count)
VALUES ("Profesor Juan Perez", 1, "1234567890", 0),
       ("Profesora Maria Lopez", 1, "9876543210", 0);
-- ---------------------------------------------------
-- Inserciones de 'salon'
INSERT INTO salon (edificio, salon)
VALUES ("Edificio Principal", "Salon 101"),
       ("Edificio Secundario", "Salon 202");
-- ---------------------------------------------------
-- Inserciones de 'condicion'
INSERT INTO condicion (temperatura, humedad, luminosidad)
VALUES (22.5, 55.0, 300.0),
       (24.0, 60.0, 400.0);
-- ----------------------------------------------------
-- Inserciones de 'visita'
INSERT INTO visita (fecha, hora, idsalon, idprofesor, idcondicion)
VALUES (CURDATE(), "10:00:00", 1, 1, 1),  
       (DATE_SUB(CURDATE(), INTERVAL 1 DAY), "11:30:00", 2, 2, 2);
-- ----------------------------------------------------