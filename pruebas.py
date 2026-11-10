"""Ejecutar con python pruebas.py. Usa solo copias temporales de datos ficticios."""
import json
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


#Abro otro proceso para probar el menú y comprobar qué queda guardado después de cerrar el programa.
def cli(carpeta, nombre, *entradas):
    proceso = subprocess.run(
        [sys.executable, "app.py"], cwd=carpeta,
        input="\n".join((nombre, *entradas)) + "\n", capture_output=True,
        text=True, encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=True, timeout=15)
    assert not proceso.stderr, proceso.stderr
    return proceso.stdout


#Las pruebas empiezan con P001 en 10 y comparan el archivo antes y después de cada cambio rechazado.
def probar(carpeta, nombre, destino_log=None):
    from seguridad import verificar_clave

    spec = importlib.util.spec_from_file_location("inventario_prueba", carpeta / "app.py")
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)
    inventario = app.DATOS
    datos = app.cargar_inventario()
    datos[0]["cantidad"] = 10
    app.guardar_inventario(datos)

    def titulo(numero):
        print(f"\nApartado {numero} | Estudiante: {nombre}")

    def p001():
        return next(p["cantidad"] for p in app.cargar_inventario() if p["id"] == "P001")

    claves = {"admin": "AdminDemo2700!", "user": "UserDemo2700!"}
    titulo(2)
    for u in json.loads(app.USUARIOS.read_text()):
        assert "clave" not in u and u["hash"].startswith("$argon2id$")
        assert verificar_clave(u["hash"], claves[u["usuario"]])
        print(u["usuario"], "| Argon2id verificado | campo clave ausente")

    titulo(3)
    for usuario, clave, valido in [("admin", claves["admin"], True),
                                   ("admin", "incorrecta", False),
                                   ("nadie", "incorrecta", False)]:
        salida = cli(carpeta, nombre, usuario, clave, "0" if valido else "salir")
        menu = "1. Consultar" in salida
        assert menu == valido
        assert ("Credenciales incorrectas." in salida) == (not valido)
        print(usuario, "|", "clave correcta" if valido else "credenciales inválidas",
              "|", "menú visible" if menu else "Credenciales incorrectas. | sin menú")

    titulo(4)
    sesion = app.autenticar("user", claves["user"])
    assert sesion is not None
    antes = inventario.read_bytes()
    for identificador, actor in [("user", sesion), ("sin_sesion", None)]:
        assert not app.modificar_cantidad(actor, "P001", "99")
        assert antes == inventario.read_bytes()
        print(identificador, "| P001 -> 99 | P001 en disco:", p001(), "| archivo idéntico")
    assert not app.consultar_inventario(None)
    print("consulta(None) | rechazada")

    titulo(5)
    admin = app.autenticar("admin", claves["admin"])
    assert admin is not None
    for entrada in ["-1", "1001", "abc", "2.5", "", "0", "1000"]:
        antes = inventario.read_bytes()
        aceptada = app.modificar_cantidad(admin, "P001", entrada)
        assert aceptada == (entrada in ("0", "1000"))
        if aceptada:
            assert p001() == int(entrada)
        else:
            assert inventario.read_bytes() == antes
        print(repr(entrada), "|", "aceptada" if aceptada else "rechazada",
              "| P001:", p001(), "|", "guardado" if aceptada else "archivo idéntico")
    assert app.modificar_cantidad(admin, "P001", "10") and p001() == 10
    print("Restauración verificada | P001:", p001())

    titulo(6)
    for usuario in ("admin", "user"):
        salida = cli(carpeta, nombre, usuario, claves[usuario], "1", "0")
        assert "P001 Teclado 10" in salida
        print(usuario, "| consulta | P001 Teclado 10")
    salida = cli(carpeta, nombre, "admin", claves["admin"], "2", "P001", "20", "0")
    assert "Cantidad actualizada." in salida and p001() == 20
    print("admin | P001: 10 ->", p001(), "| proceso finalizado")
    antes = inventario.read_bytes()
    salida = cli(carpeta, nombre, "admin", claves["admin"], "2", "P999", "77", "0")
    assert "Producto inexistente." in salida and inventario.read_bytes() == antes
    print("P999 -> 77 | Producto inexistente. | archivo idéntico")

    titulo(7)
    salida = cli(carpeta, nombre, "user", claves["user"], "1", "0")
    assert "P001 Teclado 20" in salida
    print("Nuevo proceso de app.py | consulta:", "P001 Teclado 20")
    print("Archivo:", json.dumps(app.cargar_inventario()[0], ensure_ascii=False))

    titulo(8)
    texto = app.LOG.read_text(encoding="utf-8")
    eventos = [json.loads(linea) for linea in texto.splitlines()]
    requeridos = [("login", "exitoso"), ("login", "fallido"),
                  ("modificar", "exitoso"), ("modificar", "rechazado_por_permisos")]
    for accion, resultado in requeridos:
        assert any(e["accion"] == accion and e["resultado"] == resultado for e in eventos)
        print(accion, "|", resultado, "| presente")
    assert all(v not in texto for v in [*claves.values(), "incorrecta", "$argon2"])
    print(len(eventos), "líneas JSON verificadas; sin las claves de prueba ni hashes")
    if destino_log:
        shutil.copyfile(app.LOG, destino_log)

    titulo(9)
    respaldo = carpeta / "inventario.respaldo"
    inventario.rename(respaldo)
    try:
        for modo in ("ausente", "inválido"):
            if modo == "inválido":
                inventario.write_bytes(b"ESTO NO ES JSON")
            salida = cli(carpeta, nombre, "admin", claves["admin"],
                         "1", "2", "P001", "99", "0")
            mensaje = ("Falta inventario.json." if modo == "ausente"
                       else "inventario.json contiene JSON inválido.")
            assert salida.count(mensaje) == 2
            assert (not inventario.exists() if modo == "ausente"
                    else inventario.read_bytes() == b"ESTO NO ES JSON")
            print("Consulta y modificación |", mensaje)
            print("Archivo sigue ausente." if modo == "ausente"
                  else "Contenido intacto: ESTO NO ES JSON")
    finally:
        respaldo.replace(inventario)
    assert app.consultar_inventario(sesion) and p001() == 20
    print("Respaldo restaurado | consulta correcta")


#Copio el programa y los datos en una carpeta temporal para probar errores sin tocar el inventario de entrega.
def ejecutar(nombre, destino_log=None):
    with TemporaryDirectory() as temporal:
        carpeta = Path(temporal)
        for archivo in ("app.py", "seguridad.py", "usuarios.json", "inventario.json"):
            shutil.copyfile(Path(__file__).with_name(archivo), carpeta / archivo)
        probar(carpeta, nombre, destino_log)


if __name__ == "__main__":
    ejecutar(input("Nombre del estudiante: "))
