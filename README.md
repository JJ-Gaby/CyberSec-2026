# Inventario académico

Estudiante: Leyra Bonilla Maldonado

Aplicación de terminal en Python 3.10 o posterior. La cuenta admin consulta y modifica cantidades de 0 a 1000. La cuenta user solo consulta.

## Ejecutar

Desde la carpeta del proyecto, en la terminal de Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python app.py
```

En macOS o Linux, use `.venv/bin/python` en los dos últimos comandos. La dependencia es argon2-cffi.

## Cuentas de práctica

- admin / AdminDemo2700!
- user / UserDemo2700!

## Pruebas

Ejecute `python pruebas.py` con el Python del entorno e introduzca su nombre. Las pruebas usan copias temporales. El inventario de entrega tiene P001 en 20. auditoria.jsonl incluye eventos de ejemplo de una ejecución real.
