#!/usr/bin/env bash
# Script para inicializar la base de datos en Render
# Ejecutar desde la Shell de Render

set -o errexit

echo "==================================="
echo "  Inicializando base de datos"
echo "==================================="

cd bd_Smartgalpon_api

echo "1. Ejecutando migraciones..."
python manage.py migrate

echo "2. Recolección de archivos estáticos..."
python manage.py collectstatic --noinput

echo "3. Crear superusuario (opcional)..."
read -p "¿Crear superusuario? (s/n): " respuesta
if [ "$respuesta" = "s" ]; then
    python manage.py createsuperuser
fi

echo "==================================="
echo "  ¡Base de datos lista!"
echo "==================================="
