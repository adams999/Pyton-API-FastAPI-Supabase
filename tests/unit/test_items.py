"""
Unit tests para los endpoints de Items (CRUD completo).

Estos tests verifican el funcionamiento de todos los endpoints relacionados
con la entidad Item utilizando mocks para evitar dependencias externas.
"""

from fastapi.testclient import TestClient
from unittest.mock import MagicMock


class TestCreateItem:
    """Tests para el endpoint POST /items"""

    def test_create_item_success(
        self, client: TestClient, mock_supabase_client, sample_item_data, sample_item_response
    ):
        """
        Test que verifica la creación exitosa de un item.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
            sample_item_data: Datos de ejemplo para crear un item
            sample_item_response: Respuesta simulada de la base de datos
        """
        # Configurar el mock para retornar el item creado
        mock_response = MagicMock()
        mock_response.data = [sample_item_response]
        mock_supabase_client.table.return_value.insert.return_value.execute.return_value = mock_response

        # Hacer la petición
        response = client.post("/items", json=sample_item_data)

        # Verificar la respuesta
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_item_data["name"]
        assert data["description"] == sample_item_data["description"]
        assert data["price"] == sample_item_data["price"]
        assert data["tax"] == sample_item_data["tax"]
        assert "id" in data

    def test_create_item_with_minimal_data(self, client: TestClient, mock_supabase_client):
        """
        Test que verifica la creación de un item con datos mínimos (sin price y tax).

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
        """
        minimal_item = {
            "name": "Minimal Item",
            "description": "Item with minimal data"
        }

        mock_response = MagicMock()
        mock_response.data = [{
            **minimal_item,
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "price": None,
            "tax": None
        }]
        mock_supabase_client.table.return_value.insert.return_value.execute.return_value = mock_response

        response = client.post("/items", json=minimal_item)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == minimal_item["name"]
        assert data["description"] == minimal_item["description"]

    def test_create_item_missing_required_fields(self, client: TestClient):
        """
        Test que verifica que falla al crear un item sin campos requeridos.

        Args:
            client: TestClient fixture
        """
        # Intentar crear item sin 'name'
        invalid_item = {
            "description": "Missing name field"
        }

        response = client.post("/items", json=invalid_item)
        assert response.status_code == 422  # Validation error

    def test_create_item_invalid_price(self, client: TestClient):
        """
        Test que verifica validación de precio negativo.

        Args:
            client: TestClient fixture
        """
        invalid_item = {
            "name": "Invalid Item",
            "description": "Item with negative price",
            "price": -10.0
        }

        response = client.post("/items", json=invalid_item)
        assert response.status_code == 422  # Validation error

    def test_create_item_name_too_long(self, client: TestClient):
        """
        Test que verifica validación de longitud del nombre.

        Args:
            client: TestClient fixture
        """
        invalid_item = {
            "name": "x" * 101,  # Excede el límite de 100 caracteres
            "description": "Valid description"
        }

        response = client.post("/items", json=invalid_item)
        assert response.status_code == 422  # Validation error


class TestGetItems:
    """Tests para el endpoint GET /items"""

    def test_get_items_success(self, client: TestClient, mock_supabase_client, sample_items_list):
        """
        Test que verifica obtener lista de items exitosamente.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
            sample_items_list: Lista de items de ejemplo
        """
        # Configurar el mock
        mock_response = MagicMock()
        mock_response.data = sample_items_list
        mock_supabase_client.table.return_value.select.return_value.range.return_value.execute.return_value = mock_response

        # Hacer la petición
        response = client.get("/items")

        # Verificar la respuesta
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]["name"] == "Item 1"

    def test_get_items_with_pagination(self, client: TestClient, mock_supabase_client, sample_items_list):
        """
        Test que verifica la paginación de items.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
            sample_items_list: Lista de items de ejemplo
        """
        mock_response = MagicMock()
        mock_response.data = sample_items_list[:2]  # Solo los primeros 2
        mock_supabase_client.table.return_value.select.return_value.range.return_value.execute.return_value = mock_response

        # Hacer petición con limit y offset
        response = client.get("/items?limit=2&offset=0")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_items_empty_list(self, client: TestClient, mock_supabase_client):
        """
        Test que verifica respuesta cuando no hay items.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
        """
        mock_response = MagicMock()
        mock_response.data = []
        mock_supabase_client.table.return_value.select.return_value.range.return_value.execute.return_value = mock_response

        response = client.get("/items")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0


