"""Alta, consulta, edición y baja de productos."""
from datetime import datetime, timezone

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Categoria, MovimientoStock, Producto
from ..security import administrador_requerido, login_requerido
from ..validaciones import datos_producto, entero

bp = Blueprint("productos", __name__)


def _categorias():
    return db.session.scalars(select(Categoria).where(Categoria.activa == 1).order_by(Categoria.nombre)).all()


def _validar_categoria(categoria_id):
    categoria = db.session.get(Categoria, categoria_id)
    if categoria is None or categoria.activa != 1:
        raise ValueError("Seleccioná una categoría activa")


def _normalizar_busqueda(q: str) -> str:
    """Permite buscar los caracteres % y _ como parte del texto."""
    return q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


@bp.get("/")
@login_requerido
def listar():
    q = (request.args.get("q") or "").strip()[:80]
    datos = db.session.execute(text("""
        SELECT * FROM vw_inventario
        WHERE (:q = '' OR codigo LIKE :busqueda ESCAPE '\\' OR nombre LIKE :busqueda ESCAPE '\\')
        ORDER BY nombre LIMIT 500
    """), {"q": q, "busqueda": f"%{_normalizar_busqueda(q)}%"}).mappings().all()
    return render_template("productos/lista.html", productos=datos, q=q)


@bp.route("/nuevo", methods=["GET", "POST"])
@administrador_requerido
def nuevo():
    if request.method == "POST":
        try:
            datos = datos_producto(request.form)
            _validar_categoria(datos["categoria_id"])
            inicial = entero(request.form.get("stock_inicial", "0"), "Stock inicial")
            producto = Producto(**datos)
            db.session.add(producto)
            db.session.flush()
            if inicial:
                db.session.add(MovimientoStock(
                    producto_id=producto.id, usuario_id=g.usuario.id,
                    tipo="ENTRADA", cantidad=inicial, observacion="Carga inicial",
                ))
            db.session.commit()
            flash("Producto creado", "ok")
            return redirect(url_for("productos.listar"))
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), "error")
        except IntegrityError:
            db.session.rollback()
            current_app.logger.info("Alta rechazada por una restricción SQL")
            flash("No se pudo crear: código duplicado o datos inválidos", "error")
    return render_template("productos/formulario.html", producto=None, categorias=_categorias())


@bp.route("/<int:producto_id>/editar", methods=["GET", "POST"])
@administrador_requerido
def editar(producto_id):
    producto = db.session.get(Producto, producto_id)
    if producto is None or producto.activo != 1:
        abort(404)
    if request.method == "POST":
        try:
            datos = datos_producto(request.form)
            _validar_categoria(datos["categoria_id"])
            for campo, valor in datos.items():
                setattr(producto, campo, valor)
            producto.actualizado_en = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
            db.session.commit()
            flash("Producto actualizado", "ok")
            return redirect(url_for("productos.listar"))
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), "error")
        except IntegrityError:
            db.session.rollback()
            flash("No se pudo modificar: código duplicado o datos inválidos", "error")
    return render_template("productos/formulario.html", producto=producto, categorias=_categorias())


@bp.post("/<int:producto_id>/desactivar")
@administrador_requerido
def desactivar(producto_id):
    producto = db.session.get(Producto, producto_id)
    if producto is None or producto.activo != 1:
        abort(404)
    producto.activo = 0
    db.session.commit()
    flash("Producto dado de baja (se conservó su historial)", "ok")
    return redirect(url_for("productos.listar"))
