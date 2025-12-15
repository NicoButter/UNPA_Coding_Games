#!/bin/bash
# Script de verificación rápida del sistema de juez
# Ejecutar: bash judge_quick_check.sh

echo "========================================="
echo "UNPA Coding Games - Verificación de Juez"
echo "========================================="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar comandos
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 instalado"
        return 0
    else
        echo -e "${RED}✗${NC} $1 NO encontrado"
        return 1
    fi
}

# 1. Verificar Python
echo "1. Verificando Python..."
check_command python3
python3 --version
echo ""

# 2. Verificar Docker
echo "2. Verificando Docker..."
check_command docker
if command -v docker &> /dev/null; then
    docker --version
    
    # Verificar si Docker está corriendo
    if docker ps &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker está corriendo"
    else
        echo -e "${RED}✗${NC} Docker NO está corriendo"
        echo "   Ejecutar: sudo systemctl start docker"
    fi
else
    echo "   Instalar con: sudo dnf install docker"
fi
echo ""

# 3. Verificar imágenes Docker
echo "3. Verificando imágenes Docker..."
if command -v docker &> /dev/null && docker ps &> /dev/null; then
    echo "   Buscando imágenes necesarias..."
    
    if docker images | grep -q "python.*3.11-slim"; then
        echo -e "   ${GREEN}✓${NC} python:3.11-slim"
    else
        echo -e "   ${RED}✗${NC} python:3.11-slim (no descargada)"
        echo "      Descargar: docker pull python:3.11-slim"
    fi
    
    if docker images | grep -q "openjdk.*17-slim"; then
        echo -e "   ${GREEN}✓${NC} openjdk:17-slim"
    else
        echo -e "   ${RED}✗${NC} openjdk:17-slim (no descargada)"
        echo "      Descargar: docker pull openjdk:17-slim"
    fi
    
    if docker images | grep -q "node.*18-slim"; then
        echo -e "   ${GREEN}✓${NC} node:18-slim"
    else
        echo -e "   ${RED}✗${NC} node:18-slim (no descargada)"
        echo "      Descargar: docker pull node:18-slim"
    fi
fi
echo ""

# 4. Verificar archivos del proyecto
echo "4. Verificando archivos del proyecto..."
files=(
    "judge/__init__.py"
    "judge/models.py"
    "judge/views.py"
    "judge/runner.py"
    "judge/docker_executor.py"
    "judge/templates/python.py"
    "judge/templates/java.java"
    "judge/templates/js.js"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   ${GREEN}✓${NC} $file"
    else
        echo -e "   ${RED}✗${NC} $file (falta)"
    fi
done
echo ""

# 5. Verificar dependencias Python
echo "5. Verificando dependencias Python..."
if python3 -c "import django" 2>/dev/null; then
    echo -e "   ${GREEN}✓${NC} Django instalado"
else
    echo -e "   ${RED}✗${NC} Django NO instalado"
    echo "      Instalar: pip install -r requirements.txt"
fi

if python3 -c "import docker" 2>/dev/null; then
    echo -e "   ${GREEN}✓${NC} docker (Python) instalado"
else
    echo -e "   ${RED}✗${NC} docker (Python) NO instalado"
    echo "      Instalar: pip install docker"
fi
echo ""

# 6. Verificar migraciones
echo "6. Verificando migraciones..."
if [ -f "judge/migrations/0001_initial.py" ]; then
    echo -e "   ${GREEN}✓${NC} Migraciones creadas"
else
    echo -e "   ${YELLOW}⚠${NC} Migraciones no creadas"
    echo "      Ejecutar: python manage.py makemigrations judge"
fi
echo ""

# 7. Verificar base de datos
echo "7. Verificando base de datos..."
if [ -f "db.sqlite3" ]; then
    echo -e "   ${GREEN}✓${NC} Base de datos existe"
    
    # Verificar si las tablas existen
    if python3 manage.py showmigrations judge 2>/dev/null | grep -q "\[X\]"; then
        echo -e "   ${GREEN}✓${NC} Migraciones aplicadas"
    else
        echo -e "   ${YELLOW}⚠${NC} Migraciones no aplicadas"
        echo "      Ejecutar: python manage.py migrate"
    fi
else
    echo -e "   ${RED}✗${NC} Base de datos no existe"
    echo "      Ejecutar: python manage.py migrate"
fi
echo ""

# Resumen
echo "========================================="
echo "RESUMEN"
echo "========================================="
echo ""
echo "Para completar la instalación:"
echo ""
echo "1. Si Docker no está instalado:"
echo "   sudo dnf install docker"
echo "   sudo systemctl start docker"
echo "   sudo usermod -aG docker \$USER"
echo ""
echo "2. Instalar dependencias Python:"
echo "   pip install -r requirements.txt"
echo ""
echo "3. Descargar imágenes Docker:"
echo "   docker pull python:3.11-slim"
echo "   docker pull openjdk:17-slim"
echo "   docker pull node:18-slim"
echo ""
echo "4. Crear y aplicar migraciones:"
echo "   python manage.py makemigrations arena judge"
echo "   python manage.py migrate"
echo ""
echo "5. Probar el sistema:"
echo "   python manage.py shell"
echo "   >>> from judge.management_utils import test_judge_system"
echo "   >>> test_judge_system()"
echo ""
echo "Para más información:"
echo "   - Ver docs/JUDGE_MIGRATION.md"
echo "   - Ver judge/README.md"
echo "   - Ver JUDGE_IMPLEMENTATION_SUMMARY.md"
echo ""
