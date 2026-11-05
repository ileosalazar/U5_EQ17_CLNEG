# E9 · Reglas y pruebas del PIA FerreMax

**Responsable de E9:** Roberto Santana Trujillo. Esta carpeta reúne las evidencias de las tres reglas reales de FerreMax elegidas para E9 de la Unidad 5.

## Resultado de la ejecución

Ejecución del **5 de noviembre de 2026, 16:41 h de Monterrey** (22:41 UTC), correspondiente a las capturas del reporte de U5.

| Verificación | Resultado |
| --- | --- |
| Casos de las tres reglas: éxito, error y límite | **9/9 aprobados** |
| Persistencia y concurrencia con PostgreSQL real | **6/6 aprobadas** |
| Ejercicio separado de pagos con mock | **3/3 aprobadas** |
| Bloque E9 completo | **18 aprobadas** |
| Suite de regresión de la versión probada | **38 aprobadas, 0 fallidas, 0 errores, 0 omitidas** |
| Cobertura de líneas de los cuatro componentes pertinentes de E9 | **94.09 % (366/389)** |
| Cobertura de todo `src` con el bloque E9 | **89.03 % (414/465)** |
| Cobertura de todo `src` con la suite de regresión | **92.04 % (428/465)** |

Las 18 pruebas de E9 forman parte de las 38 de regresión; no se suman como 56 pruebas. La cobertura mide líneas ejecutadas, no demuestra por sí sola la corrección de todas las condiciones o ramas.

