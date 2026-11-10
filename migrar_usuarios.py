"""Migración única de las cuentas ficticias suministradas."""
import json
from pathlib import Path
from seguridad import crear_hash


def migrar(ruta):
    usuarios = json.loads(ruta.read_text(encoding="utf-8"))
    if not any("clave" in usuario for usuario in usuarios):
        return
    for usuario in usuarios:
        if "clave" in usuario:
            usuario["hash"] = crear_hash(usuario.pop("clave"))
    temporal = ruta.with_suffix(".tmp")
    temporal.write_text(json.dumps(usuarios, indent=2) + "\n", encoding="utf-8")
    temporal.replace(ruta)


if __name__ == "__main__":
    migrar(Path(__file__).resolve().with_name("usuarios.json"))

