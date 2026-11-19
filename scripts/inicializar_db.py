"""Crea las tablas y vistas si todavía no existen."""
from contextlib import closing
from pathlib import Path
import os
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.environ.get("STOCKMANAGER_DB_PATH", ROOT / "instance" / "StockManager.db")).resolve()
SQL_PATH = ROOT / "database" / "schema.sql"


def inicializar(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    esquema = SQL_PATH.read_text(encoding="utf-8")
    with closing(sqlite3.connect(db_path, timeout=10)) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")
        # Agregamos los campos nuevos sin perder los usuarios ni sus movimientos.
        existe = conexion.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='usuarios'"
        ).fetchone()
        if existe:
            columnas = {fila[1] for fila in conexion.execute("PRAGMA table_info(usuarios)")}
            if "correo_google" not in columnas:
                conexion.execute("ALTER TABLE usuarios ADD COLUMN correo_google TEXT COLLATE NOCASE")
            if "google_sub" not in columnas:
                conexion.execute("ALTER TABLE usuarios ADD COLUMN google_sub TEXT")
        conexion.executescript(esquema)
        resultado = conexion.execute("PRAGMA integrity_check").fetchone()[0]
        if resultado != "ok":
            raise RuntimeError(f"Error de integridad SQLite: {resultado}")


if __name__ == "__main__":
    inicializar()
    print("Base lista:", DB_PATH)
