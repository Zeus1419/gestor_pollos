# ✅ Proyecto listo para desplegar en Render

## 📋 Archivos creados/actualizados

### Backend (`backend_gestor_pollos/`)

| Archivo | Estado | Descripción |
|---------|--------|-------------|
| `render.yaml` | ✅ Actualizado | Configuración del servicio web |
| `Procfile` | ✅ Actualizado | Comando de inicio |
| `.gitignore` | ✅ Actualizado | Archivos ignorados |
| `README.md` | ✅ Creado | Documentación del proyecto |
| `DEPLOY_RENDER.md` | ✅ Creado | Guía completa de despliegue |
| `prepare_render.bat` | ✅ Creado | Script Windows |
| `prepare_render.sh` | ✅ Creado | Script Linux/Mac |
| `bd_Smartgalpon_api/.env.example` | ✅ Por crear | Ejemplo de variables |
| `settings.py` | ✅ Actualizado | Configuración para producción |

---

## 🚀 Pasos rápidos para desplegar

### 1. Subir a GitHub
```bash
cd "C:\Users\Pc\Desktop\Gestion pollo\backend_gestor_pollos"

# Inicializar git
git init
git branch -M main

# Agregar archivos
git add .
git commit -m "Initial commit - Backend listo para Render"

# Crear repositorio en GitHub y conectar
# Ve a https://github.com/new y crea: backend-gestor-pollos
git remote add origin https://github.com/TU_USUARIO/backend-gestor-pollos.git
git push -u origin main
```

### 2. Desplegar en Render
1. Ve a https://dashboard.render.com/new
2. **Web Service**
3. Conecta tu repositorio: `backend-gestor-pollos`
4. Render detectará el `render.yaml` automáticamente

### 3. Configurar en Render

#### Variables de entorno (Environment)
```
DEBUG=false
SECRET_KEY=(genera en https://djecrety.ir/)
DATABASE_URL=(la obtienes de tu PostgreSQL en Render)
ALLOWED_HOSTS=*
PYTHON_VERSION=3.9.0
```

#### Crear PostgreSQL
1. **New +** → **PostgreSQL**
2. Name: `smartgalpon-db`
3. Copia el **Internal Database URL**
4. Pega en `DATABASE_URL`

### 4. Ejecutar migraciones
En la consola de Render (Shell):
```bash
cd bd_Smartgalpon_api
python manage.py migrate
python manage.py createsuperuser
```

### 5. ¡Listo! 🎉
Tu API estará en: `https://smartgalpon-api.onrender.com/api`

---

## 📱 Actualizar Flutter app

En `lib/config/api_config.dart` (línea 22):

```dart
// Para producción (Render)
static String get baseUrl => baseUrlProduccion;
```

---

## 🧪 Probar API

```bash
# Test básico
curl https://smartgalpon-api.onrender.com/api/lotes/

# Login
curl -X POST https://smartgalpon-api.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"tu_usuario","password":"tu_password"}'
```

---

## ⚠️ Importante

- El plan **gratuito** de Render se duerme después de 15 min
- La primera petición después de inactivo tarda ~30-50 segundos
- Para producción real, considera un plan de pago

---

## 📞 ¿Problemas?

1. **Revisa los logs** en Render → Logs tab
2. **Verifica variables** de entorno
3. **Ejecuta**: `python manage.py check --deploy`

---

## 📚 Documentación adicional

- `DEPLOY_RENDER.md` - Guía detallada
- `README.md` - Documentación completa del proyecto
- `CAMBIAR_ENTORNO.md` - Cómo cambiar entre desarrollo/producción en Flutter
