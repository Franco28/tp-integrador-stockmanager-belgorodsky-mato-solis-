"""Clases que representan las tablas de la base de datos."""
from .extensions import db


class Rol(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text, nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=False)


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text, nullable=False)
    usuario = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    activo = db.Column(db.Integer, nullable=False, default=1)
    creado_en = db.Column(db.Text, nullable=False, server_default=db.text("(strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))"))

    rol = db.relationship("Rol")


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text, nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    activa = db.Column(db.Integer, nullable=False, default=1)


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Text, nullable=False, unique=True)
    nombre = db.Column(db.Text, nullable=False)
    descripcion = db.Column(db.Text)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=False)
    precio_centavos = db.Column(db.Integer, nullable=False)
    stock_minimo = db.Column(db.Integer, nullable=False, default=0)
    activo = db.Column(db.Integer, nullable=False, default=1)
    creado_en = db.Column(db.Text, nullable=False, server_default=db.text("(strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))"))
    actualizado_en = db.Column(db.Text, nullable=False, server_default=db.text("(strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))"))

    categoria = db.relationship("Categoria")


class MovimientoStock(db.Model):
    __tablename__ = "movimientos_stock"

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id", ondelete="RESTRICT"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False)
    tipo = db.Column(db.Text, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    observacion = db.Column(db.Text)
    creado_en = db.Column(db.Text, nullable=False, server_default=db.text("(strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))"))

    producto = db.relationship("Producto")
    usuario = db.relationship("Usuario")
