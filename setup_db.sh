#!/bin/bash
# Script para configurar PostgreSQL sin necesidad de contraseña interactiva

echo "=== Configurando base de datos evently ==="

# Intentar crear base de datos usando diferentes métodos
if sudo -n true 2>/dev/null; then
    # Si tenemos sudo sin contraseña
    sudo -u postgres psql <<EOF
CREATE DATABASE evently;
CREATE USER evently WITH PASSWORD 'evently123';
GRANT ALL PRIVILEGES ON DATABASE evently TO evently;
ALTER USER evently CREATEDB;
\q
EOF
else
    # Intentar con el usuario actual si tiene permisos
    createdb evently 2>/dev/null || echo "No se pudo crear la base de datos automáticamente"
    echo "Por favor ejecuta manualmente:"
    echo "sudo -u postgres psql"
    echo "CREATE DATABASE evently;"
    echo "CREATE USER evently WITH PASSWORD 'evently123';"
    echo "GRANT ALL PRIVILEGES ON DATABASE evently TO evently;"
fi

echo "✅ Base de datos configurada (o instrucciones mostradas)"

