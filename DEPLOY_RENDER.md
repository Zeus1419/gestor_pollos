# 🚀 Guía de Despliegue - Backend en Render

## ✅ Archivos configurados para Render

Tu proyecto ya está configurado con:
- ✅ `render.yaml` - Configuración del servicio web
- ✅ `Procfile` - Comando de inicio
- ✅ `.gitignore` - Archivos ignorados
- ✅ `requirements.txt` - Dependencias
- ✅ `settings.py` - Configuración Django para producción

---

## 📋 Pasos para desplegar en Render

### **Opción 1: Despliegue automático con GitHub (Recomendado)**

#### 1. Subir tu código a GitHub
```bash
cd C:\Users\Pc\Desktop\Gestion pollo\backend_gestor_pollos

# Inicializar repositorio (si no existe)
git init

# Agregar todos los archivos
git add .

# Crear primer commit
git commit -m "Initial commit - Backend SmartGalpon para Render"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/backend-gestor-pollos.git
git branch -M main
git push -u origin main
```

#### 2. Conectar Render con GitHub
1. Ve a https://render.com e inicia sesión
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio `backend-gestor-pollos`
5. Render detectará automáticamente el `render.yaml`

#### 3. Configurar variables de entorno en Render
En el dashboard de Render, ve a **Environment** y agrega:

| Clave | Valor |
|-------|-------|
| `DEBUG` | `false` |
| `SECRET_KEY` | (genera una segura en https://djecrety.ir/) |
| `DATABASE_URL` | (la obtendrás de Render Database) |
| `ALLOWED_HOSTS` | `*` |
| `PYTHON_VERSION` | `3.9.0` |

#### 4. Crear base de datos PostgreSQL en Render
1. En Render, ve a **"New +"** → **"PostgreSQL"**
2. Configura:
   - Name: `smartgalpon-db`
   - Database: `smartgalpon`
   - Plan: **Free**
3. Click en **"Create Database"**
4. Copia el **Internal Database URL**
5. Pega el URL en la variable `DATABASE_URL` de tu Web Service

#### 5. Ejecutar migraciones
En la consola de Render (Shell):
```bash
cd bd_Smartgalpon_api
python manage.py migrate
python manage.py createsuperuser
```

#### 6. ¡Listo!
Render desplegará automáticamente tu API en:
```
https://smartgalpon-api.onrender.com
```

---

### **Opción 2: Despliegue manual (Sin GitHub)**

#### 1. Crear Web Service desde cero
1. Ve a https://render.com
2. **New +** → **Web Service**
3. Configura:
   - **Name**: `smartgalpon-api`
   - **Region**: Elige la más cercana (ej: Oregon)
   - **Branch**: main
   - **Root Directory**: `bd_Smartgalpon_api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn bd_Smartgalpon.wsgi:application`

#### 2. Agregar variables de entorno
Igual que en la Opción 1.

#### 3. Crear PostgreSQL
Igual que en la Opción 1.

---

## 🔧 Configuración de la API en Flutter

Una vez desplegado, actualiza tu app Flutter:

### `lib/config/api_config.dart`
```dart
static const String baseUrlProduccion = 
    'https://smartgalpon-api.onrender.com/api';

// Para producción
static String get baseUrl => baseUrlProduccion;
```

### `lib/services/auth_service.dart`
```dart
static const String _baseUrl = 'https://smartgalpon-api.onrender.com';
```

---

## 🧪 Probar la API desplegada

### 1. Verificar que el servidor responde
```bash
curl https://smartgalpon-api.onrender.com/api/lotes/
```

### 2. Probar endpoints desde Postman
- Base URL: `https://smartgalpon-api.onrender.com/api`
- Agrega header: `Authorization: Bearer <tu_token>`

---

## ⚠️ Notas importantes

### 1. El plan gratuito de Render tiene "spin down"
- Después de 15 minutos de inactividad, el servidor se duerme
- La primera petición después de inactivo tarda ~30-50 segundos
- Las siguientes peticiones son rápidas (~200ms)

### 2. Para mantener el servidor activo (opcional)
Usa un servicio como:
- https://cron-job.org (pings gratuitos cada 5 min)
- https://uptimerobot.com (monitoreo gratuito)

### 3. Base de datos
- Render PostgreSQL free tier: 90 días, 1GB
- Alternativa gratuita permanente: **Supabase** o **Neon**

---

## 🐛 Solución de problemas

### Error: "ModuleNotFoundError: No module named 'X'"
```bash
# Verifica que requirements.txt esté en la raíz del repo
# O actualiza el buildCommand en render.yaml
```

### Error: "Database not configured"
```bash
# Verifica que DATABASE_URL esté en las variables de entorno
# Ejecuta las migraciones nuevamente
python manage.py migrate
```

### Error: "Allowed Hosts"
```python
# Agrega tu dominio de Render a ALLOWED_HOSTS en settings.py
'*.onrender.com',
'smartgalpon-api.onrender.com',
```

### Error: CORS
```python
# Verifica que CORS_ALLOW_ALL_ORIGINS = True en settings.py
# O agrega tu frontend a CORS_ALLOWED_ORIGINS
```

---

## 📁 Estructura del proyecto para Render

```
backend_gestor_pollos/
├── .gitignore
├── Procfile
├── render.yaml
├── requirements.txt (opcional, el principal está en bd_Smartgalpon_api/)
└── bd_Smartgalpon_api/
    ├── manage.py
    ├── requirements.txt  ← ESTE ES EL IMPORTANTE
    └── bd_Smartgalpon/
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

---

## 🎯 Checklist final antes de desplegar

- [ ] Código subido a GitHub
- [ ] `requirements.txt` actualizado
- [ ] `render.yaml` configurado
- [ ] `settings.py` con ALLOWED_HOSTS para Render
- [ ] Variables de entorno configuradas en Render
- [ ] Base de datos PostgreSQL creada
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] API probada con curl/Postman
- [ ] Flutter app actualizada con la nueva URL

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Render: **Logs** tab
2. Verifica las variables de entorno
3. Ejecuta `python manage.py check --deploy` para verificaciones de producción
