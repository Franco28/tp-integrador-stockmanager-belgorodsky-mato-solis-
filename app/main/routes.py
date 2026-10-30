"""Página principal con el resumen del inventario."""
from flask import Blueprint, render_template
from sqlalchemy import text

from ..extensions import db
from ..security import login_requerido

bp = Blueprint("main", __name__)


@bp.get("/")
@login_requerido
def inicio():
    resumen = db.session.execute(text("SELECT * FROM vw_resumen_inventario")).mappings().one()
    bajo_stock = db.session.execute(text("""
        SELECT codigo, nombre, stock_actual, stock_minimo, estado_stock
        FROM vw_inventario WHERE estado_stock != 'NORMAL'
        ORDER BY stock_actual ASC, nombre LIMIT 30
    """)).mappings().all()
    return render_template("inicio.html", resumen=resumen, bajo_stock=bajo_stock)
