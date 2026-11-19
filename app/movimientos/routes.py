"""Registro y consulta de entradas y salidas."""
from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..extensions import db
from ..models import MovimientoStock, Producto
from ..security import administrador_o_encargado_requerido, login_requerido
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
@administrador_o_encargado_requerido
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
            if tipo == "SALIDA":
                stock_actual = db.session.execute(
                    text("SELECT stock_actual FROM vw_inventario WHERE producto_id = :producto_id"),
                    {"producto_id": producto_id},
                ).scalar_one_or_none()
                if stock_actual is None:
                    raise ValueError("Producto inexistente o inactivo")
                if cantidad > stock_actual:
                    raise ValueError("Stock insuficiente para esta salida")
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
        except IntegrityError:
            db.session.rollback()
            flash("No se pudo registrar el movimiento. Verificá el stock y el estado del producto.", "error")
        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.exception("No se pudo registrar el movimiento de stock")
            flash("No se pudo registrar el movimiento. Intentá nuevamente.", "error")
    return render_template("movimientos/formulario.html", productos=productos)
