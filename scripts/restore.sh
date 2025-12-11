
#!/bin/bash
# Restauración segura de la BD Odoo desde un dump SQL plano (nombre fijo)
# Funciona tanto si los servicios estaban en 'stop' como si se hizo 'down' antes.

PG_CONTAINER="postgres_dev_dam"             # Nombre del contenedor de Postgres
ODOO_CONTAINER="odoo_dev_dam"               # Nombre del contenedor de Odoo
PG_USER="odoo"                              # Usuario de la BD Postgres
DB_NAME="odoo"                              # Nombre de la BD a respaldar 
BACKUP_DIR="./data/backups"                 # Directorio de backups en el host
BACKUP_SQL="${BACKUP_DIR}/${DB_NAME}.sql"   # Ruta completa del archivo SQL de backup



echo "======================================================="
echo " INICIANDO RESTAURACIÓN SEGURA"
echo "======================================================="

# 1) Validar backup
if [[ ! -f "${BACKUP_SQL}" ]]; then
  echo "ERROR: No se encontró ${BACKUP_SQL}"
  exit 1
fi

# 2) Parar Odoo (si existe)
echo "==> Parando Odoo..."
docker compose stop "${ODOO_CONTAINER}" 2>/dev/null || true

# 3) Levantar Postgres (cubre caso 'down')
echo "==> Levantando Postgres..."
docker compose up -d "${PG_CONTAINER}"

# 4) Esperar readiness de Postgres
echo "==> Esperando a que Postgres acepte conexiones..."
until docker exec "${PG_CONTAINER}" pg_isready -U "${PG_USER}" >/dev/null 2>&1; do
  echo "   -> Postgres arrancando, reintentando en 2s..."
  sleep 2
done
echo "Postgres listo."

# 5) Eliminar BD y recrear
echo "==> Eliminando BD '${DB_NAME}' si existe..."
docker exec "${PG_CONTAINER}" bash -lc "dropdb -U '${PG_USER}' --if-exists '${DB_NAME}'"
echo "==> Creando BD '${DB_NAME}'..."
docker exec "${PG_CONTAINER}" bash -lc "createdb -U '${PG_USER}' '${DB_NAME}'"

# 6) Restaurar datos
echo "==> Restaurando datos desde ${BACKUP_SQL}..."
# Borra exactamente las líneas de meta-comandos (con token alfanumérico)
sed -E '/^\\restrict [A-Za-z0-9]+$/d;/^\\unrestrict [A-Za-z0-9]+$/d'  "${BACKUP_SQL}" > "${BACKUP_SQL%.sql}.clean.sql"
docker exec -i "${PG_CONTAINER}" psql -U "${PG_USER}" -d "${DB_NAME}" -v ON_ERROR_STOP=on \ < "${BACKUP_SQL%.sql}.clean.sql"
echo "Restauración completada."

# 7) Espera fija antes de arrancar Odoo
echo "==> Esperando 1 segundo antes de arrancar Odoo..."
sleep 1

# 8) Levantar Odoo (si falla, se hace manual)
echo "==> Levantando Odoo..."
docker compose up -d "${ODOO_CONTAINER}"

echo "======================================================="
echo " RESTAURACIÓN COMPLETA. Accede a: http://localhost:8069"
echo "======================================================="
