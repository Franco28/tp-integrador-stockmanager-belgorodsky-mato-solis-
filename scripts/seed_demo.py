"""Carga un catálogo de demostración de iPhone y MacBook."""
from contextlib import closing
import os
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.inicializar_db import DB_PATH, inicializar  # noqa: E402

OBSERVACION_SEED = "Seed demo StockManager v1"

CATEGORIAS = {
    "iPhone": "Teléfonos Apple para demostración de inventario",
    "MacBook": "Computadoras Apple portátiles para demostración de inventario",
}

# Precios de muestra en pesos argentinos; no representan cotizaciones vigentes.
# El precio se guarda en centavos y el stock se registra como movimiento de entrada.
PRODUCTOS = (
    (
        "DEMO-IP18PRO-256", "iPhone 18 Pro 256 GB", "Borgoña, 256 GB. Precio de muestra.",
        "iPhone", 2_499_990, 2, 3,
        "https://www.apple.com/v/iphone-18-pro/e/images/overview/aio/hero__elo7tt0mnqy6_large.jpg",
    ),
    (
        "DEMO-IP18PM-512", "iPhone 18 Pro Max 512 GB", "Negro, 512 GB. Precio de muestra.",
        "iPhone", 2_999_990, 2, 2,
        "https://www.apple.com/v/iphone-18-pro/e/images/overview/media-hero/hero_endframe__fbxsnz8txcia_large.jpg",
    ),
    (
        "DEMO-IPDUO-512", "iPhone Duo 512 GB", "512 GB. Precio de muestra.",
        "iPhone", 3_899_990, 2, 1,
        "https://www.apple.com/v/iphone-duo/f/images/overview/media-hero/hero_startframe__fcol1x2us8i2_large.jpg",
    ),
    (
        "DEMO-IP17E-256", "iPhone 17e 256 GB", "Negro, 256 GB. Precio de muestra.",
        "iPhone", 1_499_990, 3, 5,
        "https://www.apple.com/v/iphone-17e/g/images/overview/welcome/hero_endframe__eafizd06t6qa_large.jpg",
    ),
    (
        "DEMO-MBP14-M6", "MacBook Pro 14 pulgadas M6", "16 GB de memoria, 512 GB SSD. Precio de muestra.",
        "MacBook", 4_199_990, 1, 0,
        "https://www.apple.com/newsroom/images/2026/10/apple-introduces-the-new-14-inch-macbook-pro-with-m6/article/Apple-MacBook-Pro-14-in-with-M6-lifestyle-261027_big.jpg.large.jpg",
    ),
    (
        "DEMO-MBP16-M5MAX", "MacBook Pro 16 pulgadas M5 Max PROLED XDR", "48 GB de memoria, 2 TB SSD. Precio de muestra.",
        "MacBook", 7_499_990, 1, 1,
        "https://www.apple.com/newsroom/images/2026/10/apple-unveils-groundbreaking-macbook-pro-with-proled-xdr-display/article/Apple-MacBook-Pro-with-PROLED-XDR-Display-QuickTime-261028_big.jpg.large.jpg",
    ),
    (
        "DEMO-MBA15-M5", "MacBook Air 15 pulgadas M5", "16 GB de memoria, 512 GB SSD. Precio de muestra.",
        "MacBook", 2_399_990, 2, 3,
        "https://www.apple.com/v/macbook-air/z/images/overview/hero/hero_startframe__c0rhv2ultfau_large.png",
    ),
    (
        "DEMO-MBNEO-256", "MacBook Neo 256 GB", "8 GB de memoria, 256 GB SSD. Precio de muestra.",
        "MacBook", 1_299_990, 2, 4,
        "https://www.apple.com/v/macbook-neo/c/images/overview/welcome/hero_endframe__c62q483im5si_xlarge.jpg",
    ),
)


def cargar_seed(db_path: Path = DB_PATH) -> tuple[int, int]:
    inicializar(db_path)
    agregados = 0
    movimientos = 0

    with closing(sqlite3.connect(db_path, timeout=10)) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")
        administrador = conexion.execute("""
            SELECT u.id
            FROM usuarios u JOIN roles r ON r.id = u.rol_id
            WHERE r.nombre = 'administrador' AND u.activo = 1
            ORDER BY u.id
            LIMIT 1
        """).fetchone()
        if administrador is None:
            raise RuntimeError(
                "Creá o activá un usuario administrador antes de cargar el seed demo"
            )

        with conexion:
            categorias = {}
            for nombre, descripcion in CATEGORIAS.items():
                fila = conexion.execute(
                    "SELECT id FROM categorias WHERE nombre = ?", (nombre,)
                ).fetchone()
                if fila is None:
                    cursor = conexion.execute(
                        "INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)",
                        (nombre, descripcion),
                    )
                    categorias[nombre] = cursor.lastrowid
                else:
                    categorias[nombre] = fila[0]

            for codigo, nombre, descripcion, categoria, precio, minimo, cantidad, imagen in PRODUCTOS:
                existente = conexion.execute(
                    "SELECT id FROM productos WHERE codigo = ?", (codigo,)
                ).fetchone()
                if existente is not None:
                    continue

                cursor = conexion.execute("""
                    INSERT INTO productos (
                        codigo, nombre, descripcion, categoria_id,
                        precio_centavos, stock_minimo, imagen
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (codigo, nombre, descripcion, categorias[categoria], precio * 100, minimo, imagen))
                agregados += 1

                if cantidad:
                    conexion.execute("""
                        INSERT INTO movimientos_stock (
                            producto_id, usuario_id, tipo, cantidad, observacion
                        ) VALUES (?, ?, 'ENTRADA', ?, ?)
                    """, (cursor.lastrowid, administrador[0], cantidad, OBSERVACION_SEED))
                    movimientos += 1

    return agregados, movimientos


if __name__ == "__main__":
    if os.environ.get("STOCKMANAGER_ENV", "development").lower() == "production":
        raise SystemExit("El seed demo está deshabilitado en producción")
    productos, entradas = cargar_seed()
    print(f"Seed demo listo: {productos} productos nuevos y {entradas} entradas de stock.")
