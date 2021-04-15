#!/bin/bash
# declare STRING variable
STRING="Iniciando Docker Container (Sibila FastAPI)"
#print variable on a screen
echo $STRING
echo "Iniciando el servidor Python (FastAPI) de Sibila"
docker run -d --rm -p 8000:8000 --hostname sibila-fastapi --name sibila-fastapi mcasatti/sibila-fastapi:latest 
echo "Obteniendo la IP asignada a SIBILA"
sleep 3s
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' sibila-fastapi

