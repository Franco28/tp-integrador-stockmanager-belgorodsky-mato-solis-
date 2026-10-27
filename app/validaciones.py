"""Comprobaciones para los datos de los formularios."""
from decimal import Decimal, InvalidOperation
import re

CODIGO = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,39}\Z")
USUARIO = re.compile(r"[A-Za-z][A-Za-z0-9_.-]{2,31}\Z")


def entero(valor: str | None, nombre: str, minimo: int = 0, maximo: int = 1_000_000_000) -> int:
    texto = (valor or "").strip()
    if not texto.isdecimal():
        raise ValueError(f"{nombre}: ingresá un número entero válido")
    numero = int(texto)
    if not minimo <= numero <= maximo:
        raise ValueError(f"{nombre}: debe estar entre {minimo} y {maximo}")
    return numero


def requerido(valor: str | None, nombre: str, maximo: int) -> str:
    texto = (valor or "").strip()
    if not 1 <= len(texto) <= maximo:
        raise ValueError(f"{nombre}: debe tener entre 1 y {maximo} caracteres")
    return texto


def opcional(valor: str | None, nombre: str, maximo: int = 500) -> str | None:
    texto = (valor or "").strip()
    if len(texto) > maximo:
        raise ValueError(f"{nombre}: máximo {maximo} caracteres")
    return texto or None


def centavos(valor: str | None) -> int:
    entrada = (valor or "").strip().replace(",", ".")
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]{1,2})?", entrada):
        raise ValueError("Precio: usá un número positivo con hasta dos decimales")
    try:
        numero = Decimal(entrada) * 100
        entero_precio = int(numero)
    except (InvalidOperation, OverflowError, ValueError) as exc:
        raise ValueError("Precio inválido") from exc
    if entero_precio > 1_000_000_000_000:
        raise ValueError("Precio demasiado elevado")
    return entero_precio


def datos_producto(form) -> dict:
    codigo = requerido(form.get("codigo"), "Código", 40)
    if not CODIGO.fullmatch(codigo):
        raise ValueError("Código: solo letras, números, guiones, punto y guion bajo")
    return {
        "codigo": codigo,
        "nombre": requerido(form.get("nombre"), "Nombre", 120),
        "descripcion": opcional(form.get("descripcion"), "Descripción"),
        "categoria_id": entero(form.get("categoria_id"), "Categoría", 1),
        "precio_centavos": centavos(form.get("precio")),
        "stock_minimo": entero(form.get("stock_minimo"), "Stock mínimo"),
    }
