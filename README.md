# Sistema de Gestión de Pedidos - Pruebas y CI

Este repositorio contiene la implementación de reglas de negocio, persistencia y seguridad para un sistema de pedidos, respaldado por una suite completa de pruebas automatizadas y un pipeline de Integración Continua (CI).

## E9 · Reglas y pruebas del PIA FerreMax

La [carpeta E9](E9/README.md) reúne las tres reglas reales de FerreMax, sus decisiones de diseño y las evidencias de la ejecución del 5 de noviembre de 2026: **9/9 casos de negocio, 6/6 pruebas de PostgreSQL y 3/3 pruebas con mock aprobadas**. La suite de regresión de esa versión registra **38 pruebas aprobadas, sin fallos, errores ni omisiones**.

- [Matriz de los nueve casos y sus resultados](E9/matriz_e9.csv).
- [Resumen de cobertura y alcance de cada medición](E9/resumen_cobertura.md): **94.09 %** en los cuatro componentes de E9 y **92.04 %** en todo `src` con la regresión.
- [Guía de revisión y comandos para reproducir FerreMax](E9/README.md), con el enlace al commit exacto del código probado.

Los resultados se pueden consultar directamente en GitHub. Para navegar los reportes HTML, descargar y descomprimir el repositorio completo, y abrir `E9/htmlcov/index.html` o `E9/htmlcov_global/index.html`. Las capturas se incorporan en el reporte de U5.

## Arquitectura del Proyecto

El sistema está diseñado utilizando principios de separación de responsabilidades, dividiendo el código en módulos específicos dentro de la carpeta `src/`:

*   **Dominio (`domain.py`)**: Contiene las reglas de negocio principales, como la validación de totales positivos, la aplicación de descuentos a clientes VIP y las transiciones de estado de los pedidos.
*   **Aplicación (`application.py`)**: Coordina los casos de uso. Aquí se implementa el servicio de cobros (`OrderService`), el cual interactúa con pasarelas de pago externas.
*   **Persistencia (`repository.py`)**: Maneja la interacción con la base de datos utilizando SQLAlchemy. Implementa los límites transaccionales (`commit` y `rollback`) para garantizar la consistencia de los datos sin afectar entornos de producción.
*   **Seguridad (`security.py`)**: Define las políticas de autorización, validando qué usuarios (administradores o propietarios) tienen los permisos y el tiempo permitido para cancelar un pedido.

## Instalación y Configuración

Para preparar el entorno local y ejecutar las pruebas del laboratorio U5 (ejemplo para Windows PowerShell), ejecuta los siguientes comandos en la raíz del proyecto. Para reproducir las pruebas de FerreMax correspondientes a E9, sigue la [guía de E9](E9/README.md).

1. Crear el entorno virtual:

   ```powershell
   py -3.11 -m venv .venv
   ```

2. Activar el entorno virtual:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Instalar las dependencias requeridas:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Ejecutar pruebas unitarias:

   ```powershell
   python -m pytest -v
   ```

5. Revisar el formato y estilo del código:

   ```powershell
   python -m ruff check src tests
   ```

6. Medir la cobertura del código, esperando al menos 80 %:

   ```powershell
   python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
   ```
