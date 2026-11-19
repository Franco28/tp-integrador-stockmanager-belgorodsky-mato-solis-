"""Inicio y cierre de sesión."""
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
from authlib.integrations.base_client.errors import OAuthError
from requests.exceptions import RequestException
from sqlalchemy import select

from ..extensions import db
from ..models import Usuario
from ..passwords import verificar_hash
from ..oauth_client import oauth

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if g.usuario is not None:
        return redirect(url_for("main.inicio"))
    if request.method == "POST":
        nombre = (request.form.get("usuario") or "").strip()
        clave = request.form.get("password") or ""
        usuario = db.session.scalar(select(Usuario).where(Usuario.usuario == nombre)) if len(nombre) <= 32 else None
        if usuario is not None and usuario.activo and verificar_hash(clave, usuario.password_hash):
            session.clear()
            session["user_id"] = usuario.id
            session.permanent = True
            flash("Sesión iniciada correctamente", "ok")
            return redirect(url_for("main.inicio"))
        flash("Credenciales inválidas", "error")
    return render_template("login.html", google_habilitado=bool(
        current_app.config["GOOGLE_CLIENT_ID"] and current_app.config["GOOGLE_CLIENT_SECRET"]
    ))


@bp.post("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "ok")
    return redirect(url_for("auth.login"))


@bp.get("/login/google")
def login_google():
    if g.usuario is not None:
        return redirect(url_for("main.inicio"))
    if not current_app.config["GOOGLE_CLIENT_ID"] or not current_app.config["GOOGLE_CLIENT_SECRET"]:
        flash("El acceso con Google no está configurado", "error")
        return redirect(url_for("auth.login"))

    google = oauth.create_client("google")
    base = current_app.config["PUBLIC_URL"]
    destino = (base + url_for("auth.google_callback")) if base else url_for(
        "auth.google_callback", _external=True
    )
    return google.authorize_redirect(destino)


@bp.get("/login/google/callback")
def google_callback():
    if not current_app.config["GOOGLE_CLIENT_ID"] or not current_app.config["GOOGLE_CLIENT_SECRET"]:
        return redirect(url_for("auth.login"))
    try:
        google = oauth.create_client("google")
        token = google.authorize_access_token()
        # Authlib comprueba el ID token según la configuración OIDC de Google.
        identidad = token.get("userinfo")
        if not identidad:
            flash("No se pudo verificar la identidad de Google", "error")
            return redirect(url_for("auth.login"))
        sub = str(identidad.get("sub", ""))
        correo = str(identidad.get("email", "")).strip().lower()
        verificado = identidad.get("email_verified") is True
        if not sub or not correo or not verificado:
            flash("Google no confirmó un correo electrónico válido", "error")
            return redirect(url_for("auth.login"))

        usuario = db.session.scalar(select(Usuario).where(Usuario.google_sub == sub))
        if usuario is None:
            usuario = db.session.scalar(select(Usuario).where(Usuario.correo_google == correo))
            if usuario is None or usuario.google_sub:
                flash("Tu cuenta de Google no está autorizada. Consultá al administrador.", "error")
                return redirect(url_for("auth.login"))
            usuario.google_sub = sub
            db.session.commit()
        if not usuario.activo:
            flash("Esta cuenta está desactivada", "error")
            return redirect(url_for("auth.login"))
        session.clear()
        session["user_id"] = usuario.id
        session.permanent = True
        flash("Sesión iniciada con Google", "ok")
        return redirect(url_for("main.inicio"))
    except (OAuthError, RequestException, ValueError, KeyError) as exc:
        db.session.rollback()
        current_app.logger.warning("No se completó el login con Google: %s", type(exc).__name__)
        flash("No se pudo iniciar sesión con Google. Intentá nuevamente.", "error")
        return redirect(url_for("auth.login"))
