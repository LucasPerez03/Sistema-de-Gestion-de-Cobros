# BYPay

BYPay es una aplicación web para administrar clientes, usuarios, servicios, cuotas y pagos. Está compuesta por una API REST desarrollada con FastAPI y una interfaz web desarrollada con React.

## Funcionalidades

- Inicio de sesión con autenticación JWT.
- Administración de clientes, usuarios y servicios.
- Gestión de cuotas y registro de pagos.
- Documentación interactiva de la API mediante Swagger UI.

## Tecnologías

- **Backend:** Python, FastAPI, Pydantic y PostgreSQL.
- **Autenticación:** JWT y bcrypt.
- **Frontend:** React, Vite, React Router y Axios.
- **Gestor de paquetes del frontend:** pnpm.

## Requisitos

- Python y pip.
- PostgreSQL y la herramienta `psql` disponible en PATH.
- Node.js y pnpm.

## Configuración inicial

### 1. Crear y configurar la base de datos

Desde la raíz del repositorio, crea la base de datos:

```powershell
psql -U postgres -c "CREATE DATABASE bypay_db;"
```

Copia el archivo de configuración de ejemplo y edita `backend/.env` con los datos de tu instalación:

```powershell
Copy-Item backend/.env.example backend/.env
```

Variables disponibles:

| Variable | Descripción | Valor de ejemplo |
| --- | --- | --- |
| `DB_HOST` | Servidor PostgreSQL | `localhost` |
| `DB_PORT` | Puerto PostgreSQL | `5432` |
| `DB_NAME` | Base de datos | `bypay_db` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | Configúrala localmente |
| `SECRET_KEY` | Clave para firmar tokens JWT | Reemplaza el ejemplo por una clave secreta propia |
| `ALGORITHM` | Algoritmo JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token en minutos | `120` |

Inicializa las tablas:

```powershell
psql -U postgres -d bypay_db -f backend/schema.sql
```

> **Importante:** `schema.sql` ejecuta `DROP TABLE` sobre las tablas de la aplicación antes de crearlas. Esto elimina los datos existentes; úsalo solo en una base de datos nueva o después de hacer un respaldo.

### 2. Instalar dependencias del backend

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/Activate.ps1
python -m pip install -r backend/requirements.txt
```

### 3. Instalar dependencias del frontend

```powershell
Set-Location frontend
pnpm install
Set-Location ..
```

## Ejecutar la aplicación

Carga los datos de demostración una vez que la base de datos esté inicializada:

```powershell
python -m backend.seed
```

El seed crea usuarios, un cliente, un servicio y una cuota de ejemplo. Las credenciales de demostración que utiliza son `admin@bypay.com`, `entrenador@bypay.com` y `juan.perez@example.com`, todas con contraseña `admin123`. No uses estas credenciales en producción.

Abre dos terminales desde la raíz del repositorio.

Terminal 1, API:

```powershell
backend/.venv/Scripts/Activate.ps1
uvicorn backend.app.main:app --reload
```

Terminal 2, frontend:

```powershell
Set-Location frontend
pnpm dev
```

La interfaz estará disponible en `http://localhost:5173`. La API estará disponible en `http://127.0.0.1:8000`; su documentación interactiva se encuentra en `http://127.0.0.1:8000/docs`.

El frontend tiene configurada la URL local de la API en `frontend/src/api/axios.js`. Si cambias el host o el puerto del backend, actualiza esa URL y los orígenes permitidos de CORS en `backend/app/main.py`.

## Pruebas

Las pruebas de `backend/tests` usan pytest, que no está incluido en `backend/requirements.txt`. Instálalo en el entorno virtual y ejecútalas desde la raíz:

```powershell
python -m pip install pytest
python -m pytest backend/tests
```

El script `backend/test_db.py` es una comprobación manual adicional y requiere una conexión activa a PostgreSQL:

```powershell
python -m backend.test_db
```

## Estructura del proyecto

```text
backend/
  app/
    config/       Configuración, seguridad y conexión a PostgreSQL
    models/       Modelos del dominio
    repositories/ Acceso a datos
    routers/      Endpoints de la API
    schemas/      Esquemas de entrada y salida
    services/     Lógica de negocio
    strategies/   Estrategias de pago
  schema.sql      Esquema de la base de datos
  seed.py         Datos de demostración
  tests/          Pruebas automatizadas
frontend/
  src/
    api/          Cliente HTTP
    pages/        Vistas de la aplicación
    services/     Servicios del frontend
```

## Endpoints principales

- `/auth`: inicio de sesión y consulta del usuario autenticado.
- `/clientes`: consulta y administración de clientes.
- `/usuarios`: consulta y administración de usuarios.
- `/servicios`: consulta y administración de servicios.
- `/cuotas`: consulta y administración de cuotas.
- `/pagos`: consulta y registro de pagos.

Consulta los esquemas y operaciones completas en Swagger UI (`/docs`) con el backend en ejecución.