El código probado está en [FerreMax, commit `cda5b32905c63567767b426a3c9777ef9d2cb027`](https://github.com/Santana-R/ferremax-u3/tree/cda5b32905c63567767b426a3c9777ef9d2cb027). Este enlace identifica el **código fuente** utilizado; para consultar los resultados de esta ejecución, usar los archivos de esta carpeta. Los avances posteriores del PIA se revisan por separado.

## Cómo revisar las evidencias desde U5

1. Leer las reglas y los nueve casos de las tablas siguientes.
2. Abrir la [matriz CSV completa](matriz_e9.csv): relaciona regla, historia, tipo de caso, entrada, resultado esperado, resultado real, estado, prueba, commit y fecha.
3. Revisar el [resumen de cobertura](resumen_cobertura.md), la [salida del bloque E9](ejecucion_e9.txt) y la [salida de regresión](ejecucion_regresion.txt).
4. Para ver los informes HTML como páginas navegables, descargar este repositorio mediante **Code → Download ZIP**, descomprimirlo y abrir `E9/htmlcov/index.html` y `E9/htmlcov_global/index.html`. Deben conservarse las carpetas completas, con sus CSS, JavaScript e imágenes. GitHub muestra el código del HTML al abrirlo directamente.

Los resultados y su resumen se pueden leer aquí mismo en GitHub. El repositorio FerreMax permite examinar las implementaciones y volver a ejecutar las pruebas. Las capturas se incorporan en el reporte de U5 a cargo de Isaías.

## Tres reglas y sus nueve casos

| Regla | Trazabilidad | Decisión comprobada |
| --- | --- | --- |
| Confirmar un pedido reserva solo el inventario disponible. | BR04/BR05 · US09 | Disponible = existencia física − reservas comprometidas. El inventario en tránsito no se ofrece como disponible. |
| Revalidar una cotización vencida conserva el historial. | BR02/BR03 · US04/US05 | La revalidación crea una nueva versión; el pedido usa la versión aceptada y vigente. Exactamente al vencer, la cotización ya no permite conversión. |
| Cancelar antes del surtido libera la reserva propia. | BR06 · US10 | La cancelación autorizada libera solo la reserva de ese pedido. Un pedido surtido o ya cancelado rechaza otra cancelación. |

| Caso | Tipo | Entrada o condición | Resultado observado |
| --- | --- | --- | --- |
| E9-INV-01 | Éxito | 10 unidades físicas, 7 comprometidas; solicitar 2. | Pedido confirmado; 9 comprometidas y 1 disponible. Conserva las 7 de otro pedido. |
| E9-INV-02 | Error | Mismo inventario; solicitar 4 cuando solo hay 3 disponibles. | Rechazo por disponibilidad; pedido pendiente e inventario intacto. |
| E9-INV-03 | Límite | Solicitar exactamente las 3 disponibles. | Pedido confirmado; disponibilidad final de 0. |
| E9-COT-01 | Éxito | Revalidar la versión 1 vencida, actualizar precio de 100 a 120 MXN y aceptar la versión 2 por 2 unidades. | Versión 1 intacta; pedido ligado a la versión 2, total 240 MXN, sin reserva de inventario. |
| E9-COT-02 | Error | Convertir a las 12:01 UTC una versión vencida a las 12:00 UTC. | Rechazo por vencimiento; no crea pedido ni modifica los datos. |
| E9-COT-03 | Límite | Intentar convertir exactamente a las 12:00 UTC, instante de vencimiento. | Rechazo por vencimiento; no crea pedido ni modifica los datos. |
| E9-CAN-01 | Éxito | Cancelar un pedido confirmado y no surtido con reserva propia de 2 y 7 ajenas. | Pedido cancelado; libera 2, conserva las 7 ajenas y registra auditoría y evento. |
| E9-CAN-02 | Error | Intentar cancelar un pedido ya surtido. | Rechazo; conserva estado, reservas y eventos. |
| E9-CAN-03 | Límite | Intentar cancelar nuevamente un pedido ya cancelado. | Rechazo; no vuelve a liberar inventario ni duplica el evento de cancelación. |

Los nueve casos aprobaron. La [matriz CSV](matriz_e9.csv) y las [observaciones de ejecución](observaciones_e9.json) conservan los resultados detallados. Las reglas se relacionan con el [BRD y las historias del proyecto](https://github.com/Santana-R/ferremax-u3/tree/cda5b32905c63567767b426a3c9777ef9d2cb027/reference).

## Pruebas complementarias

### PostgreSQL real: seis pruebas

Se usó una instancia PostgreSQL 16.2 temporal, con un socket Unix privado y TCP desactivado. El generador crea el esquema de pruebas y detiene la instancia al terminar.

| Prueba | Comprobación |
| --- | --- |
| Persistencia 01 | Un pedido con commit se recupera desde otra conexión. |
| Persistencia 02 | Al cerrar sin commit, el rollback impide conservar la cotización. |
| Persistencia 03 | Si falla un segundo SKU sin stock, revierte el estado del pedido y la primera reserva. |
| Persistencia 04 | Confirmación y cancelación conservan en PostgreSQL las reservas, auditoría y eventos correspondientes. |
| Persistencia 05 | La revalidación conserva ambas versiones y el pedido ligado a la versión nueva. |
| Concurrencia | Dos conexiones compiten por la última unidad: solo una confirma y la otra se rechaza. |

Implementaciones ejecutables: [cinco pruebas de persistencia](https://github.com/Santana-R/ferremax-u3/blob/cda5b32905c63567767b426a3c9777ef9d2cb027/tests/test_e9_persistencia.py) y [prueba de concurrencia](https://github.com/Santana-R/ferremax-u3/blob/cda5b32905c63567767b426a3c9777ef9d2cb027/tests/test_postgres.py).

### Mock de pagos: tres pruebas

FerreMax aún no tiene una integración operativa con un proveedor externo de pagos. Se justifica esa ausencia con un ejercicio separado que utiliza el puerto `ProveedorPago` y un adaptador simulado en `examples/`. El mock sustituye al proveedor y se verifica una sola llamada por 200 MXN. No hay cobros reales ni llamadas de red.

| Respuesta simulada | Resultado |
| --- | --- |
| Aprobación | Confirma el pedido y reserva inventario. |
| Rechazo | Mantiene el pedido pendiente y sus datos intactos. |
| Tiempo de espera agotado (`TimeoutError`) | Mantiene el pedido pendiente y sus datos intactos. |

Consultar las [pruebas con Mock](https://github.com/Santana-R/ferremax-u3/blob/cda5b32905c63567767b426a3c9777ef9d2cb027/tests/test_e9_adaptador_simulado.py), el [adaptador simulado](https://github.com/Santana-R/ferremax-u3/blob/cda5b32905c63567767b426a3c9777ef9d2cb027/examples/e9_pago_simulado.py) y las [observaciones complementarias](complementarias_e9.json).

## Decisiones de diseño

- Cada caso usa datos ficticios, fechas UTC fijas y un contexto nuevo para que el resultado sea reproducible.
- Los importes se representan con `Decimal`. La vigencia de siete días es un parámetro simulado del BRD; el instante de vencimiento queda excluido.
- Revalidar o convertir una cotización no reserva inventario. La reserva ocurre al confirmar el pedido.
- El Unit of Work coordina las modificaciones del pedido, las reservas, la auditoría y los eventos; los rechazos deben conservar los datos anteriores.
- Se comprueba tanto el estado resultante como la conservación del historial y de las reservas ajenas. La matriz se genera a partir de los resultados observados, sin sustituirlos por las expectativas.
- El caso de cancelación repetida detectó un problema en el orden de validación: se buscaba una reserva ya liberada antes de validar el estado del pedido. Se corrigió el orden para rechazar por la regla de cancelación sin liberar ni registrar un evento adicional.

## Archivos incluidos

| Archivo o carpeta | Uso |
| --- | --- |
| [matriz_e9.csv](matriz_e9.csv) | Trazabilidad y resultados de los nueve casos de negocio. |
| [observaciones_e9.json](observaciones_e9.json) | Estados, versiones, reservas, eventos, auditoría y rechazos observados. |
| [complementarias_e9.json](complementarias_e9.json) | Observaciones de PostgreSQL, concurrencia y mock. |
| [resumen_e9.json](resumen_e9.json) | Fecha, commit, hashes SHA-256 del código, conteos y estado de la ejecución. |
| [resumen_cobertura.md](resumen_cobertura.md) | Resumen generado de los tres alcances de cobertura. |
| [ejecucion_e9.txt](ejecucion_e9.txt) | Salida real de las 18 pruebas del bloque E9. |
| [ejecucion_regresion.txt](ejecucion_regresion.txt) y [regresion.xml](regresion.xml) | Resultados de las 38 pruebas de regresión. |
| [cobertura_e9.json](cobertura_e9.json), [cobertura_e9_todo_src.json](cobertura_e9_todo_src.json), [cobertura_global.json](cobertura_global.json) | Datos de cobertura de los tres alcances declarados. |
| [htmlcov/](htmlcov/index.html) | Informe HTML de los cuatro componentes pertinentes de E9. |
| [htmlcov_global/](htmlcov_global/index.html) | Informe HTML de todo `src` con la regresión. |

El mensaje de incorporación pendiente que conserva `resumen_cobertura.md` fue emitido por el generador antes de subir estas evidencias a U5. Es parte de la salida original de esa ejecución; esta carpeta contiene la incorporación.

## Reproducir la versión probada

Requisitos: Git y Python 3.11 con `venv` y `pip`. Los binarios de PostgreSQL temporal se instalan mediante `pgserver`, fijado en `requirements-e9.txt`. Ejecutar en una terminal local con permisos para iniciar procesos.

En macOS/Linux, desde una carpeta donde se desee crear una copia independiente:

```bash
git clone https://github.com/Santana-R/ferremax-u3.git ferremax-e9-reproduccion
cd ferremax-e9-reproduccion
git checkout --detach cda5b32905c63567767b426a3c9777ef9d2cb027
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements-e9.txt
.venv/bin/python scripts/generar_e9.py --postgres-temporal
```

En Windows PowerShell, los tres primeros comandos Git son iguales. Después:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-e9.txt
.\.venv\Scripts\python.exe scripts/generar_e9.py --postgres-temporal
```

Los comandos de Windows se proporcionan como referencia; esta evidencia se obtuvo en macOS. El generador utiliza una base temporal de pruebas, y la cierra al finalizar. Los nuevos resultados se escriben en `evidencias/e9/` de esa copia de FerreMax. La salida esperada es `9/9 PASSED`, `38 PASSED, 0 SKIPPED`, `PostgreSQL real: 6/6`, `mocks: 3/3` y `E9 COMPLETA`.

Si falta la conexión PostgreSQL, las pruebas aparecen omitidas y no acreditan persistencia. Deben resolverse las causas antes de presentar esa nueva ejecución como completa.