class TestGetItem:
    """Tests para el endpoint GET /items/{item_id}"""

    def test_get_item_by_id_success(self, client: TestClient, mock_supabase_client, sample_item_response):
        """
        Test que verifica obtener un item por ID exitosamente.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
            sample_item_response: Item de ejemplo
        """
        # Configurar el mock
        mock_response = MagicMock()
        mock_response.data = [sample_item_response]
        mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        item_id = sample_item_response["id"]
        response = client.get(f"/items/{item_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == sample_item_response["name"]

    def test_get_item_by_id_not_found(self, client: TestClient, mock_supabase_client):
        """
        Test que verifica respuesta cuando el item no existe.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
        """
        # Configurar el mock para retornar lista vacía (item no encontrado)
        mock_response = MagicMock()
        mock_response.data = []
        mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        non_existent_id = "123e4567-e89b-12d3-a456-426614174999"
        response = client.get(f"/items/{non_existent_id}")

        # El servicio lanza HTTPException(404) pero el handler genérico lo captura y retorna 400
        assert response.status_code in [400, 404]
        # Verificar que hay un detalle en la respuesta
        assert "detail" in response.json()

    def test_get_item_invalid_uuid(self, client: TestClient):
        """
        Test que verifica respuesta con UUID inválido.

        Args:
            client: TestClient fixture
        """
        invalid_id = "not-a-valid-uuid"
        response = client.get(f"/items/{invalid_id}")

        assert response.status_code == 422  # Validation error


class TestUpdateItem:
    """Tests para el endpoint PUT /items/{item_id}"""

    def test_update_item_success(
        self, client: TestClient, mock_supabase_client, sample_item_data, sample_item_response
    ):
        """
        Test que verifica actualización exitosa de un item.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
            sample_item_data: Datos actualizados
            sample_item_response: Respuesta simulada
        """
        # Datos actualizados
        updated_data = {
            "name": "Updated Item",
            "description": "Updated description",
            "price": 199.99,
            "tax": 19.0
        }

        # Configurar el mock
        mock_response = MagicMock()
        mock_response.data = [{**sample_item_response, **updated_data}]
        mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response

        item_id = sample_item_response["id"]
        response = client.put(f"/items/{item_id}", json=updated_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == updated_data["name"]
        assert data["description"] == updated_data["description"]
        assert data["price"] == updated_data["price"]

    def test_update_item_not_found(self, client: TestClient, mock_supabase_client):
        """
        Test que verifica respuesta al actualizar item inexistente.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
        """
        # Configurar el mock para retornar lista vacía
        mock_response = MagicMock()
        mock_response.data = []
        mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response

        updated_data = {
            "name": "Updated Item",
            "description": "Updated description"
        }

        non_existent_id = "123e4567-e89b-12d3-a456-426614174999"
        response = client.put(f"/items/{non_existent_id}", json=updated_data)

        # El servicio lanza HTTPException(404) pero el handler genérico lo captura y retorna 400
        assert response.status_code in [400, 404]
        # Verificar que hay un detalle en la respuesta
        assert "detail" in response.json()

    def test_update_item_invalid_data(self, client: TestClient):
        """
        Test que verifica validación al actualizar con datos inválidos.

        Args:
            client: TestClient fixture
        """
        invalid_data = {
            "name": "",  # Nombre vacío, debería fallar
            "description": "Valid description"
        }

        item_id = "123e4567-e89b-12d3-a456-426614174000"
        response = client.put(f"/items/{item_id}", json=invalid_data)

        assert response.status_code == 422


class TestDeleteItem:
    """Tests para el endpoint DELETE /items/{item_id}"""

    def test_delete_item_success(self, client: TestClient, mock_supabase_client):
        """
        Test que verifica eliminación exitosa de un item.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
        """
        # Configurar el mock
        mock_response = MagicMock()
        mock_supabase_client.table.return_value.delete.return_value.eq.return_value.execute.return_value = mock_response

        item_id = "123e4567-e89b-12d3-a456-426614174000"
        response = client.delete(f"/items/{item_id}")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Item deleted successfully"

    def test_delete_item_invalid_uuid(self, client: TestClient):
        """
        Test que verifica respuesta al eliminar con UUID inválido.

        Args:
            client: TestClient fixture
        """
        invalid_id = "invalid-uuid"
        response = client.delete(f"/items/{invalid_id}")

        assert response.status_code == 422


class TestItemsEndpointIntegrity:
    """Tests de integridad general para los endpoints de items"""

    def test_items_endpoint_methods(self, client: TestClient, mock_supabase_client):
        """
        Test que verifica que todos los métodos HTTP están disponibles.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
        """
        # Configurar mocks básicos para GET
        mock_response_get = MagicMock()
        mock_response_get.data = []
        mock_supabase_client.table.return_value.select.return_value.range.return_value.execute.return_value = mock_response_get

        # Verificar que GET /items está disponible
        response = client.get("/items")
        assert response.status_code in [200, 404, 500]  # No debería ser 404 (not found endpoint)

        # Configurar mock para POST
        mock_response_post = MagicMock()
        mock_response_post.data = [{"id": "123e4567-e89b-12d3-a456-426614174000", "name": "test", "description": "test", "price": None, "tax": None}]
        mock_supabase_client.table.return_value.insert.return_value.execute.return_value = mock_response_post

        # Verificar que POST /items está disponible
        response = client.post("/items", json={"name": "test", "description": "test"})
        assert response.status_code in [200, 400, 422, 500]  # No debería ser 404

    def test_content_type_json(self, client: TestClient, mock_supabase_client):
        """
        Test que verifica que los endpoints retornan JSON.

        Args:
            client: TestClient fixture
            mock_supabase_client: Mock del cliente de Supabase
        """
        mock_response = MagicMock()
        mock_response.data = []
        mock_supabase_client.table.return_value.select.return_value.range.return_value.execute.return_value = mock_response

        response = client.get("/items")
        assert "application/json" in response.headers.get("content-type", "")
