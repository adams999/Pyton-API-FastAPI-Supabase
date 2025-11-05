# Guía Rápida de Testing

Esta guía te ayudará a empezar con los tests de forma rápida.

## Instalación Rápida

```bash
# Instalar dependencias de testing
pip install -r requirements-test.txt
```

## Ejecutar Tests - Forma Rápida

### Windows
```bash
# Usar el script interactivo
run_tests.bat

# O directamente
pytest
```

### Linux/MacOS
```bash
# Dar permisos de ejecución
chmod +x run_tests.sh

# Usar el script interactivo
./run_tests.sh

# O directamente
pytest
```

## Comandos Más Usados

```bash
# Ejecutar todos los tests
pytest

# Solo tests unitarios (sin Supabase)
pytest tests/unit/

# Tests con cobertura
pytest --cov=. --cov-report=html

# Tests verbose (más detalles)
pytest -v

# Tests de un archivo específico
pytest tests/unit/test_items.py

# Tests de una clase específica
pytest tests/unit/test_items.py::TestCreateItem

# Test específico
pytest tests/unit/test_items.py::TestCreateItem::test_create_item_success
```

## Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidas (client, mocks, datos de prueba)
├── unit/                    # Tests unitarios (usan mocks)
│   ├── test_root.py        # Tests del endpoint /
│   └── test_items.py       # Tests de CRUD de items
└── integration/             # Tests de integración (usan Supabase real)
    └── test_items_integration.py
```

## Fixtures Disponibles

En tus tests puedes usar estas fixtures directamente:

```python
def test_example(client, sample_item_data):
    # client: TestClient de FastAPI
    # sample_item_data: Datos de ejemplo para crear items
    response = client.post("/items", json=sample_item_data)
    assert response.status_code == 200
```

### Fixtures principales:
- `client`: TestClient de FastAPI
- `mock_supabase_client`: Mock de Supabase
- `sample_item_data`: Datos para crear un item
- `sample_item_response`: Item completo con ID
- `sample_items_list`: Lista de items

## Escribir un Test Nuevo

### Template básico:

```python
"""Descripción del módulo"""

import pytest
from fastapi.testclient import TestClient


class TestMiFeature:
    """Tests para mi feature"""

    def test_algo_exitoso(self, client: TestClient):
        """Test que verifica comportamiento exitoso"""
        # Arrange (preparar)
        data = {"key": "value"}

        # Act (actuar)
        response = client.post("/endpoint", json=data)

        # Assert (verificar)
        assert response.status_code == 200
        assert response.json()["key"] == "value"
```

## Tests con Mock de Supabase

```python
from unittest.mock import MagicMock

def test_con_mock(self, client, mock_supabase_client):
    # Configurar el mock
    mock_response = MagicMock()
    mock_response.data = [{"id": "123", "name": "Test"}]
    mock_supabase_client.table.return_value.select.return_value.execute.return_value = mock_response

    # Hacer petición
    response = client.get("/items")

    # Verificar
    assert response.status_code == 200
    assert len(response.json()) == 1
```

## Ver Cobertura

```bash
# Generar reporte HTML
pytest --cov=. --cov-report=html

# Abrir en navegador (Windows)
start htmlcov\index.html

# Abrir en navegador (Linux/MacOS)
open htmlcov/index.html
```

## Debugging

```bash
# Ver print statements
pytest -s

# Detener en primer fallo
pytest -x

# Modo muy verbose
pytest -vv
```

## Tests de Integración

Los tests de integración requieren conexión real con Supabase:

```bash
# Ejecutar solo tests de integración
pytest tests/integration/ -m integration

# Saltar tests de integración
pytest -m "not integration"
```

**IMPORTANTE**: Los tests de integración usan tu base de datos real. Usa una base de datos de prueba.

## Solución de Problemas Comunes

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de instalar las dependencias
pip install -r requirements-test.txt
```

### Error: "No module named 'models'"
```bash
# Ejecuta pytest desde el directorio raíz del proyecto
cd c:\Users\ADAMS\Documents\ADAMS\ADAMS PROGRAMACION\BE-BETTER\fastApi
pytest
```

### Tests de integración fallan
- Verifica que tu archivo `.env` tenga las credenciales correctas de Supabase
- Verifica que la tabla `items` exista en Supabase
- Verifica que tengas conexión a internet

## Verificar que Todo Funciona

Ejecuta este test rápido:

```bash
# Debería pasar 4 tests del endpoint root
pytest tests/unit/test_root.py -v
```

Si este test pasa, ¡todo está funcionando correctamente!

## Próximos Pasos

1. Lee el [README de tests](tests/README.md) completo para más detalles
2. Ejecuta `pytest` para ver todos los tests
3. Agrega tests cuando implementes nuevas funcionalidades

## Enlaces Útiles

- [Documentación de Pytest](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [README completo de tests](tests/README.md)

---

Para más información, consulta [tests/README.md](tests/README.md)
