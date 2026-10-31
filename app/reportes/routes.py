"""Consulta y descarga de reportes."""
import csv
import io

from flask import Blueprint, Response, abort, render_template, request
from sqlalchemy import text

from ..extensions import db
from ..security import login_requerido

bp = Blueprint("reportes", __name__)

CONSULTAS = {
    "inventario": (
        "SELECT codigo, nombre, categoria, precio_centavos, stock_actual, stock_minimo, estado_stock "
        "FROM vw_inventario ORDER BY nombre",
        "inventario.csv",
    ),
    "movimientos": (
        "SELECT fecha, codigo_producto, producto, tipo, cantidad, registrado_por, observacion "
        "FROM vw_reporte_movimientos ORDER BY fecha DESC, movimiento_id DESC",
        "movimientos.csv",
    ),
}


def _celda_csv(valor):
    texto = "" if valor is None else str(valor)
    # Evita que una planilla ejecute el dato como una fórmula.
    if texto.startswith(("=", "+", "-", "@", "\t", "\r", "\n")):
        return "'" + texto
    return texto


@bp.get("/")
@login_requerido
def inicio():
    resumen = db.session.execute(text("SELECT * FROM vw_resumen_inventario")).mappings().one()
    inventario = db.session.execute(text("SELECT * FROM vw_inventario ORDER BY nombre LIMIT 500")).mappings().all()
    return render_template("reportes/inicio.html", resumen=resumen, inventario=inventario)


@bp.get("/exportar")
@login_requerido
def exportar():
    tipo = request.args.get("tipo", "")
    if tipo not in CONSULTAS:
        abort(400, description="Tipo de reporte no válido")
    consulta, nombre = CONSULTAS[tipo]
    resultado = db.session.execute(text(consulta))
    columnas = list(resultado.keys())
    salida = io.StringIO(newline="")
    escritor = csv.writer(salida)
    escritor.writerow(columnas)
    for fila in resultado:
        escritor.writerow([_celda_csv(valor) for valor in fila])
    contenido = "\ufeff" + salida.getvalue()
    return Response(contenido, content_type="text/csv; charset=utf-8", headers={
        "Content-Disposition": f'attachment; filename="{nombre}"',
    })
