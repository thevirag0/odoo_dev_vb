#!/bin/bash
# Script para crear un paquete de backup de datos y código

echo "========================================"
echo "     INICIANDO COPIA DE SEGURIDAD       "
echo "========================================"

# 1. Detener los servicios para garantizar la integridad de los datos
echo "Deteniendo contenedores..."
docker-compose stop

# 2. Eliminar cualquier paquete anterior
rm -f odoo_data_package.tar.gz

# 3. Empaquetar los datos persistentes (PostgreSQL, Filestore, Sessions)
echo "Empaquetando volúmenes de datos..."
tar -czvf odoo_data_package.tar.gz \
    data/dataPostgreSQL \
    data/odoo/filestore \
    data/odoo/sessions

# 4. Limpiar las carpetas de datos en crudo para evitar commit accidental
echo "Limpiando carpetas de datos en crudo..."
rm -rf data/dataPostgreSQL data/odoo/filestore data/odoo/sessions

echo "Copia de seguridad de datos finalizada: odoo_data_package.tar.gz creado en la raíz del proyecto."
echo "========================================"
echo " PASO SIGUIENTE: git add . && git commit && git push"
echo "========================================"