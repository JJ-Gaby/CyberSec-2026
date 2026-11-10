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

En macOS o Linux, usa `.venv/bin/python` en los dos últimos comandos. La dependencia es argon2-cffi.

## Cuentas de práctica

- admin / AdminDemo2700!
- user / UserDemo2700!

## Pruebas

En Windows, ejecuta `.\.venv\Scripts\python pruebas.py` y escribe tu nombre. Las pruebas usan una copia del inventario. En el archivo de entrega, P001 tiene 20 unidades.

Usé la base del curso y sus funciones de seguridad.py. Consulté la [documentación de Argon2](https://argon2-cffi.readthedocs.io/en/stable/api.html) para verificar las contraseñas y la [documentación de Python](https://docs.python.org/3/library/json.html) para guardar los datos en JSON.
