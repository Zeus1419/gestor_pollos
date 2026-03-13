# 🚀 Backend - SmartGalpon API

Backend Django para la aplicación de gestión de galpones de pollos.

## 📁 Estructura del proyecto

```
backend_gestor_pollos/
├── bd_Smartgalpon_api/       # Directorio principal de Django
│   ├── api/                  # Aplicación principal
│   ├── bd_Smartgalpon/       # Configuración del proyecto
│   ├── manage.py             # Script de gestión de Django
│   ├── requirements.txt      # Dependencias
│   └── .env.example          # Ejemplo de variables de entorno
├── render.yaml               # Configuración para Render
├── Procfile                  # Comando de inicio
├── .gitignore                # Archivos ignorados
├── prepare_render.bat        # Script Windows para preparar despliegue
├── prepare_render.sh         # Script Linux/Mac para preparar despliegue
└── DEPLOY_RENDER.md          # Guía completa de despliegue
```

## 🛠️ Desarrollo local

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/backend-gestor-pollos.git
cd backend_gestor_pollos
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
cd bd_Smartgalpon_api
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus variables
```

### 5. Ejecutar migraciones
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Iniciar servidor
```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/api`

---

## 🚀 Despliegue en Render

### Opción rápida (Windows)
```bash
# Ejecutar script de preparación
prepare_render.bat

# Seguir las instrucciones en pantalla
```

### Pasos manuales

1. **Subir a GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **Crear Web Service en Render**
   - Ve a https://dashboard.render.com/new
   - Conecta tu repositorio de GitHub
   - Render detectará automáticamente el `render.yaml`

3. **Configurar variables de entorno**
   | Clave | Valor |
   |-------|-------|
   | `DEBUG` | `false` |
   | `SECRET_KEY` | (genera en https://djecrety.ir/) |
   | `DATABASE_URL` | (de tu PostgreSQL en Render) |
   | `ALLOWED_HOSTS` | `*` |

4. **Crear base de datos PostgreSQL**
   - New + → PostgreSQL
   - Copia el Internal Database URL
   - Pega en `DATABASE_URL`

5. **Ejecutar migraciones**
   ```bash
   cd bd_Smartgalpon_api
   python manage.py migrate
   python manage.py createsuperuser
   ```

📖 **Guía completa**: Ver `DEPLOY_RENDER.md`

---

## 🔑 Endpoints principales

### Autenticación
- `POST /api/auth/register/` - Registrar usuario
- `POST /api/auth/login/` - Iniciar sesión
- `GET /api/auth/profile/` - Obtener perfil

### Lotes (Engorde)
- `GET /api/lotes/` - Listar lotes
- `POST /api/crearLote/` - Crear lote
- `GET /api/detalleLote/{id}/` - Detalle de lote
- `DELETE /api/eliminarLote/{id}/` - Eliminar lote

### Insumos
- `POST /api/agregarInsumo/` - Agregar insumo
- `DELETE /api/eliminarInsumo/{id}/` - Eliminar insumo

### Pesos
- `POST /api/registrarPeso/` - Registrar peso

### Mortalidad
- `GET /api/historialMortalidad/{loteId}/` - Historial
- `POST /api/registrarMortalidad/` - Registrar mortalidad

### Ponedoras
- `GET /api/ponedoras/lotesPonedoras/` - Listar lotes
- `POST /api/ponedoras/crearLotePonedora/` - Crear lote
- `POST /api/ponedoras/registroHuevos/` - Registrar huevos
- `GET /api/ponedoras/resumenGanancias/{loteId}/` - Ganancias

---

## 🔧 Tecnologías

- **Framework**: Django 4.2
- **API**: Django REST Framework 3.16
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **Base de datos**: PostgreSQL (Render) / MySQL (local)
- **Servidor**: Gunicorn
- **Static files**: WhiteNoise

---

## 📝 Variables de entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `DEBUG` | Modo debug (True/False) | Sí |
| `SECRET_KEY` | Clave secreta de Django | Sí |
| `DATABASE_URL` | URL de conexión a BD | Sí |
| `ALLOWED_HOSTS` | Hosts permitidos | No (default: *) |
| `PYTHON_VERSION` | Versión de Python | No (default: 3.9.0) |

---

## 🧪 Probar la API

### Con curl
```bash
# Listar lotes
curl https://tu-api.onrender.com/api/lotes/

# Login
curl -X POST https://tu-api.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"tu_usuario","password":"tu_password"}'
```

### Con Postman
1. Importa la colección desde `pruebasPostman.txt`
2. Configura la URL base
3. Ejecuta las peticiones

---

## ⚠️ Notas importantes

1. **Plan gratuito de Render**: El servidor se duerme después de 15 min de inactividad
2. **Primera petición**: Puede tardar 30-50 segundos después de inactivo
3. **Base de datos**: El plan free de Render dura 90 días

---

## 📞 Soporte

Para problemas o preguntas:
1. Revisa los logs en Render
2. Verifica las variables de entorno
3. Ejecuta `python manage.py check --deploy`

---

## 📄 Licencia

MIT
