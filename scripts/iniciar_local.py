"""Prepara y ejecuta StockManager localmente desde macOS o Windows.

El entorno virtual y las dependencias se preparan cuando hacen falta.
La base y las cuentas existentes no se borran.
"""
from __future__ import annotations

from contextlib import closing
import hashlib
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = ROOT / ".venv"
REQUIREMENTS = ROOT / "requirements.txt"
ENV_EXAMPLE = ROOT / ".env.example"
ENV_FILE = ROOT / ".env"
MARCADOR_DEPS = VENV_DIR / ".stockmanager_requirements_sha256"


def python_del_entorno() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def verificar_version() -> None:
    if sys.version_info < (3, 10):
        raise RuntimeError("StockManager necesita Python 3.10 o superior.")


def preparar() -> None:
    verificar_version()
    os.chdir(ROOT)
    if not REQUIREMENTS.is_file() or not ENV_EXAMPLE.is_file():
        raise RuntimeError("Ejecutá el iniciador desde el proyecto completo de StockManager.")

    python_venv = python_del_entorno()
    if not VENV_DIR.exists():
        print("[1/5] Creando entorno virtual .venv...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True, cwd=ROOT)
    elif not python_venv.is_file():
        raise RuntimeError(
            "La carpeta .venv no corresponde a este sistema operativo o está incompleta. "
            "Renombrala o eliminá únicamente esa carpeta y volvé a ejecutar el iniciador."
        )
    else:
        print("[1/5] Usando el entorno virtual existente.")

    contenido = REQUIREMENTS.read_bytes()
    huella = hashlib.sha256(contenido).hexdigest()
    if not MARCADOR_DEPS.is_file() or MARCADOR_DEPS.read_text(encoding="ascii").strip() != huella:
        print("[2/5] Instalando dependencias de requirements.txt...")
        subprocess.run(
            [str(python_venv), "-m", "pip", "install", "-r", str(REQUIREMENTS)],
            check=True,
            cwd=ROOT,
        )
        MARCADOR_DEPS.write_text(huella, encoding="ascii")
    else:
        print("[2/5] Dependencias ya instaladas; sin cambios en requirements.txt.")

    if ENV_FILE.exists():
        print("[3/5] Manteniendo el .env existente.")
    else:
        shutil.copyfile(ENV_EXAMPLE, ENV_FILE)
        print("[3/5] Creado .env desde .env.example (sin credenciales reales).")

    subprocess.run([str(python_venv), str(Path(__file__).resolve()), "--continuar"], check=True, cwd=ROOT)


def iniciar_aplicacion() -> None:
    verificar_version()
    os.chdir(ROOT)
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    # SQLite STRICT está disponible desde SQLite 3.37.
    if sqlite3.sqlite_version_info < (3, 37, 0):
        raise RuntimeError(
            "La versión de SQLite de este Python es demasiado antigua. "
            "Instalá una versión actual de Python 3 desde python.org."
        )

    from scripts.inicializar_db import DB_PATH, inicializar

    print("[4/5] Inicializando o verificando la base de datos...")
    inicializar()

    with closing(sqlite3.connect(DB_PATH, timeout=10)) as conexion:
        existe_admin = conexion.execute(
            """SELECT 1 FROM usuarios AS u
               JOIN roles AS r ON r.id = u.rol_id
               WHERE r.nombre = 'administrador' AND u.activo = 1
               LIMIT 1"""
        ).fetchone()

    if not existe_admin:
        print("No existe un administrador activo. Vamos a crear el primero.")
        from scripts.crear_admin import main as crear_admin
        crear_admin()
    else:
        print("Ya hay un administrador activo: no se crea otra cuenta.")

    print("[5/5] Iniciando StockManager...")
    print("Abrí http://127.0.0.1:5000 en el navegador.")
    print("Para detenerlo, presioná Ctrl+C en esta ventana.")
    print("Modo debug habilitado solo para desarrollo local.\n")
    subprocess.run(
        [sys.executable, "-m", "flask", "--app", "wsgi", "run", "--debug"],
        check=True,
        cwd=ROOT,
    )


def main() -> int:
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "--continuar":
            iniciar_aplicacion()
        elif len(sys.argv) == 1:
            preparar()
        else:
            print("Uso: ejecutar desde iniciar_mac.command o iniciar_windows.bat", file=sys.stderr)
            return 2
        return 0
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        return 0
    except subprocess.CalledProcessError as error:
        print(f"\nFalló un comando (código {error.returncode}).", file=sys.stderr)
        return error.returncode or 1
    except (RuntimeError, OSError, sqlite3.Error) as error:
        print(f"\nNo se pudo iniciar StockManager: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
