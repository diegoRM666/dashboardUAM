#!/bin/bash

# Cambiar al directorio del proyecto
cd /home/mrcubeoner/Desktop/DashboardUAM/dashboardUAM || { echo "Error: No se puede acceder a /home/mrcubeoner/Desktop/DashboardUAM/dashboardUAM"; exit 1; }

# Agregar cambios
git add .

# Pedir al usuario el mensaje del commit
echo "Ingrese el mensaje del commit:"
read -r mensaje

# Obtener la fecha y hora actuales en el formato deseado
fecha_hora=$(date +"%Y-%m-%d-%H:%M")

# Crear el commit con el mensaje personalizado
git commit -m "U-${fecha_hora}:${mensaje}"

# Hacer push al repositorio
git push

