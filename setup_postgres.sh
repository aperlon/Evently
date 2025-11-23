#!/bin/bash

# Script para configurar PostgreSQL para Evently

echo "========================================="
echo "  Configurando PostgreSQL para Evently"
echo "========================================="
echo ""

# Verificar si PostgreSQL está corriendo
if ! pg_isready > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL no está corriendo"
    echo "   Iniciando PostgreSQL..."
    sudo service postgresql start
    sleep 2
fi

# Intentar crear usuario y base de datos
echo "📦 Creando base de datos y usuario..."

# Opción 1: Intentar con sudo
sudo -u postgres psql <<EOF 2>/dev/null || true
-- Crear usuario si no existe
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'evently') THEN
        CREATE USER evently WITH PASSWORD 'evently123';
    END IF;
END
\$\$;

-- Crear base de datos si no existe
SELECT 'CREATE DATABASE evently OWNER evently'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'evently')\gexec

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE evently TO evently;
\q
EOF

# Opción 2: Si no funciona con sudo, dar instrucciones manuales
if ! psql -U evently -d evently -c "SELECT 1;" > /dev/null 2>&1; then
    echo ""
    echo "⚠️  No se pudo configurar automáticamente"
    echo ""
    echo "Por favor, ejecuta estos comandos manualmente:"
    echo ""
    echo "1. Conecta a PostgreSQL:"
    echo "   sudo -u postgres psql"
    echo ""
    echo "2. Dentro de psql, ejecuta:"
    echo "   CREATE USER evently WITH PASSWORD 'evently123';"
    echo "   CREATE DATABASE evently OWNER evently;"
    echo "   GRANT ALL PRIVILEGES ON DATABASE evently TO evently;"
    echo "   \\q"
    echo ""
    echo "3. Luego ejecuta: ./dev.sh"
    exit 1
fi

echo "✅ Base de datos configurada correctamente"
echo ""
echo "Ahora puedes ejecutar: ./dev.sh"

