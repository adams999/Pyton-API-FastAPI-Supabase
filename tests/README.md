# Tests para FastAPI + Supabase API

Este directorio contiene la suite completa de tests para la aplicación FastAPI con Supabase.

## Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidas para todos los tests
├── unit/                    # Tests unitarios
│   ├── test_root.py        # Tests para el endpoint raíz
│   └── test_items.py       # Tests para CRUD de items
├── integration/             # Tests de integración (futuro)
├── e2e/                     # Tests end-to-end (futuro)
├── fixtures/                # Datos de prueba (futuro)
└── utils/                   # Utilidades para tests (futuro)
```

## Instalación de Dependencias

### Instalar dependencias de testing

```bash
pip install -r requirements-test.txt
```

O instalar individualmente:

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

## Ejecutar Tests

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests con output verbose

```bash
pytest -v
```

### Ejecutar solo tests unitarios

```bash
pytest tests/unit/
```

### Ejecutar un archivo específico

```bash
pytest tests/unit/test_items.py
```

### Ejecutar una clase específica de tests

```bash
pytest tests/unit/test_items.py::TestCreateItem
```

### Ejecutar un test específico

```bash
pytest tests/unit/test_items.py::TestCreateItem::test_create_item_success
```

### Ejecutar tests con cobertura

```bash
pytest --cov=. --cov-report=html
```

Esto generará un reporte de cobertura en `htmlcov/index.html`.

### Ejecutar tests y ver print statements

```bash
pytest -s
```

### Ejecutar tests y detener en el primer fallo

```bash
pytest -x
```

## Fixtures Disponibles

Las fixtures están definidas en [conftest.py](conftest.py) y están disponibles para todos los tests:

### `client`
TestClient de FastAPI que permite hacer peticiones HTTP a la aplicación sin ejecutar un servidor real.

**Uso:**
```python
def test_example(client):
    response = client.get("/")
    assert response.status_code == 200
```

### `mock_supabase_client`
Mock del cliente de Supabase para tests sin conectarse a la base de datos real.

**Uso:**
```python
def test_example(client, mock_supabase_client):
    # Configurar el comportamiento del mock
    mock_response = MagicMock()
    mock_response.data = [{"id": "123", "name": "Test"}]
    mock_supabase_client.table.return_value.select.return_value.execute.return_value = mock_response

    response = client.get("/items")
    assert response.status_code == 200
```

### `sample_item_data`
Diccionario con datos de ejemplo para crear un item.

**Uso:**
```python
def test_example(client, sample_item_data):
    response = client.post("/items", json=sample_item_data)
    assert response.status_code == 200
```

### `sample_item_response`
Diccionario con un item completo incluyendo ID y metadata.

### `sample_items_list`
Lista de múltiples items para tests de listado.

## Cobertura de Tests

### Tests Unitarios Implementados

#### Endpoint Root (`test_root.py`)
- ✅ Verificar status code 200
- ✅ Verificar respuesta JSON
- ✅ Verificar mensaje de respuesta
- ✅ Verificar estructura completa de respuesta

#### Endpoint Items - CREATE (`test_items.py`)
- ✅ Crear item exitosamente con todos los campos
- ✅ Crear item con datos mínimos (sin price y tax)
- ✅ Validar campos requeridos faltantes
- ✅ Validar precio negativo
- ✅ Validar longitud del nombre

#### Endpoint Items - READ (`test_items.py`)
- ✅ Obtener lista de items exitosamente
- ✅ Paginación de items (limit y offset)
- ✅ Lista vacía cuando no hay items
- ✅ Obtener item por ID exitosamente
- ✅ Respuesta 404 cuando item no existe
- ✅ Validar UUID inválido

#### Endpoint Items - UPDATE (`test_items.py`)
- ✅ Actualizar item exitosamente
- ✅ Respuesta 404 al actualizar item inexistente
- ✅ Validar datos inválidos en actualización

#### Endpoint Items - DELETE (`test_items.py`)
- ✅ Eliminar item exitosamente
- ✅ Validar UUID inválido

#### Tests de Integridad
- ✅ Verificar métodos HTTP disponibles
- ✅ Verificar Content-Type JSON

## Escribir Nuevos Tests

### Estructura básica de un test

```python
"""
Descripción del módulo de tests
"""

import pytest
from fastapi.testclient import TestClient


class TestNombreDelModulo:
    """Tests para [descripción]"""

    def test_nombre_descriptivo(self, client: TestClient):
        """
        Descripción detallada de qué verifica este test.

        Args:
            client: TestClient fixture
        """
        # Arrange (preparar)
        data = {"key": "value"}

        # Act (actuar)
        response = client.post("/endpoint", json=data)

        # Assert (verificar)
        assert response.status_code == 200
        assert response.json()["key"] == "value"
```

### Buenas prácticas

1. **Nombres descriptivos**: Los nombres de tests deben describir claramente qué se está probando
2. **AAA Pattern**: Seguir el patrón Arrange-Act-Assert
3. **Un concepto por test**: Cada test debe verificar una sola cosa
4. **Tests independientes**: Los tests no deben depender de otros tests
5. **Usar fixtures**: Reutilizar fixtures para evitar código duplicado
6. **Documentar**: Agregar docstrings que expliquen qué verifica el test

### Ejemplo de test con mock

```python
def test_with_mock(self, client: TestClient, mock_supabase_client):
    """Test que usa un mock de Supabase"""
    # Configurar el mock
    mock_response = MagicMock()
    mock_response.data = [{"id": "123", "name": "Test Item"}]
    mock_supabase_client.table.return_value.select.return_value.execute.return_value = mock_response

    # Hacer la petición
    response = client.get("/items")

    # Verificar
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Item"
```

## Tests Asíncronos

Si necesitas probar funciones asíncronas, usa el decorador `@pytest.mark.asyncio`:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected_value
```

## Verificar Excepciones

Para verificar que se lanzan excepciones correctamente:

```python
import pytest

def test_raises_exception(client):
    with pytest.raises(ValueError):
        # Código que debería lanzar ValueError
        some_function_that_raises()
```

## Marcadores de Tests

Puedes marcar tests con categorías:

```python
@pytest.mark.slow
def test_slow_operation(client):
    # Test que toma mucho tiempo
    pass

@pytest.mark.skip(reason="Funcionalidad aún no implementada")
def test_future_feature(client):
    pass
```

Ejecutar solo tests marcados:

```bash
# Solo tests lentos
pytest -m slow

# Saltar tests lentos
pytest -m "not slow"
```

## Debugging de Tests

### Ver print statements

```bash
pytest -s
```

### Entrar en modo debug con pdb

```python
def test_with_debug(client):
    import pdb; pdb.set_trace()
    response = client.get("/items")
    assert response.status_code == 200
```

### Ver información detallada de fallos

```bash
pytest -vv
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements-test.txt
      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml
```

## Próximos Pasos

### Tests de Integración
- Tests que verifican la integración real con Supabase
- Tests de flujos completos de usuario

### Tests E2E
- Tests que simulan el comportamiento real del usuario
- Tests de escenarios completos

### Tests de Performance
- Verificar tiempos de respuesta
- Tests de carga

## Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [TestClient Documentation](https://www.starlette.io/testclient/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)

## Contribuir

Al agregar nuevas funcionalidades, asegúrate de:

1. Escribir tests para la nueva funcionalidad
2. Asegurar que todos los tests existentes sigan pasando
3. Mantener la cobertura de código por encima del 80%
4. Seguir las convenciones de nombres establecidas
5. Documentar adecuadamente los nuevos tests

---

Desarrollado con Pytest y FastAPI TestClient
