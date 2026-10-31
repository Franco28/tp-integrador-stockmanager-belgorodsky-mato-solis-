"""Funciones para controlar el acceso y los formularios."""
from functools import wraps
import hmac
import secrets

from flask import abort, g, redirect, request, session, url_for


def csrf_token() -> str:
    """Crea un token para validar los formularios."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def validar_csrf() -> None:
    """Revisa el token cuando se envía un formulario."""
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        actual = session.get("csrf_token", "")
        recibido = request.form.get("csrf_token", "")
        if not actual or not recibido or not hmac.compare_digest(actual, recibido):
            abort(400, description="Token CSRF inválido. Volvé a cargar el formulario.")


def login_requerido(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.usuario is None:
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


def administrador_requerido(func):
    @wraps(func)
    @login_requerido
    def wrapper(*args, **kwargs):
        if g.usuario.rol.nombre != "administrador":
            abort(403)
        return func(*args, **kwargs)
    return wrapper
