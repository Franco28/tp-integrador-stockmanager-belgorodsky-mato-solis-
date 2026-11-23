"""Alta, consulta, edición y baja de productos."""
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..extensions import db
from ..models import Categoria, MovimientoStock, Producto
from ..security import administrador_requerido, login_requerido
from ..validaciones import datos_producto, entero

bp = Blueprint("productos", __name__)

FIRMAS_IMAGEN = {
    ".jpg": lambda contenido: contenido.startswith(b"\xff\xd8\xff"),
    ".jpeg": lambda contenido: contenido.startswith(b"\xff\xd8\xff"),
    ".png": lambda contenido: contenido.startswith(b"\x89PNG\r\n\x1a\n"),
    ".webp": lambda contenido: contenido.startswith(b"RIFF") and contenido[8:12] == b"WEBP",
}
MAX_IMAGEN_BYTES = 5 * 1024 * 1024


def _guardar_imagen(archivo):
    if archivo is None or not archivo.filename:
        return None

    extension = Path(archivo.filename).suffix.lower()
    verificar = FIRMAS_IMAGEN.get(extension)
    contenido = archivo.stream.read(MAX_IMAGEN_BYTES + 1)
    archivo.stream.seek(0)
    if len(contenido) > MAX_IMAGEN_BYTES:
        raise ValueError("La imagen no puede superar los 5 MB")
    if verificar is None or not verificar(contenido[:12]):
        raise ValueError("La imagen debe ser JPEG, PNG o WebP válida")

    nombre = f"{uuid4().hex}{extension}"
    carpeta = Path(current_app.static_folder) / "uploads" / "productos"
    destino = carpeta / nombre
    carpeta.mkdir(parents=True, exist_ok=True)
    try:
        archivo.save(destino)
    except OSError as exc:
        _eliminar_imagen_segura(f"uploads/productos/{nombre}")
        current_app.logger.exception("No se pudo guardar el archivo de imagen")
        raise ValueError("No se pudo guardar la imagen") from exc
    return f"uploads/productos/{nombre}"


def _validar_url_imagen(valor):
    url = (valor or "").strip()
    if not url:
        return None
    if len(url) > 2048:
        raise ValueError("La URL de la imagen no puede superar los 2048 caracteres")
    try:
        partes = urlsplit(url)
        if partes.port is not None and not 1 <= partes.port <= 65535:
            raise ValueError
    except ValueError as exc:
        raise ValueError("Ingresá una URL de imagen válida con HTTPS") from exc
    if partes.scheme.lower() != "https" or not partes.hostname or partes.username or partes.password:
        raise ValueError("La URL de la imagen debe comenzar con https://")
    return url


def _eliminar_imagen(ruta):
    if not ruta:
        return
    partes = Path(ruta).parts
    if len(partes) != 3 or partes[:2] != ("uploads", "productos"):
        return
    (Path(current_app.static_folder) / "uploads" / "productos" / partes[2]).unlink(missing_ok=True)


def _eliminar_imagen_segura(ruta):
    """Limpia un archivo sin convertir un fallo de limpieza en un fallo de la operación."""
    try:
        _eliminar_imagen(ruta)
    except OSError:
        current_app.logger.warning("No se pudo eliminar un archivo de imagen", exc_info=True)


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
    categoria = (request.args.get("categoria") or "").strip()
    try:
        categoria_id = entero(categoria, "Categoría", 1) if categoria else 0
    except ValueError:
        abort(400, description="Filtro de categoría inválido")
    datos = db.session.execute(text("""
        SELECT inventario.*, productos.imagen
        FROM vw_inventario AS inventario
        JOIN productos ON productos.id = inventario.producto_id
        WHERE (:q = '' OR inventario.codigo LIKE :busqueda ESCAPE '\\'
                         OR inventario.nombre LIKE :busqueda ESCAPE '\\')
          AND (:categoria_id = 0 OR inventario.categoria_id = :categoria_id)
        ORDER BY inventario.nombre LIMIT 500
    """), {"q": q, "busqueda": f"%{_normalizar_busqueda(q)}%", "categoria_id": categoria_id}).mappings().all()
    categorias = db.session.scalars(select(Categoria).order_by(Categoria.nombre)).all()
    return render_template("productos/lista.html", productos=datos, q=q,
                           categorias=categorias, categoria_id=categoria_id)


