#!/bin/bash

# Script de configuración inicial para UNPA Coding Games
# Uso: bash setup.sh

set -e  # Detener en caso de error

echo "🎮 UNPA Coding Games - Configuración Inicial 🎮"
echo "==============================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${YELLOW}Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python encontrado: $(python3 --version)${NC}"
echo ""

# Crear entorno virtual
echo -e "${YELLOW}Creando entorno virtual...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}El entorno virtual ya existe. ¿Deseas recrearlo? (s/n)${NC}"
    read -r response
    if [[ "$response" =~ ^([sS][iI]|[sS])$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo -e "${GREEN}✓ Entorno virtual recreado${NC}"
    else
        echo -e "${YELLOW}Usando entorno virtual existente${NC}"
    fi
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
fi
echo ""

# Activar entorno virtual
echo -e "${YELLOW}Activando entorno virtual...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Entorno virtual activado${NC}"
echo ""

# Actualizar pip
echo -e "${YELLOW}Actualizando pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip actualizado${NC}"
echo ""

# Instalar dependencias
echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""

# Configurar .env
echo -e "${YELLOW}Configurando variables de entorno...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    # Generar nueva SECRET_KEY
    NEW_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$NEW_SECRET_KEY/" .env
    echo -e "${GREEN}✓ Archivo .env creado con SECRET_KEY generada${NC}"
else
    echo -e "${YELLOW}.env ya existe, no se modificará${NC}"
fi
echo ""

# Ejecutar migraciones
echo -e "${YELLOW}Ejecutando migraciones de base de datos...${NC}"
python manage.py migrate
echo -e "${GREEN}✓ Migraciones aplicadas${NC}"
echo ""

# Preguntar si crear superusuario
echo -e "${YELLOW}¿Deseas crear un superusuario ahora? (s/n)${NC}"
read -r response
if [[ "$response" =~ ^([sS][iI]|[sS])$ ]]; then
    python manage.py createsuperuser
    echo -e "${GREEN}✓ Superusuario creado${NC}"
fi
echo ""

# Recopilar archivos estáticos
echo -e "${YELLOW}Recopilando archivos estáticos...${NC}"
python manage.py collectstatic --noinput > /dev/null 2>&1 || true
echo -e "${GREEN}✓ Archivos estáticos recopilados${NC}"
echo ""

# Resumen final
echo -e "${GREEN}===============================================${NC}"
echo -e "${GREEN}🎉 Configuración completada exitosamente 🎉${NC}"
echo -e "${GREEN}===============================================${NC}"
echo ""
echo -e "${YELLOW}Para iniciar el servidor:${NC}"
echo -e "  source venv/bin/activate"
echo -e "  python manage.py runserver"
echo ""
echo -e "${YELLOW}Acceder a:${NC}"
echo -e "  🌐 Aplicación: http://127.0.0.1:8000/"
echo -e "  ⚙️  Admin: http://127.0.0.1:8000/admin/"
echo ""
echo -e "${YELLOW}No olvides editar el archivo .env con tus valores específicos${NC}"
echo ""
echo -e "${GREEN}¡Que los juegos comiencen! 🔥${NC}"
