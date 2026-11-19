"""Crea el primer administrador usando variables de entorno (para Render)."""
import os
from contextlib import closing
import sqlite3

from crear_admin import DB_PATH, PATRON
from app.passwords import crear_hash


def crear_administrador_inicial():
    nombre = os.environ.get("STOCKMANAGER_ADMIN_NOMBRE", "").strip()
    usuario = os.environ.get("STOCKMANAGER_ADMIN_USUARIO", "").strip()
    clave = os.environ.get("STOCKMANAGER_ADMIN_PASSWORD", "")
    with closing(sqlite3.connect(DB_PATH, timeout=10)) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")
        ya_existe = conexion.execute("""
            SELECT 1 FROM usuarios u JOIN roles r ON r.id = u.rol_id
            WHERE r.nombre = 'administrador' AND u.activo = 1 LIMIT 1
        """).fetchone()
        if ya_existe:
            return
        if not nombre or not usuario or not clave:
            raise RuntimeError("Configurá las 3 variables STOCKMANAGER_ADMIN_* en Render")
        if len(nombre) > 120 or not PATRON.fullmatch(usuario):
            raise ValueError("Nombre o usuario inicial inválido")
        password_hash = crear_hash(clave)
        with conexion:
            conexion.execute("""
                INSERT INTO usuarios (nombre, usuario, password_hash, rol_id)
                SELECT ?, ?, ?, id FROM roles WHERE nombre='administrador'
            """, (nombre, usuario, password_hash))


if __name__ == "__main__":
    crear_administrador_inicial()
    print("Se verificó la cuenta administradora inicial")
