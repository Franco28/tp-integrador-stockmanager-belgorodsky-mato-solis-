# Rutas principales de StockManager

Todas las rutas requieren inicio de sesión, excepto `/login`, las rutas de Google, `/health` y los archivos estáticos.

| Ruta | Método | Uso | Acceso |
|---|---|---|---|
| `/login` | GET, POST | Inicio de sesión | Público |
| `/login/google` | GET | Comenzar ingreso con Google | Público |
| `/login/google/callback` | GET | Retorno de Google | Público |
| `/health` | GET | Estado para Render | Público |
| `/logout` | POST | Cierre de sesión | Sesión activa |
| `/` | GET | Resumen y alertas | Administrador / encargado |
| `/productos/` | GET | Listar y buscar productos | Administrador / encargado |
| `/productos/nuevo` | GET, POST | Registrar un producto | Administrador |
| `/productos/<id>/editar` | GET, POST | Modificar un producto | Administrador |
| `/productos/<id>/confirmar-baja` | GET | Confirmar la baja | Administrador |
| `/productos/<id>/desactivar` | POST | Dar de baja un producto | Administrador |
| `/categorias/` | GET | Listar categorías | Administrador / encargado |
| `/categorias/nuevo` | POST | Agregar categoría | Administrador |
| `/categorias/<id>/desactivar` | POST | Desactivar categoría | Administrador |
| `/movimientos/` | GET | Historial de movimientos | Administrador / encargado |
| `/movimientos/nuevo` | GET, POST | Registrar entrada o salida | Administrador |
| `/reportes/` | GET | Resumen y listado de inventario | Administrador / encargado |
| `/reportes/exportar?tipo=inventario` | GET | Descargar inventario CSV | Administrador / encargado |
| `/reportes/exportar?tipo=movimientos` | GET | Descargar movimientos CSV | Administrador / encargado |
| `/usuarios/` | GET | Listar cuentas | Administrador |
| `/usuarios/nuevo` | POST | Crear cuenta | Administrador |
| `/usuarios/<id>/desactivar` | POST | Desactivar cuenta | Administrador |
| `/usuarios/<id>/google` | POST | Asociar correo Google | Administrador |
| `/cotizaciones/` | GET | Cotización desde API externa | Administrador |

`<id>` representa el identificador numérico del registro.

## Vistas y plantillas

- `app/templates/base.html`: diseño compartido y navegación.
- `app/templates/inicio.html`: resumen y alertas.
- `app/templates/login.html`: inicio de sesión.
- `app/templates/productos/`: listado, formulario y confirmación de baja.
- `app/templates/categorias/lista.html`: consulta y alta de categorías.
- `app/templates/movimientos/`: historial y formulario de movimientos.
- `app/templates/reportes/inicio.html`: resumen y descargas CSV.
- `app/templates/usuarios/lista.html`: cuentas, roles y Google.
- `app/templates/cotizaciones/inicio.html`: consulta de API externa.
- `app/templates/error.html`: respuestas de error 400, 403 y 404.

Los archivos HTML utilizan Jinja2 para mostrar información de las consultas. Los estilos están en `app/static/css/styles.css`.
