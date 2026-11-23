# Guía breve del código — StockManager

Este documento explica las partes principales para facilitar el seguimiento del proyecto.

## Inicio de la aplicación

`wsgi.py` crea la aplicación llamando a `create_app()` de `app/__init__.py`. Allí se configura Flask, se conecta SQLAlchemy con SQLite y se registran los Blueprints.

La base de datos se crea previamente con `python scripts/inicializar_db.py`. No se generan las tablas al entrar a una página.

## Organización por módulos

Cada carpeta funcional tiene un `routes.py` con las rutas de Flask. Por ejemplo, `productos/routes.py` contiene las operaciones de alta, listado, edición y baja. Esta separación evita concentrar todo el proyecto en un archivo.

En `app/models.py` están las clases `Rol`, `Usuario`, `Categoria`, `Producto` y `MovimientoStock`. Cada una representa una tabla de SQLite.

## Formularios y páginas

Las páginas están en `app/templates`. Se usa `render_template()` y Jinja2 para mostrar resultados de las consultas. `base.html` contiene el menú común y se completa con los estilos de `app/static/css/styles.css`.

El botón de baja de productos abre una página de confirmación. Así se verifica la decisión del usuario antes de desactivar un registro.

## Datos y validaciones

`app/validaciones.py` controla datos como código, nombre, cantidades y precio. Después, SQLite también aplica restricciones para que no se graben movimientos inválidos. Ante un error conocido, se informa al usuario sin perder la consistencia de los registros.

El stock se calcula con las vistas definidas en `database/schema.sql`, a partir de entradas y salidas. Los movimientos no se modifican ni se eliminan porque forman parte del historial.

## Sesiones y permisos

`app/passwords.py` crea y comprueba hashes de contraseñas. `app/security.py` valida la sesión, el token de los formularios y los permisos según el rol. El administrador gestiona el catálogo y las cuentas; administrador y encargado pueden registrar movimientos de stock.

## Alcance técnico

El proyecto utiliza herramientas trabajadas en la cursada: Python, Flask, Blueprints, Jinja2, SQLite y SQLAlchemy. No necesita microservicios ni una infraestructura adicional para el objetivo académico.
