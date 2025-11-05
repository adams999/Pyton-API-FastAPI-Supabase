"""
Tests de integración para Items con Supabase.

NOTA: Estos tests requieren una conexión real con Supabase.
Para ejecutarlos, asegúrate de tener configuradas las variables de entorno
correctas en tu archivo .env

Para ejecutar solo estos tests:
    pytest tests/integration/ -m integration

Para saltear estos tests:
    pytest -m "not integration"
"""

import pytest
from fastapi.testclient import TestClient
from main import app
import uuid


@pytest.mark.integration
class TestItemsIntegration:
    """
    Tests de integración para verificar la interacción real con Supabase.

    IMPORTANTE: Estos tests hacen peticiones reales a Supabase.
    Asegúrate de usar una base de datos de prueba, no la de producción.
    """

    @pytest.fixture(scope="class")
    def integration_client(self):
        """Cliente de test para integración."""
        with TestClient(app) as test_client:
            yield test_client

    def test_create_and_retrieve_item(self, integration_client):
        """
        Test de integración: Crear un item y luego recuperarlo.

        Este test verifica el flujo completo de creación y lectura.
        """
        # Crear un item
        new_item = {
            "name": f"Integration Test Item {uuid.uuid4().hex[:8]}",
            "description": "Item creado durante test de integración",
            "price": 99.99,
            "tax": 21.0
        }

        create_response = integration_client.post("/items", json=new_item)
        assert create_response.status_code == 200

        created_item = create_response.json()
        item_id = created_item["id"]

        # Verificar que se puede recuperar
        get_response = integration_client.get(f"/items/{item_id}")
        assert get_response.status_code == 200

        retrieved_item = get_response.json()
        assert retrieved_item["name"] == new_item["name"]
        assert retrieved_item["description"] == new_item["description"]

        # Limpiar: eliminar el item creado
        delete_response = integration_client.delete(f"/items/{item_id}")
        assert delete_response.status_code == 200

    def test_full_crud_cycle(self, integration_client):
        """
        Test de integración: Ciclo CRUD completo.

        Este test verifica Create, Read, Update, Delete en secuencia.
        """
        # 1. CREATE
        new_item = {
            "name": f"CRUD Test Item {uuid.uuid4().hex[:8]}",
            "description": "Item para test CRUD completo",
            "price": 149.99,
            "tax": 19.0
        }

        create_response = integration_client.post("/items", json=new_item)
        assert create_response.status_code == 200
        created_item = create_response.json()
        item_id = created_item["id"]

        # 2. READ (individual)
        read_response = integration_client.get(f"/items/{item_id}")
        assert read_response.status_code == 200
        read_item = read_response.json()
        assert read_item["name"] == new_item["name"]

        # 3. UPDATE
        updated_data = {
            "name": "CRUD Test Item UPDATED",
            "description": "Descripción actualizada",
            "price": 199.99,
            "tax": 21.0
        }

        update_response = integration_client.put(f"/items/{item_id}", json=updated_data)
        assert update_response.status_code == 200
        updated_item = update_response.json()
        assert updated_item["name"] == updated_data["name"]
        assert updated_item["price"] == updated_data["price"]

        # 4. DELETE
        delete_response = integration_client.delete(f"/items/{item_id}")
        assert delete_response.status_code == 200

        # Verificar que ya no existe
        get_deleted_response = integration_client.get(f"/items/{item_id}")
        assert get_deleted_response.status_code == 404

    @pytest.mark.skip(reason="Test costoso - ejecutar manualmente")
    def test_list_items_pagination(self, integration_client):
        """
        Test de integración: Paginación de items.

        Este test verifica que la paginación funciona correctamente.
        Está marcado como skip porque crea múltiples items.
        """
        # Crear varios items
        created_ids = []
        for i in range(5):
            new_item = {
                "name": f"Pagination Test Item {i}",
                "description": f"Item {i} para test de paginación",
                "price": 10.0 * (i + 1),
                "tax": 21.0
            }
            response = integration_client.post("/items", json=new_item)
            assert response.status_code == 200
            created_ids.append(response.json()["id"])

        try:
            # Probar paginación
            page1 = integration_client.get("/items?limit=2&offset=0")
            assert page1.status_code == 200
            page1_data = page1.json()
            assert len(page1_data) <= 2

            page2 = integration_client.get("/items?limit=2&offset=2")
            assert page2.status_code == 200
            page2_data = page2.json()
            assert len(page2_data) <= 2

        finally:
            # Limpiar: eliminar items creados
            for item_id in created_ids:
                integration_client.delete(f"/items/{item_id}")


@pytest.mark.integration
class TestDatabaseConnectivity:
    """Tests que verifican la conectividad básica con Supabase."""

    def test_database_is_accessible(self):
        """
        Test que verifica que la base de datos es accesible.

        Este test verifica que podemos conectarnos a Supabase.
        """
        from db import get_supabase_client

        try:
            client = get_supabase_client()
            assert client is not None
        except Exception as e:
            pytest.fail(f"No se pudo conectar a Supabase: {str(e)}")

    def test_items_table_exists(self):
        """
        Test que verifica que la tabla items existe.

        Este test hace una consulta simple para verificar la tabla.
        """
        from db import get_supabase_client

        try:
            client = get_supabase_client()
            # Intentar hacer una query simple a la tabla
            response = client.table("items").select("id").limit(1).execute()
            assert response is not None
        except Exception as e:
            pytest.fail(f"Error al acceder a la tabla items: {str(e)}")
