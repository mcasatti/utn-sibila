#!/bin/bash
echo "Detectando servidores:"
echo "======================"
echo "Sibila FastAPI: 8000"
echo "Sibila OrientDB: 2480"
echo "======================"
echo "Resultados"
echo "----------"
netstat -tulpn | grep '8000\|2480'
echo "=========================================="
echo "Direcciones IP de los contenedores Docker:"
echo "=========================================="
echo "OrientDB:"
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' sibila-orientdb
echo "FastAPI"
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' sibila-fastapi
