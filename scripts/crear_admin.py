"""Pide los datos y crea la primera cuenta administradora."""
import getpass
from pathlib import Path
import re
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.passwords import crear_hash  # noqa: E402
from scripts.inicializar_db import inicializar  # noqa: E402

DB_PATH = ROOT / "instance" / "StockManager.db"
PATRON = re.compile(r"[A-Za-z][A-Za-z0-9_.-]{2,31}\Z")


def main() -> None:
    inicializar()
    nombre = input("Nombre completo: ").strip()
    usuario = input("Usuario: ").strip()
    if not 1 <= len(nombre) <= 120 or not PATRON.fullmatch(usuario):
        raise SystemExit("Nombre o nombre de usuario inválido")
    clave = getpass.getpass("Contraseña (mínimo 12 caracteres): ")
    repetida = getpass.getpass("Repetir contraseña: ")
    if clave != repetida:
        raise SystemExit("Las contraseñas no coinciden")
    try:
        password_hash = crear_hash(clave)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    try:
        with sqlite3.connect(DB_PATH, timeout=10) as conexion:
            conexion.execute("PRAGMA foreign_keys=ON")
            cursor = conexion.execute("""
                INSERT INTO usuarios (nombre, usuario, password_hash, rol_id)
                SELECT ?, ?, ?, id FROM roles WHERE nombre='administrador'
            """, (nombre, usuario, password_hash))
            if cursor.rowcount != 1:
                raise RuntimeError("Falta el rol administrador")
    except sqlite3.IntegrityError as exc:
        raise SystemExit("No se pudo crear: el nombre de usuario ya existe") from exc
    print("Cuenta administrador creada:", usuario)


if __name__ == "__main__":
    main()
