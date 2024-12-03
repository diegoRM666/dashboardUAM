#!/bin/bash

# Detectar el sistema operativo y establecer la ruta del proyecto
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ruta_proyecto="/home/mrcubeoner/Desktop/DashboardUAM/dashboardUAM"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    ruta_proyecto="/Users/diegoruiz/Desktop/DashboardUAM/dashboardUAM"
else
    echo "Error: Sistema operativo no soportado"
    exit 1
fi

# Cambiar al directorio del proyecto
cd "$ruta_proyecto" || { echo "Error: No se puede acceder a $ruta_proyecto"; exit 1; }

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

