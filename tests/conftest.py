"""
Configuración de fixtures para pytest.

Este archivo contiene fixtures reutilizables para todos los tests.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app


@pytest.fixture
def client():
    """
    Fixture que proporciona un TestClient de FastAPI.

    Este cliente se puede usar para hacer peticiones HTTP a la aplicación
    sin necesidad de ejecutar un servidor real.

    Yields:
        TestClient: Cliente de prueba configurado con la app de FastAPI
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_supabase_client():
    """
    Fixture que proporciona un cliente mock de Supabase.

    Este mock permite hacer tests sin conectarse a la base de datos real.

    Yields:
        MagicMock: Mock del cliente de Supabase
    """
    with patch('services.item_service.item_service.get_supabase_client') as mock_client:
        mock = MagicMock()
        mock_client.return_value = mock
        yield mock


@pytest.fixture
def sample_item_data():
    """
    Fixture que proporciona datos de ejemplo para un item.

    Returns:
        dict: Datos de ejemplo para crear un item
    """
    return {
        "name": "Test Item",
        "description": "This is a test item",
        "price": 99.99,
        "tax": 21.0
    }


@pytest.fixture
def sample_item_response():
    """
    Fixture que proporciona una respuesta simulada de la base de datos.

    Returns:
        dict: Item completo con ID y metadatos
    """
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Test Item",
        "description": "This is a test item",
        "price": 99.99,
        "tax": 21.0,
        "created_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def sample_items_list():
    """
    Fixture que proporciona una lista de items simulados.

    Returns:
        list: Lista de items para tests de listado
    """
    return [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Item 1",
            "description": "First test item",
            "price": 99.99,
            "tax": 21.0
        },
        {
            "id": "223e4567-e89b-12d3-a456-426614174001",
            "name": "Item 2",
            "description": "Second test item",
            "price": 149.99,
            "tax": 21.0
        },
        {
            "id": "323e4567-e89b-12d3-a456-426614174002",
            "name": "Item 3",
            "description": "Third test item",
            "price": 199.99,
            "tax": 21.0
        }
    ]
