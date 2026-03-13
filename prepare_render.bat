@echo off
REM Script para preparar y subir el backend a Render (Windows)

echo ===================================
echo   Preparando backend para Render
echo ===================================
echo.

REM Verificar si estamos en el directorio correcto
if not exist "render.yaml" (
    echo Error: render.yaml no encontrado
    echo    Ejecuta este script desde la carpeta backend_gestor_pollos\
    pause
    exit /b 1
)

echo OK 1. Verificando archivos necesarios...

REM Verificar archivos
if exist "render.yaml" (echo    [OK] render.yaml) else (echo    [FALTA] render.yaml ^& exit /b 1)
if exist "Procfile" (echo    [OK] Procfile) else (echo    [FALTA] Procfile ^& exit /b 1)
if exist ".gitignore" (echo    [OK] .gitignore) else (echo    [FALTA] .gitignore ^& exit /b 1)
if exist "bd_Smartgalpon_api\requirements.txt" (echo    [OK] bd_Smartgalpon_api\requirements.txt) else (echo    [FALTA] bd_Smartgalpon_api\requirements.txt ^& exit /b 1)
if exist "bd_Smartgalpon_api\manage.py" (echo    [OK] bd_Smartgalpon_api\manage.py) else (echo    [FALTA] bd_Smartgalpon_api\manage.py ^& exit /b 1)

echo.
echo OK 2. Creando .env de ejemplo...

if not exist "bd_Smartgalpon_api\.env.example" (
    (
        echo # Variables de entorno para Render
        echo DEBUG=false
        echo SECRET_KEY=tu-secret-key-aqui
        echo DATABASE_URL=postgresql://usuario:password@host:port/database
        echo ALLOWED_HOSTS=*
        echo PYTHON_VERSION=3.9.0
    ) > "bd_Smartgalpon_api\.env.example"
    echo    Creado bd_Smartgalpon_api\.env.example
) else (
    echo    bd_Smartgalpon_api\.env.example ya existe
)

echo.
echo OK 3. Verificando git...

if not exist ".git" (
    echo    Inicializando repositorio git...
    git init
    git branch -M main
) else (
    echo    Repositorio git ya existe
)

echo.
echo ===================================
echo   Próximos pasos:
echo ===================================
echo.
echo 1. Agrega los archivos a git:
echo    git add .
echo    git commit -m "Preparando para Render"
echo.
echo 2. Crea un repositorio en GitHub:
echo    https://github.com/new
echo.
echo 3. Conecta y sube el código:
echo    git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
echo    git push -u origin main
echo.
echo 4. Ve a Render y conecta el repositorio:
echo    https://dashboard.render.com/new
echo.
echo 5. Agrega las variables de entorno en Render:
echo    - DEBUG=false
echo    - SECRET_KEY=^((genera una en https://djecrety.ir/^))
echo    - DATABASE_URL=^((de tu PostgreSQL en Render^))
echo    - ALLOWED_HOSTS=*
echo.
echo ===================================
echo   ¡Listo para desplegar!
echo ===================================
echo.
pause
