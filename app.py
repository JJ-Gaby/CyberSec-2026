"""Inventario académico de COMP 2700."""
import json
import sys
from datetime import datetime, timezone
from getpass import getpass
from pathlib import Path

from seguridad import verificar_clave

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "inventario.json"
USUARIOS = RAIZ / "usuarios.json"
LOG = RAIZ / "auditoria.jsonl"


def cargar_inventario():
    try:
        return json.loads(DATOS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("Falta inventario.json. Restaure la copia de respaldo.")
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("inventario.json contiene JSON inválido. Revise el archivo.")
    return None


def guardar_inventario(productos):
    temporal = DATOS.with_suffix(".tmp")
    texto = json.dumps(productos, indent=2, ensure_ascii=False)
    temporal.write_text(texto + "\n", encoding="utf-8")
    temporal.replace(DATOS)


def registrar_evento(usuario, accion, resultado, *, producto=None,
                     anterior=None, nueva=None):
    evento = {"fecha_hora": datetime.now(timezone.utc).isoformat(),
              "usuario": usuario, "accion": accion, "resultado": resultado}
    if producto is not None:
        evento.update(producto=producto, anterior=anterior, nueva=nueva)
    with LOG.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")


def autenticar(nombre, clave):
    usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))
    for usuario in usuarios:
        if usuario["usuario"] == nombre and verificar_clave(usuario["hash"], clave):
            registrar_evento(nombre, "login", "exitoso")
            return {"usuario": nombre, "rol": usuario["rol"]}
    registrar_evento(nombre, "login", "fallido")
    print("Credenciales incorrectas.")
    return None


def consultar_inventario(sesion):
    if not sesion or sesion.get("rol") not in ("admin", "user"):
        print("Se requiere una sesión válida.")
        return False
    productos = cargar_inventario()
    if productos is None:
        return False
    for producto in productos:
        print(producto["id"], producto["nombre"], producto["cantidad"])
    return True


def validar_cantidad(entrada):
    texto = str(entrada).strip()
    if not texto.isascii() or not texto.isdecimal():
        return None
    cifras = texto.lstrip("0") or "0"
    if len(cifras) > 4:
        return None
    cantidad = int(cifras)
    return cantidad if cantidad <= 1000 else None


def modificar_cantidad(sesion, identificador, entrada):
    cantidad = validar_cantidad(entrada)
    if not sesion or sesion.get("rol") != "admin":
        usuario = sesion["usuario"] if sesion else "sin_sesion"
        productos = cargar_inventario() or []
        anterior = None
        for producto in productos:
            if producto["id"] == identificador:
                anterior = producto["cantidad"]
                break
        registrar_evento(usuario, "modificar", "rechazado_por_permisos",
                         producto=identificador, anterior=anterior, nueva=cantidad)
        print("Modificación rechazada por falta de autorización.")
        return False
    if cantidad is None:
        print("Cantidad inválida. Escriba un entero de 0 a 1000.")
        return False
    productos = cargar_inventario()
    if productos is None:
        return False
    for producto in productos:
        if producto["id"] == identificador:
            anterior = producto["cantidad"]
            producto["cantidad"] = cantidad
            guardar_inventario(productos)
            registrar_evento(sesion["usuario"], "modificar", "exitoso",
                             producto=identificador, anterior=anterior, nueva=cantidad)
            print("Cantidad actualizada.")
            return True
    print("Producto inexistente.")
    return False


def main():
    print("Inventario académico")
    print("Estudiante:", input("Escriba su nombre: "))
    sesion = None
    while True:
        if sesion is None:
            nombre = input("Usuario (o salir): ")
            if nombre == "salir":
                break
            leer_clave = getpass if sys.stdin.isatty() else input
            sesion = autenticar(nombre, leer_clave("Contraseña de prueba: "))
            continue
        opciones = "1. Consultar"
        if sesion["rol"] == "admin":
            opciones += " | 2. Modificar"
        print(opciones + " | 3. Cerrar sesión | 0. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            consultar_inventario(sesion)
        elif opcion == "2":
            identificador = input("ID del producto: ")
            entrada = input("Nueva cantidad: ")
            modificar_cantidad(sesion, identificador, entrada)
        elif opcion == "3":
            sesion = None
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()

