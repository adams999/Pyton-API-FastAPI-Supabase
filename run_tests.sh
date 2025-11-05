#!/bin/bash
# Script para ejecutar tests en Linux/MacOS

echo "========================================"
echo " Ejecutando Tests - FastAPI + Supabase"
echo "========================================"
echo ""

# Activar entorno virtual si existe
if [ -f "venv/bin/activate" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

# Verificar que pytest está instalado
if ! python -c "import pytest" 2>/dev/null; then
    echo "ERROR: pytest no está instalado"
    echo "Por favor ejecuta: pip install -r requirements-test.txt"
    exit 1
fi

echo "Tests disponibles:"
echo "  1. Todos los tests"
echo "  2. Solo tests unitarios"
echo "  3. Solo tests de integración"
echo "  4. Tests con cobertura"
echo "  5. Tests verbose"
echo ""

read -p "Selecciona una opción (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Ejecutando todos los tests..."
        pytest
        ;;
    2)
        echo ""
        echo "Ejecutando solo tests unitarios..."
        pytest tests/unit/ -m "not integration"
        ;;
    3)
        echo ""
        echo "Ejecutando tests de integración..."
        pytest tests/integration/ -m integration
        ;;
    4)
        echo ""
        echo "Ejecutando tests con reporte de cobertura..."
        pytest --cov=. --cov-report=html --cov-report=term
        echo ""
        echo "Reporte HTML generado en: htmlcov/index.html"
        ;;
    5)
        echo ""
        echo "Ejecutando tests en modo verbose..."
        pytest -vv
        ;;
    *)
        echo "Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo " Tests completados"
echo "========================================"
