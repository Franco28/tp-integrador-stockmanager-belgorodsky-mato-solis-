"""Alta, consulta y baja de categorías."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Categoria
from ..security import administrador_requerido, login_requerido
from ..validaciones import opcional, requerido

bp = Blueprint("categorias", __name__)


@bp.get("/")
@login_requerido
def listar():
    categorias = db.session.scalars(select(Categoria).order_by(Categoria.nombre)).all()
    return render_template("categorias/lista.html", categorias=categorias)


@bp.post("/nuevo")
@administrador_requerido
def nuevo():
    try:
        nombre = requerido(request.form.get("nombre"), "Nombre", 80)
        descripcion = opcional(request.form.get("descripcion"), "Descripción")
        db.session.add(Categoria(nombre=nombre, descripcion=descripcion))
        db.session.commit()
        flash("Categoría agregada", "ok")
    except ValueError as exc:
        flash(str(exc), "error")
    except IntegrityError:
        db.session.rollback()
        flash("La categoría ya existe", "error")
    return redirect(url_for("categorias.listar"))


@bp.post("/<int:categoria_id>/desactivar")
@administrador_requerido
def desactivar(categoria_id):
    categoria = db.session.get(Categoria, categoria_id)
    if categoria is None:
        abort(404)
    categoria.activa = 0
    db.session.commit()
    flash("Categoría desactivada; los productos existentes conservan su clasificación", "ok")
    return redirect(url_for("categorias.listar"))
