"""Alta, consulta y baja de cuentas."""
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Rol, Usuario
from ..passwords import crear_hash
from ..security import administrador_requerido
from ..validaciones import USUARIO, entero, requerido

bp = Blueprint("usuarios", __name__)


@bp.get("/")
@administrador_requerido
def listar():
    usuarios = db.session.scalars(select(Usuario).order_by(Usuario.usuario)).all()
    roles = db.session.scalars(select(Rol).order_by(Rol.nombre)).all()
    return render_template("usuarios/lista.html", usuarios=usuarios, roles=roles)


@bp.post("/nuevo")
@administrador_requerido
def nuevo():
    try:
        nombre = requerido(request.form.get("nombre"), "Nombre", 120)
        username = requerido(request.form.get("usuario"), "Usuario", 32)
        if not USUARIO.fullmatch(username):
            raise ValueError("Usuario: debe comenzar con una letra y usar letras, números, _, . o -")
        rol_id = entero(request.form.get("rol_id"), "Rol", 1)
        rol = db.session.get(Rol, rol_id)
        if rol is None:
            raise ValueError("Rol inexistente")
        clave = request.form.get("password", "")
        if clave != request.form.get("confirmacion", ""):
            raise ValueError("Las contraseñas no coinciden")
        password_hash = crear_hash(clave)
        db.session.add(Usuario(nombre=nombre, usuario=username, password_hash=password_hash, rol_id=rol.id))
        db.session.commit()
        flash("Usuario creado", "ok")
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), "error")
    except IntegrityError:
        db.session.rollback()
        flash("Ya existe un usuario con ese nombre de acceso", "error")
    return redirect(url_for("usuarios.listar"))


@bp.post("/<int:usuario_id>/desactivar")
@administrador_requerido
def desactivar(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None or not usuario.activo:
        abort(404)
    if usuario.id == g.usuario.id:
        flash("No podés desactivar tu propia cuenta", "error")
        return redirect(url_for("usuarios.listar"))
    usuario.activo = 0
    db.session.commit()
    flash("Cuenta desactivada (historial preservado)", "ok")
    return redirect(url_for("usuarios.listar"))
