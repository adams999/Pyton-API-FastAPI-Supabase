@echo off
REM Script para ejecutar tests en Windows

echo ========================================
echo  Ejecutando Tests - FastAPI + Supabase
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Verificar que pytest está instalado
python -c "import pytest" 2>nul
if errorlevel 1 (
    echo ERROR: pytest no está instalado
    echo Por favor ejecuta: pip install -r requirements-test.txt
    exit /b 1
)

echo Tests disponibles:
echo   1. Todos los tests
echo   2. Solo tests unitarios
echo   3. Solo tests de integración
echo   4. Tests con cobertura
echo   5. Tests verbose
echo.

set /p choice="Selecciona una opción (1-5): "

if "%choice%"=="1" (
    echo.
    echo Ejecutando todos los tests...
    pytest
) else if "%choice%"=="2" (
    echo.
    echo Ejecutando solo tests unitarios...
    pytest tests/unit/ -m "not integration"
) else if "%choice%"=="3" (
    echo.
    echo Ejecutando tests de integración...
    pytest tests/integration/ -m integration
) else if "%choice%"=="4" (
    echo.
    echo Ejecutando tests con reporte de cobertura...
    pytest --cov=. --cov-report=html --cov-report=term
    echo.
    echo Reporte HTML generado en: htmlcov\index.html
) else if "%choice%"=="5" (
    echo.
    echo Ejecutando tests en modo verbose...
    pytest -vv
) else (
    echo Opción inválida
    exit /b 1
)

echo.
echo ========================================
echo  Tests completados
echo ========================================
