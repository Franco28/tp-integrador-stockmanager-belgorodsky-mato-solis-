"""Inicio y cierre de sesión."""
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import select

from ..extensions import db
from ..models import Usuario
from ..passwords import verificar_hash

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
    return render_template("login.html")


@bp.post("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "ok")
    return redirect(url_for("auth.login"))
