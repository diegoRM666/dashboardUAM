USE sensor;

-- Insert sample data into profesor table
INSERT INTO profesor (nombre, reconocido, rfid, count)
VALUES
  ('Profesor 1', 1, 'RFID123', 5),
  ('Profesor 2', 0, 'RFID456', 3),
  ('Profesor 3', 1, 'RFID789', 8);

-- Insert sample data into salon table
INSERT INTO salon (edificio, salon)
VALUES
  ('A', '101'),
  ('B', '202'),
  ('C', '303');

-- Insert sample data into condicion table
INSERT INTO condicion (temperatura, humedad, luminosidad, timestamp, idsalon)
VALUES
  (22.5, 45, 80, NOW(), 1),
  (25, 50, 75, NOW(), 2),
  (20, 35, 90, NOW(), 3);

-- Insert sample data into visita table
INSERT INTO visita (fecha, hora, idsalon, idprofesor)
VALUES
  ('2023-11-15', '10:30', 1, 1),
  ('2023-11-16', '12:00', 2, 2),
  ('2023-11-17', '14:15', 3, 3);

-- Insert sample data into preferencias_atmosfericas table
INSERT INTO preferencias_atmosfericas (temperatura, humedad, luminosidad, idprofesor)
VALUES
  (23, 40, 85, 1),
  (24, 55, 70, 2),
  (21, 38, 92, 3);
