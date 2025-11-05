# FastAPI + Supabase REST API

API REST moderna construida con FastAPI y Supabase para gestión de items con operaciones CRUD completas, implementando arquitectura MVC.

## Características

- **FastAPI**: Framework web moderno y rápido para construir APIs con Python
- **Supabase**: Backend-as-a-Service con PostgreSQL
- **Pydantic**: Validación de datos y serialización
- **UUID**: Identificadores únicos universales para los recursos
- **Arquitectura MVC**: Separación de responsabilidades en Modelos, Vistas (Routes) y Controladores
- **Arquitectura escalable**: Estructura modular lista para crecer
- **Testing completo**: 22+ tests unitarios con pytest y TestClient (79% cobertura)

## Tecnologías

- Python 3.9+
- FastAPI
- Supabase (PostgreSQL)
- Pydantic v2
- Uvicorn (ASGI server)

## Estructura del Proyecto

```
fastApi/
├── config/                          # Configuraciones centralizadas
│   ├── __init__.py
│   └── settings.py                  # Variables de entorno con Pydantic Settings
│
├── db/                              # Conexiones a bases de datos
│   ├── __init__.py
│   └── supabase.py                  # Cliente de Supabase y dependencias
│
├── models/                          # Esquemas Pydantic (Modelos)
│   ├── __init__.py
│   └── items/                       # Módulo de modelos de Items
│       ├── __init__.py
│       └── item.py                  # Modelos de Item (Create, Base, Item)
│
├── controllers/                     # Controladores (Lógica de peticiones)
│   ├── __init__.py
│   └── item_controller/             # Módulo del controlador de Items
│       ├── __init__.py
│       └── item_controller.py       # Controlador para Items
│
├── services/                        # Servicios (Lógica de negocio)
│   ├── __init__.py
│   └── item_service.py              # Servicio para Items (operaciones DB)
│
├── routes/                          # Rutas (Definición de endpoints)
│   ├── __init__.py
│   └── item_routes/                 # Módulo de rutas de Items
│       ├── __init__.py
│       └── item_routes.py           # Router para Items
│
├── tests/                           # Suite de tests
│   ├── conftest.py                  # Fixtures compartidas
│   ├── unit/                        # Tests unitarios
│   │   ├── test_root.py            # Tests del endpoint root
│   │   └── test_items.py           # Tests CRUD de items
│   ├── integration/                 # Tests de integración
│   └── e2e/                         # Tests end-to-end
│
├── main.py                          # Aplicación principal
├── pytest.ini                       # Configuración de pytest
├── requirements-test.txt            # Dependencias de testing
├── run_tests.bat / run_tests.sh     # Scripts para ejecutar tests
├── .env                             # Variables de entorno (no incluido en git)
├── .env.example                     # Plantilla de variables de entorno
├── requirements.txt                 # Dependencias de Python
├── TESTING_GUIDE.md                 # Guía rápida de testing
└── README.md                        # Este archivo
```

## Arquitectura MVC

### Modelos (Models)
- Definen la estructura de datos usando Pydantic
- Validación automática de datos
- Ubicación: `models/`

### Controladores (Controllers)
- Manejan las peticiones HTTP
- Validan parámetros de entrada
- Delegan la lógica de negocio a los servicios
- Ubicación: `controllers/`

### Servicios (Services)
- Contienen la lógica de negocio
- Interactúan con la base de datos
- Pueden ser reutilizados por múltiples controladores
- Ubicación: `services/`

### Rutas (Routes)
- Definen los endpoints de la API
- Configuran decoradores HTTP (GET, POST, PUT, DELETE)
- Llaman a los controladores correspondientes
- Ubicación: `routes/`

## Requisitos Previos

