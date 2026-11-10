# Inventario académico

Estudiante: Leyra Bonilla Maldonado

Este programa usa Python 3.10 o posterior. Con admin puedes consultar el inventario y cambiar cantidades de 0 a 1000. Con user puedes consultar los productos.

## Ejecutar

Abre la terminal de Windows en la carpeta del proyecto y ejecuta estos comandos.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python app.py
```

## Cuentas de práctica

- admin / AdminDemo2700!
- user / UserDemo2700!

## Pruebas

En Windows, ejecuta `.\.venv\Scripts\python pruebas.py` y escribe tu nombre. Las pruebas usan una copia del inventario. En el archivo de entrega, P001 tiene 20 unidades.

Usé la base del curso y sus funciones de seguridad.py. Consulté la [documentación de Argon2](https://argon2-cffi.readthedocs.io/en/stable/api.html) para verificar las contraseñas y la [documentación de Python](https://docs.python.org/3/library/json.html) para guardar los datos en JSON.

## Cambios que hice a la base

| Dónde | Qué cambié y cómo lo comprobé |
|---|---|
| `migrar_usuarios.py` y `usuarios.json` | Añadí `migrar` para reemplazar el campo `clave` de las dos cuentas por un hash Argon2id. En la prueba 2 comprobé que cada contraseña funciona con su hash y que el campo anterior ya no aparece. |
| `seguridad.py` y `requirements.txt` | Usé las funciones de la base para crear y verificar los hashes. En `seguridad.py` solo acorté el comentario sobre el salt. La dependencia argon2-cffi ya venía en la base. |
| `app.py`, `autenticar` y `main` | Añadí la verificación del hash y el registro de cada intento. El menú muestra la opción de modificar a admin y oculta la contraseña al escribirla en la terminal. La prueba 3 comprueba cuándo aparece el menú. |
| `app.py`, `consultar_inventario` y `modificar_cantidad` | Comprobé la sesión dentro de ambas funciones y exigí el rol admin para escribir. En la prueba 4, user pidió cambiar P001 a 99 directamente desde un script. El archivo siguió igual. También probé ambas funciones sin sesión. |
| `app.py`, `validar_cantidad` y `modificar_cantidad` | Añadí la validación antes de guardar y un aviso cuando el ID no existe. La prueba 5 revisa cinco entradas inválidas y los límites 0 y 1000. La prueba 6 comprueba que P999 no cambia ningún producto. |
| `app.py`, `guardar_inventario`, e `inventario.json` | Cambié la escritura para guardar primero en un temporal. En el inventario final, P001 pasó de 10 a 20. La prueba 7 abre el programa de nuevo y lee las 20 unidades. |
| `app.py`, `registrar_evento`, y `auditoria.jsonl` | Añadí un registro por línea con la fecha y hora, el usuario, la acción y el resultado. Para los cambios incluí el producto y las dos cantidades. La muestra contiene eventos reales de las pruebas. La prueba 8 comprueba los cuatro tipos de evento pedidos. |
| `app.py`, `cargar_inventario` | Añadí avisos para el archivo ausente y el JSON inválido. La prueba 9 intenta consultar y modificar en ambos casos y después recupera el respaldo. |
| `pruebas.py` | Añadí el script que ejecuta los casos 2 a 9 en copias temporales e imprime el nombre del estudiante. En el apartado 10 también ejecuté el programa desde una copia del repositorio. |
| `.gitignore` y `README.md` | Añadí reglas para excluir el entorno virtual, la caché de Python y los temporales. Actualicé las instrucciones para instalar, ejecutar y probar el programa. |

Formato de codigo hecho con IA Copilot
