#!/bin/bash
# Script para crear un paquete de backup de datos desde Named Volume, subirlo a GitHub y reiniciar el entorno local.

echo "======================================================="
echo "    PASO 1: INICIANDO COPIA DE SEGURIDAD LOCAL"
echo "======================================================="

# Nombres según tu último docker-compose.yml
PG_CONTAINER="postgres_dev_vb"             # Nombre del contenedor de Postgres
ODOO_CONTAINER="odoo_dev_vb"               # Nombre del contenedor de Odoo
PG_USER="odoo"                              # Usuario de la BD Postgres
DB_NAME="odoo"                              # Nombre de la BD a respaldar 
BACKUP_DIR="./data/backups"                 # Directorio de backups en el host
BACKUP_SQL="${BACKUP_DIR}/${DB_NAME}.sql"   # Ruta completa del archivo SQL de backup

echo "==> Parando Odoo para garantizar consistencia..."
docker-compose stop "$ODOO_CONTAINER" 2>/dev/null || true

mkdir -p "${BACKUP_DIR}"

# Comprobar que el contenedor de Postgres está up
if ! docker ps --format '{{.Names}}' | grep -q "^${PG_CONTAINER}$"; then
  echo "==> Arrancando Postgres..."
  docker-compose up -d "$PG_CONTAINER"
fi

echo "==> Creando backup lógico (SQL plano) de la BD '${DB_NAME}'..."
# El dump se genera dentro del contenedor y se escribe en el bind mount /backups => ./data/backups del host
docker exec "${PG_CONTAINER}" bash -lc "pg_dump -U '${PG_USER}' -d '${DB_NAME}' --no-owner --no-privileges > '/backups/${DB_NAME}.sql'"
echo "==> Creando backup lógico (SQL plano)..."
echo "Backup completado: ${BACKUP_SQL}"

# Comprimimos el contenido de la carpeta filestore
echo "==> Empaquetando Filestore ..."
tar -czf "${BACKUP_DIR}/filestore.tar.gz" -C ./data/odoo/filestore .
echo "==> Filestore empaquetado..."

echo "==> Arrancando Odoo de nuevo..."
docker compose start ${ODOO_CONTAINER}

echo "FIN"
