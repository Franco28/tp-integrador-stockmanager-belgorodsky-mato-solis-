"""Crea las tablas y vistas si todavía no existen."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "instance" / "StockManager.db"
SQL_PATH = ROOT / "database" / "schema.sql"


def inicializar(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    esquema = SQL_PATH.read_text(encoding="utf-8")
    with sqlite3.connect(db_path, timeout=10) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.executescript(esquema)
        resultado = conexion.execute("PRAGMA integrity_check").fetchone()[0]
        if resultado != "ok":
            raise RuntimeError(f"Error de integridad SQLite: {resultado}")


if __name__ == "__main__":
    inicializar()
    print("Base lista:", DB_PATH)