@bp.route("/nuevo", methods=["GET", "POST"])
@administrador_requerido
def nuevo():
    if request.method == "POST":
        imagen_guardada = None
        try:
            datos = datos_producto(request.form)
            _validar_categoria(datos["categoria_id"])
            inicial = entero(request.form.get("stock_inicial", "0"), "Stock inicial")
            imagen_guardada = _guardar_imagen(request.files.get("imagen"))
            if imagen_guardada:
                datos["imagen"] = imagen_guardada
            else:
                imagen_url = _validar_url_imagen(request.form.get("imagen_url"))
                if imagen_url:
                    datos["imagen"] = imagen_url
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
            _eliminar_imagen_segura(imagen_guardada)
            flash(str(exc), "error")
        except IntegrityError:
            db.session.rollback()
            _eliminar_imagen_segura(imagen_guardada)
            current_app.logger.info("Alta rechazada por una restricción SQL")
            flash("No se pudo crear: código duplicado o datos inválidos", "error")
        except OSError:
            db.session.rollback()
            _eliminar_imagen_segura(imagen_guardada)
            current_app.logger.exception("No se pudo guardar la imagen del producto")
            flash("No se pudo guardar la imagen", "error")
        except SQLAlchemyError:
            db.session.rollback()
            _eliminar_imagen_segura(imagen_guardada)
            current_app.logger.exception("No se pudo guardar el producto en la base de datos")
            flash("No se pudo guardar el producto", "error")
    form_data = request.form.to_dict() if request.method == "POST" else {}
    requiere_reseleccionar_imagen = bool(
        request.method == "POST"
        and request.files.get("imagen")
        and request.files["imagen"].filename
    )
    if requiere_reseleccionar_imagen:
        flash("Volvé a seleccionar el archivo de imagen para adjuntarlo nuevamente.", "warning")
    return render_template(
        "productos/formulario.html",
        producto=None,
        categorias=_categorias(),
        form_data=form_data,
    )


@bp.route("/<int:producto_id>/editar", methods=["GET", "POST"])
@administrador_requerido
def editar(producto_id):
    producto = db.session.get(Producto, producto_id)
    if producto is None or producto.activo != 1:
        abort(404)
    if request.method == "POST":
        imagen_guardada = None
        imagen_anterior = producto.imagen
        try:
            datos = datos_producto(request.form)
            _validar_categoria(datos["categoria_id"])
            imagen_guardada = _guardar_imagen(request.files.get("imagen"))
            if imagen_guardada:
                datos["imagen"] = imagen_guardada
            elif request.form.get("quitar_imagen") == "1":
                datos["imagen"] = None
            elif (imagen_url := _validar_url_imagen(request.form.get("imagen_url"))):
                datos["imagen"] = imagen_url
            for campo, valor in datos.items():
                setattr(producto, campo, valor)
            producto.actualizado_en = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
            db.session.commit()
            if imagen_anterior and imagen_anterior != producto.imagen:
                # La operación ya se confirmó en la base: un fallo al borrar el
                # archivo viejo se registra, pero no debe borrar la imagen nueva.
                _eliminar_imagen_segura(imagen_anterior)
            flash("Producto actualizado", "ok")
            return redirect(url_for("productos.listar"))
        except ValueError as exc:
            db.session.rollback()
            _eliminar_imagen_segura(imagen_guardada)
            flash(str(exc), "error")
        except IntegrityError:
            db.session.rollback()
            _eliminar_imagen_segura(imagen_guardada)
            flash("No se pudo modificar: código duplicado o datos inválidos", "error")
        except OSError:
            db.session.rollback()
            _eliminar_imagen_segura(imagen_guardada)
            current_app.logger.exception("No se pudo guardar la imagen del producto")
            flash("No se pudo guardar la imagen", "error")
        except SQLAlchemyError:
            db.session.rollback()
            _eliminar_imagen_segura(imagen_guardada)
            current_app.logger.exception("No se pudo actualizar el producto en la base de datos")
            flash("No se pudo actualizar el producto", "error")
    form_data = request.form.to_dict() if request.method == "POST" else {}
    requiere_reseleccionar_imagen = bool(
        request.method == "POST"
        and request.files.get("imagen")
        and request.files["imagen"].filename
    )
    if requiere_reseleccionar_imagen:
        flash("Volvé a seleccionar el archivo de imagen para adjuntarlo nuevamente.", "warning")
    return render_template(
        "productos/formulario.html",
        producto=producto,
        categorias=_categorias(),
        form_data=form_data,
    )


@bp.get("/<int:producto_id>/confirmar-baja")
@administrador_requerido
def confirmar_baja(producto_id):
    producto = db.session.get(Producto, producto_id)
    if producto is None or producto.activo != 1:
        abort(404)
    return render_template("productos/confirmar_baja.html", producto=producto)


@bp.post("/<int:producto_id>/desactivar")
@administrador_requerido
def desactivar(producto_id):
    producto = db.session.get(Producto, producto_id)
    if producto is None or producto.activo != 1:
        abort(404)
    try:
        producto.activo = 0
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("No se pudo dar de baja el producto %s", producto_id)
        flash("No se pudo dar de baja el producto. Intentá nuevamente.", "error")
        return redirect(url_for("productos.listar"))
    flash("Producto dado de baja (se conservó su historial)", "ok")
    return redirect(url_for("productos.listar"))
