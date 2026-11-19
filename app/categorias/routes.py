"""Alta, consulta y baja de categorías."""
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..extensions import db
from ..models import Categoria, Producto
from ..security import administrador_requerido, login_requerido
from ..validaciones import opcional, requerido

bp = Blueprint("categorias", __name__)


@bp.get("/")
@login_requerido
def listar():
    busqueda = request.args.get("q", "").strip()[:80]
    estado = request.args.get("estado", "")
    orden = request.args.get("orden", "nombre_asc")
    if estado not in {"activa", "inactiva"}:
        estado = ""
    if orden not in {"nombre_asc", "nombre_desc", "productos_desc", "productos_asc"}:
        orden = "nombre_asc"

    cantidad_productos = (
        select(func.count(Producto.id))
        .where(Producto.categoria_id == Categoria.id, Producto.activo == 1)
        .scalar_subquery()
    )
    consulta = select(Categoria, cantidad_productos.label("cantidad_productos"))
    if busqueda:
        termino = f"%{busqueda}%"
        consulta = consulta.where(
            or_(Categoria.nombre.ilike(termino), Categoria.descripcion.ilike(termino))
        )
    if estado:
        consulta = consulta.where(Categoria.activa == (1 if estado == "activa" else 0))

    if orden == "nombre_desc":
        consulta = consulta.order_by(Categoria.nombre.desc(), Categoria.id)
    elif orden == "productos_desc":
        consulta = consulta.order_by(cantidad_productos.desc(), Categoria.nombre)
    elif orden == "productos_asc":
        consulta = consulta.order_by(cantidad_productos.asc(), Categoria.nombre)
    else:
        consulta = consulta.order_by(Categoria.nombre, Categoria.id)

    categorias = db.session.execute(consulta).all()
    return render_template(
        "categorias/lista.html",
        categorias=categorias,
        busqueda=busqueda,
        estado=estado,
        orden=orden,
    )


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
        db.session.rollback()
        flash(str(exc), "error")
    except IntegrityError:
        db.session.rollback()
        flash("La categoría ya existe", "error")
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("No se pudo guardar la categoría")
        flash("No se pudo guardar la categoría. Intentá nuevamente.", "error")
    return redirect(url_for("categorias.listar"))


@bp.post("/<int:categoria_id>/desactivar")
@administrador_requerido
def desactivar(categoria_id):
    categoria = db.session.get(Categoria, categoria_id)
    if categoria is None:
        abort(404)
    try:
        categoria.activa = 0
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("No se pudo desactivar la categoría %s", categoria_id)
        flash("No se pudo desactivar la categoría. Intentá nuevamente.", "error")
        return redirect(url_for("categorias.listar"))
    flash("Categoría desactivada; los productos existentes conservan su clasificación", "ok")
    return redirect(url_for("categorias.listar"))
