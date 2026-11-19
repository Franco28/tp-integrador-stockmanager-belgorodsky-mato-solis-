"""Consulta una cotización externa para mostrarla como referencia."""
from decimal import Decimal, InvalidOperation

from flask import Blueprint, current_app, render_template
import requests

from ..security import administrador_requerido

bp = Blueprint("cotizaciones", __name__)


def obtener_cotizacion(url: str) -> dict:
    respuesta = requests.get(url, timeout=5)
    respuesta.raise_for_status()
    datos = respuesta.json()
    if not isinstance(datos, dict):
        raise ValueError("La API no devolvió un objeto")
    try:
        compra = Decimal(str(datos["compra"]))
        venta = Decimal(str(datos["venta"]))
    except (KeyError, InvalidOperation, TypeError) as exc:
        raise ValueError("La API devolvió una cotización inválida") from exc
    if not compra.is_finite() or not venta.is_finite() or compra < 0 or venta < 0:
        raise ValueError("La API devolvió una cotización inválida")
    return {
        "compra": compra,
        "venta": venta,
        "moneda": str(datos.get("moneda", "USD"))[:12],
        "fuente": "DolarAPI (cotización oficial)",
        "fecha": str(datos.get("fechaActualizacion", "No indicada"))[:40],
    }


@bp.get("/")
@administrador_requerido
def inicio():
    cotizacion = None
    error = None
    try:
        cotizacion = obtener_cotizacion(current_app.config["COTIZACION_API_URL"])
    except (requests.RequestException, ValueError) as exc:
        current_app.logger.warning("Fallo en la consulta de cotización: %s", type(exc).__name__)
        error = "No se pudo consultar la cotización en este momento. Probá nuevamente más tarde."
    return render_template("cotizaciones/inicio.html", cotizacion=cotizacion, error=error)