- Python 3.9 o superior
- Cuenta de Supabase (gratis en [supabase.com](https://supabase.com))
- Git (opcional, para clonar el repositorio)

## Instalación

### 1. Clonar el repositorio (si aplica)

```bash
git clone <tu-repositorio>
cd fastApi
```

### 2. Crear entorno virtual

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key-aqui

# Configuración de la aplicación
APP_NAME="FastAPI + Supabase API"
APP_VERSION="1.0.0"
DEBUG=False
```

Para obtener tus credenciales de Supabase:
1. Ve a [supabase.com](https://supabase.com) y accede a tu proyecto
2. Ve a **Settings** > **API**
3. Copia el **Project URL** (SUPABASE_URL)
4. Copia el **anon/public** key (SUPABASE_KEY)

### 5. Crear la tabla en Supabase

Ejecuta este SQL en el SQL Editor de Supabase:

```sql
-- Crear tabla items
CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price NUMERIC,
    tax NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar Row Level Security (opcional pero recomendado)
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas las operaciones (ajustar según necesidades)
CREATE POLICY "Allow all operations" ON items
    FOR ALL
    USING (true)
    WITH CHECK (true);
```

## Uso

### Iniciar el servidor de desarrollo

```bash
uvicorn main:app --reload
```

O alternativamente:

```bash
python -m uvicorn main:app --reload
```

El servidor estará disponible en: **http://127.0.0.1:8000**

### Opciones del servidor

```bash
# Cambiar puerto
uvicorn main:app --reload --port 8080

# Cambiar host (permitir conexiones externas)
uvicorn main:app --reload --host 0.0.0.0

# Sin auto-reload (producción)
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Documentación de la API

FastAPI genera documentación interactiva automáticamente:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

## Endpoints Disponibles

### Root
- `GET /` - Verificar que la API está funcionando

### Items CRUD

#### Crear Item
```http
POST /items
Content-Type: application/json

{
    "name": "Producto ejemplo",
    "description": "Descripción del producto",
    "price": 99.99,
    "tax": 21.0
}
```

#### Obtener todos los Items
```http
GET /items?limit=10&offset=0
```

Parámetros query:
- `limit` (opcional): Número de items a retornar (default: 10)
- `offset` (opcional): Número de items a saltar (default: 0)

#### Obtener Item por ID
```http
GET /items/{item_id}
```

#### Actualizar Item
```http
PUT /items/{item_id}
Content-Type: application/json

{
    "name": "Producto actualizado",
    "description": "Nueva descripción",
    "price": 149.99,
    "tax": 21.0
}
```

#### Eliminar Item
```http
DELETE /items/{item_id}
```

## Ejemplos con cURL

### Crear un item
```bash
curl -X POST "http://127.0.0.1:8000/items" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Laptop",
        "description": "Laptop de alta gama",
        "price": 1299.99,
        "tax": 21.0
    }'
```

### Obtener todos los items
```bash
curl "http://127.0.0.1:8000/items?limit=5&offset=0"
```

### Obtener un item específico
```bash
curl "http://127.0.0.1:8000/items/{uuid-del-item}"
```

### Actualizar un item
```bash
curl -X PUT "http://127.0.0.1:8000/items/{uuid-del-item}" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Laptop Actualizada",
        "description": "Descripción actualizada",
        "price": 1199.99,
        "tax": 21.0
    }'
```

### Eliminar un item
```bash
curl -X DELETE "http://127.0.0.1:8000/items/{uuid-del-item}"
```

## Modelos de Datos

### ItemCreate (Request para crear)
```json
{
    "name": "string (required, 1-100 chars)",
    "description": "string (required, 1-500 chars)",
    "price": "number (optional, >= 0)",
    "tax": "number (optional, >= 0)"
}
```

### ItemBase (Response básico)
```json
{
    "id": "uuid",
    "name": "string",
    "description": "string",
    "price": "number | null",
    "tax": "number | null"
}
```

### Item (Response completo)
```json
{
    "id": "uuid",
    "name": "string",
    "description": "string",
    "price": "number | null",
    "tax": "number | null",
    "created_at": "datetime | null"
}
```

## Validaciones

La API implementa validaciones automáticas usando Pydantic:

- **name**: Requerido, 1-100 caracteres
- **description**: Requerido, 1-500 caracteres
- **price**: Opcional, debe ser >= 0
- **tax**: Opcional, debe ser >= 0
- **id**: UUID válido en rutas

Los errores de validación retornan código 422 con detalles del error.

## Desarrollo

### Agregar nuevos recursos (siguiendo MVC)

El proyecto utiliza una estructura modular anidada. Cada recurso tiene su propio módulo dentro de models, controllers y routes.

#### 1. Crear el Modelo
```python
# models/users/__init__.py
from .user import User, UserBase, UserCreate

__all__ = ["User", "UserBase", "UserCreate"]

# models/users/user.py
from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    email: str

class UserBase(UserCreate):
    id: UUID

class User(UserBase):
    pass
```

Luego exportar en `models/__init__.py`:
```python
from .users import User, UserBase, UserCreate
```

#### 2. Crear el Servicio (Lógica de Negocio)
```python
# services/user_service.py
from supabase import Client
from models import User, UserBase, UserCreate

class UserService:
    @staticmethod
    def create_user(user: UserCreate, db: Client) -> UserBase:
        response = db.table("users").insert(user.model_dump()).execute()
        return response.data[0]
```

Exportar en `services/__init__.py`:
```python
from .user_service import UserService
```

#### 3. Crear el Controlador
```python
# controllers/user_controller/__init__.py
from .user_controller import UserController

__all__ = ["UserController"]

# controllers/user_controller/user_controller.py
from db import DbDependency
from models import User, UserBase, UserCreate
from services import UserService

class UserController:
    @staticmethod
    async def create_user(user: UserCreate, db: DbDependency) -> UserBase:
        return UserService.create_user(user, db)
```

Exportar en `controllers/__init__.py`:
```python
from .user_controller import UserController
```

#### 4. Crear las Rutas
```python
# routes/user_routes/__init__.py
from .user_routes import router

__all__ = ["router"]

# routes/user_routes/user_routes.py
from fastapi import APIRouter
from controllers import UserController
from models import User, UserBase, UserCreate
from db import DbDependency

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserBase)
async def create_user(user: UserCreate, db: DbDependency):
    return await UserController.create_user(user, db)
```

Exportar en `routes/__init__.py`:
```python
from .user_routes import router as user_router
```

#### 5. Registrar el Router en main.py
```python
# main.py
from routes import item_router, user_router

app.include_router(item_router)
app.include_router(user_router)
```

**Nota importante:** La estructura modular anidada permite una mejor organización cuando el proyecto crece, manteniendo cada recurso aislado en su propio módulo.

### Agregar nuevas bases de datos

1. Crear archivo en `db/` (ej: `mongodb.py`)
2. Implementar cliente y dependencia
3. Exportar en `db/__init__.py`

### Agregar configuraciones

Editar `config/settings.py` y agregar nuevos campos a la clase `Settings`.

## Testing

La aplicación cuenta con una suite completa de tests unitarios y de integración implementada con **pytest** y **TestClient de FastAPI**.

### Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidas (client, mocks, datos de prueba)
├── unit/                    # Tests unitarios (usan mocks, no requieren Supabase)
│   ├── test_root.py        # Tests del endpoint / (4 tests)
│   └── test_items.py       # Tests CRUD de items (18 tests)
├── integration/             # Tests de integración (requieren Supabase real)
│   └── test_items_integration.py
├── e2e/                     # Tests end-to-end (futuro)
├── fixtures/                # Datos de prueba adicionales
└── utils/                   # Utilidades para tests
```

### Instalación de Dependencias de Testing

```bash
pip install -r requirements-test.txt
```

### Ejecutar Tests

#### Comandos básicos

```bash
# Ejecutar todos los tests unitarios
pytest tests/unit/

# Ejecutar tests con output detallado
pytest -v

# Ejecutar tests con cobertura
pytest --cov=. --cov-report=html

# Ejecutar un archivo específico
pytest tests/unit/test_items.py

# Ejecutar un test específico
pytest tests/unit/test_items.py::TestCreateItem::test_create_item_success
```

#### Scripts interactivos

**Windows:**
```bash
run_tests.bat
```

**Linux/MacOS:**
```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Cobertura de Tests

**Tests Implementados: 22 tests unitarios**

- ✅ **Endpoint Root** (4 tests) - 100% cobertura
- ✅ **CREATE /items** (5 tests) - Crear items, validaciones
- ✅ **READ /items** (3 tests) - Listar items, paginación
- ✅ **READ /items/{id}** (3 tests) - Obtener por ID, errores
- ✅ **UPDATE /items/{id}** (3 tests) - Actualizar items
- ✅ **DELETE /items/{id}** (2 tests) - Eliminar items
- ✅ **Integridad** (2 tests) - Métodos HTTP, Content-Type

**Cobertura Total: 79%**

### Fixtures Disponibles

Los tests incluyen fixtures reutilizables en `conftest.py`:

- **`client`**: TestClient de FastAPI para hacer peticiones HTTP
- **`mock_supabase_client`**: Mock de Supabase (no requiere conexión)
- **`sample_item_data`**: Datos de ejemplo para crear items
- **`sample_item_response`**: Item completo con ID y metadata
- **`sample_items_list`**: Lista de múltiples items

### Ejemplo de Test

```python
def test_create_item_success(client, mock_supabase_client, sample_item_data):
    """Test que verifica la creación exitosa de un item."""
    # Configurar el mock
    mock_response = MagicMock()
    mock_response.data = [sample_item_data]
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = mock_response

    # Hacer petición
    response = client.post("/items", json=sample_item_data)

    # Verificar
    assert response.status_code == 200
    assert response.json()["name"] == sample_item_data["name"]
```

### Tests de Integración

Los tests de integración verifican la interacción real con Supabase:

```bash
# Ejecutar tests de integración (requiere Supabase configurado)
pytest tests/integration/ -m integration

# Saltar tests de integración
pytest -m "not integration"
```

**IMPORTANTE**: Los tests de integración usan tu base de datos real. Usa una base de datos de prueba.

### Documentación Completa de Testing

Para más información sobre testing:

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Guía rápida de inicio
- **[tests/README.md](tests/README.md)** - Documentación completa de tests
- **[TESTS_SUMMARY.md](TESTS_SUMMARY.md)** - Resumen de implementación

### Agregar Nuevos Tests

Al agregar nuevas funcionalidades:

1. Escribe tests primero (TDD)
2. Ejecuta `pytest` para verificar que todos pasen
3. Mantén la cobertura por encima del 70%
4. Usa las fixtures existentes en `conftest.py`
5. Documenta los tests con docstrings

## Deployment

### Opción 1: Render.com (Recomendado)

1. Crear cuenta en [render.com](https://render.com)
2. Conectar tu repositorio de GitHub
3. Crear un nuevo Web Service
4. Configurar:
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Agregar variables de entorno desde el dashboard

### Opción 2: Railway

1. Crear cuenta en [railway.app](https://railway.app)
2. Crear nuevo proyecto desde GitHub
3. Railway detectará automáticamente que es Python
4. Agregar variables de entorno

### Opción 3: Fly.io

```bash
# Instalar flyctl
# Seguir instrucciones en https://fly.io/docs/hands-on/install-flyctl/

# Login
flyctl auth login

# Lanzar app
flyctl launch

# Deploy
flyctl deploy
```

## Variables de Entorno en Producción

Asegúrate de configurar estas variables en tu plataforma de hosting:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
APP_NAME=FastAPI + Supabase API
APP_VERSION=1.0.0
DEBUG=False
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pydantic_settings'"
```bash
pip install pydantic-settings
```

### Error: "Connection refused" a Supabase
- Verifica que `SUPABASE_URL` y `SUPABASE_KEY` sean correctas
- Verifica que la tabla `items` exista en Supabase
- Verifica las políticas RLS en Supabase

### Error: "404 Item not found"
- Verifica que el UUID sea correcto
- Verifica que el item exista en la base de datos

### Error: "ImportError: cannot import name 'Client'"
- Asegúrate de que estés importando `Client` desde `supabase`, no de `postgrest`
- Limpia la caché de Python: `find . -type d -name "__pycache__" -exec rm -rf {} +`

### Error en tests: "ModuleNotFoundError"
```bash
# Instalar dependencias de testing
pip install -r requirements-test.txt
```

### Tests fallan con error de conexión
- Los **tests unitarios** NO requieren conexión a Supabase (usan mocks)
- Los **tests de integración** SÍ requieren Supabase configurado
- Ejecuta solo tests unitarios: `pytest tests/unit/`

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

## Recursos Adicionales

### Documentación del Proyecto
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Guía rápida de testing
- [tests/README.md](tests/README.md) - Documentación completa de tests
- [TESTS_SUMMARY.md](TESTS_SUMMARY.md) - Resumen de implementación de tests

### Documentación Externa
- [Documentación de FastAPI](https://fastapi.tiangolo.com)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Documentación de Supabase](https://supabase.com/docs)
- [Documentación de Pydantic](https://docs.pydantic.dev)
- [Documentación de Uvicorn](https://www.uvicorn.org)
- [Documentación de Pytest](https://docs.pytest.org/)
- [Patrones de Arquitectura MVC](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)

---

**Stack Tecnológico:** FastAPI + Supabase + PostgreSQL + Pydantic + Pytest

**Desarrollado con ❤️ usando testing moderno y arquitectura MVC**
