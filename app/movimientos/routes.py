"""Registro y consulta de entradas y salidas."""
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import MovimientoStock, Producto
from ..security import administrador_requerido, login_requerido
from ..validaciones import entero, opcional

bp = Blueprint("movimientos", __name__)


@bp.get("/")
@login_requerido
def listar():
    movimientos = db.session.execute(text("""
        SELECT * FROM vw_reporte_movimientos ORDER BY fecha DESC, movimiento_id DESC LIMIT 500
    """)).mappings().all()
    return render_template("movimientos/lista.html", movimientos=movimientos)


@bp.route("/nuevo", methods=["GET", "POST"])
@administrador_requerido
def nuevo():
    productos = db.session.scalars(select(Producto).where(Producto.activo == 1).order_by(Producto.nombre)).all()
    if request.method == "POST":
        try:
            producto_id = entero(request.form.get("producto_id"), "Producto", 1)
            producto = db.session.get(Producto, producto_id)
            if producto is None or producto.activo != 1:
                raise ValueError("Producto inexistente o inactivo")
            tipo = request.form.get("tipo")
            if tipo not in {"ENTRADA", "SALIDA"}:
                raise ValueError("Tipo de movimiento inválido")
            cantidad = entero(request.form.get("cantidad"), "Cantidad", 1)
            observacion = opcional(request.form.get("observacion"), "Observación")
            db.session.add(MovimientoStock(
                producto_id=producto_id, usuario_id=g.usuario.id,
                tipo=tipo, cantidad=cantidad, observacion=observacion,
            ))
            db.session.commit()
            flash("Movimiento registrado", "ok")
            return redirect(url_for("movimientos.listar"))
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), "error")
        except IntegrityError as exc:
            db.session.rollback()
            texto = str(exc.orig)
            if "Stock insuficiente" in texto:
                flash("Stock insuficiente para esta salida", "error")
            else:
                flash("No se pudo registrar el movimiento", "error")
    return render_template("movimientos/formulario.html", productos=productos)
