# Sistema de Gestión de Pedidos - Pruebas y CI

Este repositorio contiene la implementación de reglas de negocio, persistencia y seguridad para un sistema de pedidos, respaldado por una suite completa de pruebas automatizadas y un pipeline de Integración Continua (CI).

## Arquitectura del Proyecto

El sistema está diseñado utilizando principios de separación de responsabilidades, dividiendo el código en módulos específicos dentro de la carpeta `src/`:

*   **Dominio (`domain.py`)**: Contiene las reglas de negocio principales, como la validación de totales positivos, la aplicación de descuentos a clientes VIP y las transiciones de estado de los pedidos.
*   **Aplicación (`application.py`)**: Coordina los casos de uso. Aquí se implementa el servicio de cobros (`OrderService`), el cual interactúa con pasarelas de pago externas.
*   **Persistencia (`repository.py`)**: Maneja la interacción con la base de datos utilizando SQLAlchemy. Implementa los límites transaccionales (`commit` y `rollback`) para garantizar la consistencia de los datos sin afectar entornos de producción.
*   **Seguridad (`security.py`)**: Define las políticas de autorización, validando qué usuarios (administradores o propietarios) tienen los permisos y el tiempo permitido para cancelar un pedido.

## Instalación y Configuración

Para preparar el entorno local (ejemplo para Windows PowerShell), ejecuta los siguientes comandos en la raíz del proyecto:

1. Crear el entorno virtual:
   ```bash
   py -3.11 -m venv .venv

2. Activar el entorno virtual:
   ```bash
   .\.venv\Scripts\Activate.ps1

3. Instalar las dependencias requeridas:
    ```bash
    python -m pip install -r requirements.txt

4. Ejecutar pruebas unitarias:
    ```bash
    python -m pytest -v

5. Revisar el formato y estilo del código:
    ```bash
    python -m ruff check src tests

6. Medir la cobertura del código, esperando al menos 80%
    ```bash
    python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80