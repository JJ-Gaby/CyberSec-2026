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

| Cambio | Dónde | Función | Resultado |
|---|---|---|---|
| Cambié como se guardan las contraseñas. | `migrar_usuarios.py` y `usuarios.json` | `migrar` usa `crear_hash` para guardar un hash de cada contraseña. | Verifiqué que pude entrar con las dos cuentas. El campo `clave` ya no aparece en el archivo. |
| Añadí una revisión de la contraseña al entrar. | `app.py` | `autenticar` usa `verificar_clave` para revisar la contraseña. | Verifiqué que una clave incorrecta y un usuario que no existe dan el mismo mensaje. En los dos casos vi “Credenciales incorrectas.” y el menú no apareció. |
| Cambié las opciones del menú según la cuenta. | `app.py` | `main` muestra las opciones que tiene cada usuario. | Con `admin` vi la opción de cambiar cantidades. Con `user` pude ver los productos. Al cerrar sesión, el programa me pidió el usuario otra vez. |
| Hice que fuera necesario iniciar sesión para ver el inventario. | `app.py` | `consultar_inventario` revisa si hay una sesión abierta. | Verifiqué que pude ver los productos con `admin` y con `user`. Sin sesión, el programa no mostró la lista. |
| Dejé que solo `admin` pudiera cambiar cantidades. | `app.py` | `modificar_cantidad` revisa el permiso antes de guardar. | Verifiqué que el programa rechazó el cambio de P001 a 99 con `user` y también sin sesión. En los dos casos P001 siguió en 10. |
| Puse un límite a las cantidades. | `app.py` | `validar_cantidad` acepta números enteros de 0 a 1000. | Verifiqué que el programa aceptó 0 y 1000. Rechazó `-1`, `1001`, `abc`, `2.5` y la entrada vacía. Después de cada rechazo, el archivo quedó igual. |
| Añadí un aviso para los productos que no existen. | `app.py` | `modificar_cantidad` busca el producto por su ID. | Cambié P001 de 10 a 20. Después verifiqué que al usar P999 apareció “Producto inexistente.” y P001 siguió en 20. |
| Cambié como se guarda el inventario. | `app.py` e `inventario.json` | `guardar_inventario` guarda los datos primero en un archivo temporal y luego reemplaza el inventario. | Cerré el programa y lo abrí de nuevo. Vi que P001 todavía tenía 20 unidades. |
| Añadí un historial de accesos y cambios. | `app.py` y `auditoria.jsonl` | `registrar_evento` guarda quién hizo el intento, a qué hora y qué pasó. | En el archivo vi un acceso correcto, un acceso fallido, el cambio que hizo `admin` y el intento que se le rechazó a `user`. |
| Añadí avisos cuando hay un problema con el archivo. | `app.py` | `cargar_inventario` avisa si falta el archivo o si no puede leer los datos. | Al quitar el archivo, verifiqué que el programa no creó otro. Cuando escribí `ESTO NO ES JSON`, el texto quedó igual. Al restaurar la copia, pude ver los productos otra vez. |
| Añadí pruebas con copias del inventario. | `pruebas.py` | `ejecutar` prepara una copia y `probar` ejecuta los casos. | Las pruebas pasaron y mi nombre apareció en la terminal. |

Formato de codigo hecho con IA Copilot
