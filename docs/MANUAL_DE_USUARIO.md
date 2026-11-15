# Manual de usuario — StockManager

## 1. ¿Para qué sirve StockManager?

StockManager es un programa web que permite registrar productos, consultar las existencias y llevar un historial de entradas y salidas del inventario.

Para utilizarlo es necesario que la aplicación esté iniciada y contar con un nombre de usuario y contraseña.

## 2. Ingresar al sistema

1. Abrí la dirección que te informó el equipo (en una instalación local: `http://127.0.0.1:5000`).
2. Ingresá tu nombre de usuario y contraseña.
3. Seleccioná **Iniciar sesión**.

Si los datos son incorrectos, el sistema muestra un aviso. Si no tenés cuenta, solicitale al administrador que la cree.

## 3. Consultar productos

1. Elegí **Productos** en el menú.
2. Revisá el listado con código, nombre, categoría, precio y stock.
3. Para buscar uno en particular, escribí su código o nombre; también podés elegir una categoría.
4. Presioná **Buscar** para mostrar los resultados.

Los productos dados de baja no se muestran en el listado principal.

## 4. Agregar un producto (administrador)

1. Entrá a **Categorías** y agregá una categoría si todavía no existe alguna activa.
2. Entrá a **Productos** y elegí **Nuevo producto**.
3. Completá código, nombre, categoría, precio, stock mínimo y stock inicial (si corresponde).
4. Presioná **Guardar producto**.

Si falta algún dato o el código ya existe, el sistema informa el error.

## 5. Modificar o dar de baja un producto (administrador)

En el listado de productos, seleccioná **Editar** para modificar sus datos. Guardá los cambios al terminar.

Para dar de baja un producto, seleccioná **Dar de baja** y revisá la pantalla de confirmación. La baja no elimina los movimientos anteriores.

## 6. Registrar una entrada o salida (administrador)

1. Entrá a **Movimientos** y elegí **Registrar movimiento**.
2. Seleccioná el producto y el tipo (**Entrada** o **Salida**).
3. Ingresá una cantidad mayor que cero y, si querés, una observación.
4. Seleccioná **Guardar movimiento**.

Si intentás registrar una salida mayor al stock disponible, aparece un mensaje de error y el movimiento no se guarda.

## 7. Consultar el estado del inventario

En **Inicio** podés consultar la cantidad de productos, las unidades disponibles y los productos con stock bajo o sin stock.

En **Reportes** podés consultar un resumen y descargar el inventario o el historial de movimientos en formato CSV.

## 8. Administración de usuarios (administrador)

Desde **Usuarios** podés registrar otras cuentas e indicar su rol. El administrador puede modificar información; el encargado solo puede consultar. También es posible desactivar cuentas que ya no se utilizan.

## 9. Cerrar sesión

Presioná **Salir** desde el encabezado cuando termines de utilizar el sistema.

## 10. Problemas frecuentes

| Situación | Qué hacer |
|---|---|
| No se puede iniciar sesión | Revisá usuario y contraseña. Solicitá ayuda al administrador si el problema continúa. |
| No aparece el botón para crear o modificar | Tu cuenta puede tener rol encargado, que tiene acceso de consulta. |
| No permite registrar una salida | Comprobá que el producto tenga suficientes unidades. |
| No permite crear un producto | Verificá que exista una categoría activa y que el código no esté repetido. |
| Aparece un error al enviar un formulario | Volvé a cargar la página e intentá nuevamente. |

Si la aplicación no abre, verificá con el equipo que el servidor Flask esté iniciado.
