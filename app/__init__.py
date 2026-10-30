"""Configuración y creación de la aplicación Flask."""
import os
from pathlib import Path
import secrets

from flask import Flask

from .extensions import db


def create_app(configuracion: dict | None = None) -> Flask:
    """Crea la aplicación y registra sus rutas."""
    raiz = Path(__file__).resolve().parent.parent
    carpeta_instance = raiz / "instance"
    carpeta_instance.mkdir(parents=True, exist_ok=True)

    clave_path = carpeta_instance / ".secret_key"
    clave = os.environ.get("SECRET_KEY")
    if not clave and clave_path.exists():
        clave = clave_path.read_text(encoding="utf-8").strip()
    if not clave:
        clave = secrets.token_hex(32)

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=clave,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{carpeta_instance / 'StockManager.db'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if configuracion:
        app.config.update(configuracion)

    db.init_app(app)

    # Importar los modelos registra sus tablas en SQLAlchemy.
    from . import models  # noqa: F401
    from .categorias.routes import bp as categorias_bp
    from .main.routes import bp as main_bp
    from .movimientos.routes import bp as movimientos_bp
    from .productos.routes import bp as productos_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(movimientos_bp, url_prefix="/movimientos")

    return app
