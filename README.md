# Lenguajes
Nombre: Nicolás Torandell Ballesteros
Entrenamientos de LoL
Análisis de entrenamientos de campeones de LoL

Descripción

Este programa en Python permite analizar registros de entrenamientos de campeones de League of Legends a partir de un archivo CSV
Genera estadísticas sobre:
- Días de la semana con más entrenamientos
- Período total de registros
- Campeón que más entrenó y el que más entreno el fin de semana
- Promedio de entrenamientos por día de la semana

Archivos de salida:
- CSV con cantidad de entrenamientos por campeón
- JSON con resumen detallado por día de la semana y campeones

Requisitos
- Python 3.x
- Módulos estándar: csv, json, pathlib, datetime
(No requiere instalación adicional)

Archivos
- actividad_2.csv → Archivo de entrada con los registros de entrenamiento
- Entrenamientos_LoL.py → Script principal del programa

Carpeta salida/ → Contendrá los archivos generados:
- entrenamientos.csv
- resumen_entrenamientos.json

Cómo ejecutar
-Descargar el repositorio en tu computadora
- Asegurarse de tener el archivo CSV actividad_2.csv en la misma carpeta que el script
- Abrir una terminal o CMD y moverse a la carpeta del proyecto
- Ejecutar el script con Python:
     python Entrenamientos_LoL.py

El programa mostrará estadísticas en pantalla y generará los archivos en la carpeta salida/

El programa permite visualizar y analizar la actividad de entrenamientos de campeones de forma rápida y completa
Se pueden ver patrones por día, identificar campeones más activos y generar archivos de salida
