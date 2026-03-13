#!/bin/bash
# Script para preparar y subir el backend a Render

echo "==================================="
echo "  Preparando backend para Render"
echo "==================================="
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml no encontrado"
    echo "   Ejecuta este script desde la carpeta backend_gestor_pollos/"
    exit 1
fi

echo "✅ 1. Verificando archivos necesarios..."

# Verificar archivos
FILES=("render.yaml" "Procfile" ".gitignore" "bd_Smartgalpon_api/requirements.txt" "bd_Smartgalpon_api/manage.py")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file (FALTA)"
        exit 1
    fi
done

echo ""
echo "✅ 2. Creando .env de ejemplo..."

if [ ! -f "bd_Smartgalpon_api/.env.example" ]; then
    cat > bd_Smartgalpon_api/.env.example << EOF
# Variables de entorno para Render
DEBUG=false
SECRET_KEY=tu-secret-key-aqui
DATABASE_URL=postgresql://usuario:password@host:port/database
ALLOWED_HOSTS=*
PYTHON_VERSION=3.9.0
EOF
    echo "   ✓ Creado bd_Smartgalpon_api/.env.example"
else
    echo "   ✓ bd_Smartgalpon_api/.env.example ya existe"
fi

echo ""
echo "✅ 3. Verificando requirements.txt..."
cd bd_Smartgalpon_api
if python -m pip check 2>/dev/null; then
    echo "   ✓ Dependencias OK"
else
    echo "   ⚠ Algunas dependencias pueden faltar"
fi
cd ..

echo ""
echo "✅ 4. Preparando para git..."

# Inicializar git si no existe
if [ ! -d ".git" ]; then
    echo "   📦 Inicializando repositorio git..."
    git init
    git branch -M main
fi

echo ""
echo "==================================="
echo "  📋 Próximos pasos:"
echo "==================================="
echo ""
echo "1. Agrega los archivos a git:"
echo "   git add ."
echo "   git commit -m 'Preparando para Render'"
echo ""
echo "2. Crea un repositorio en GitHub:"
echo "   https://github.com/new"
echo ""
echo "3. Conecta y sube el código:"
echo "   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git"
echo "   git push -u origin main"
echo ""
echo "4. Ve a Render y conecta el repositorio:"
echo "   https://dashboard.render.com/new"
echo ""
echo "5. Agrega las variables de entorno en Render:"
echo "   - DEBUG=false"
echo "   - SECRET_KEY=(genera una en https://djecrety.ir/)"
echo "   - DATABASE_URL=(de tu PostgreSQL en Render)"
echo "   - ALLOWED_HOSTS=*"
echo ""
echo "==================================="
echo "  ¡Listo para desplegar! 🚀"
echo "==================================="
