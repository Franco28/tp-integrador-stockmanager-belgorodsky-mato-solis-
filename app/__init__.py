"""Configuración principal de StockManager."""
from datetime import timedelta
import os
from pathlib import Path
import secrets

from flask import Flask, g, render_template, session
from sqlalchemy import event
from sqlalchemy.engine import Engine

from .extensions import db
from .models import Usuario
from .security import csrf_token, validar_csrf


@event.listens_for(Engine, "connect")
def habilitar_claves_foraneas(conexion, registro):
    """SQLite necesita esta opción para hacer cumplir las claves foráneas."""
    import sqlite3

    if isinstance(conexion, sqlite3.Connection):
        conexion.execute("PRAGMA foreign_keys = ON")


def obtener_clave(instance_path):
    """Usa la misma clave cada vez que se inicia la aplicación."""
    archivo = Path(instance_path) / ".secret_key"
    if not archivo.exists():
        archivo.write_text(secrets.token_hex(32), encoding="ascii")
    return archivo.read_text(encoding="ascii").strip()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    db_path = Path(os.environ.get("STOCKMANAGER_DB_PATH", instance_path / "StockManager.db"))
    db_path = db_path.resolve()

    app.config.update(
        SECRET_KEY=os.environ.get("STOCKMANAGER_SECRET_KEY") or obtener_clave(instance_path),
        SQLALCHEMY_DATABASE_URI="sqlite:///" + db_path.as_posix(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("STOCKMANAGER_COOKIE_SECURE") == "1",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=6),
        MAX_CONTENT_LENGTH=64 * 1024,
    )
    db.init_app(app)

    @app.before_request
    def cargar_usuario():
        g.usuario = None
        usuario_id = session.get("user_id")
        if isinstance(usuario_id, int):
            usuario = db.session.get(Usuario, usuario_id)
            if usuario and usuario.activo:
                g.usuario = usuario
            else:
                session.clear()
        validar_csrf()

    @app.context_processor
    def agregar_token_csrf():
        return {"csrf_token": csrf_token}

    @app.template_filter("ars")
    def formato_precio(centavos):
        pesos, resto = divmod(int(centavos), 100)
        return f"{pesos:,}".replace(",", ".") + f",{resto:02d}"

    @app.after_request
    def agregar_encabezados(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'"
        )
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.errorhandler(400)
    @app.errorhandler(403)
    @app.errorhandler(404)
    def mostrar_error(error):
        return render_template("error.html", error=error), error.code

    from .auth.routes import bp as auth_bp
    from .main.routes import bp as main_bp
    from .productos.routes import bp as productos_bp
    from .categorias.routes import bp as categorias_bp
    from .movimientos.routes import bp as movimientos_bp
    from .reportes.routes import bp as reportes_bp
    from .usuarios.routes import bp as usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(movimientos_bp, url_prefix="/movimientos")
    app.register_blueprint(reportes_bp, url_prefix="/reportes")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    return app
