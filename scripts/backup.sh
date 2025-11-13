#!/bin/bash
# Script para crear un paquete de backup de datos, subirlo a GitHub y reiniciar el entorno local.

echo "======================================================="
echo "    PASO 1: INICIANDO COPIA DE SEGURIDAD LOCAL"
echo "======================================================="

# Definimos la ruta del paquete para facilitar la actualización
PKG_PATH="data/backups/odoo_data_package.tar.gz"

# 1. Detener los servicios para garantizar la integridad de los datos
echo "-> Deteniendo contenedores..."
docker-compose stop

# 2. Aseguramos que la carpeta de destino exista
mkdir -p data/backups

# 3. Eliminar cualquier paquete anterior en la nueva ubicación
rm -f $PKG_PATH

# 4. Empaquetar los datos persistentes (PostgreSQL, Filestore, Sessions)
echo "-> Empaquetando volúmenes de datos en $PKG_PATH..."
tar -czvf $PKG_PATH \
    data/dataPostgreSQL \
    data/odoo/filestore \
    data/odoo/sessions

# 5. Iniciar los contenedores inmediatamente para continuar el trabajo
echo "-> Iniciando contenedores de nuevo para continuar el trabajo..."
docker-compose start

echo "Copia de seguridad local completada y entorno reiniciado."

echo "======================================================="
echo "    PASO 2: SUBIENDO CAMBIOS A GITHUB"
echo "======================================================="

# 6. Añadir archivos al staging
echo "-> Añadiendo el nuevo paquete de datos y todos los cambios de código a Git..."
# Añade el paquete y cualquier cambio en addons, odoo.conf o docker-compose.yml
git add $PKG_PATH .

# 7. Realizar el commit
FECHA_BACKUP=$(date +"%Y-%m-%d %H:%M:%S")
echo "-> Creando commit..."
git commit -m "BACKUP AUTOMÁTICO - Datos y código actualizados al $FECHA_BACKUP"

# 8. Subir a GitHub
echo "-> Subiendo a GitHub (rama main)..."
git push origin main

if [ $? -eq 0 ]; then
    echo "======================================================="
    echo " ¡ÉXITO! COPIA DE SEGURIDAD Y SUBIDA COMPLETADAS."
    echo "======================================================="
else
    echo "======================================================="
    echo " ERROR: FALLÓ LA SUBIDA A GITHUB."
    echo "======================================================="
fi