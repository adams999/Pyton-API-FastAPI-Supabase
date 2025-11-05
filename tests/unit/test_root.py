"""
Unit tests para el endpoint root de la aplicación.

Tests básicos que verifican el funcionamiento del endpoint raíz.
"""

from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Tests para el endpoint raíz de la API"""

    def test_root_endpoint_returns_200(self, client: TestClient):
        """
        Test que verifica que el endpoint root retorna status code 200.

        Args:
            client: TestClient fixture de FastAPI
        """
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_returns_json(self, client: TestClient):
        """
        Test que verifica que el endpoint root retorna JSON.

        Args:
            client: TestClient fixture de FastAPI
        """
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"

    def test_root_endpoint_returns_message(self, client: TestClient):
        """
        Test que verifica que el endpoint root retorna el mensaje esperado.

        Args:
            client: TestClient fixture de FastAPI
        """
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World - Connected to Supabase"

    def test_root_endpoint_structure(self, client: TestClient):
        """
        Test que verifica la estructura completa de la respuesta.

        Args:
            client: TestClient fixture de FastAPI
        """
        response = client.get("/")
        data = response.json()

        # Verificar que la respuesta es un diccionario
        assert isinstance(data, dict)

        # Verificar que solo tiene el campo esperado
        assert len(data) == 1
        assert "message" in data
