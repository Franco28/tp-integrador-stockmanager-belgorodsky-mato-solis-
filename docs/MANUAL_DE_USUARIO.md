# Manual de usuario - StockManager

**Trabajo Práctico Integrador | Análisis y Metodologías de Sistemas | Escuela Da Vinci**

## 1. Presentación

StockManager permite administrar productos, consultar existencias y registrar entradas y salidas de mercadería. Se utiliza desde un navegador web. Las acciones disponibles dependen del rol de cada persona.

## 2. Iniciar sesión

1. Abrí la dirección informada por el equipo o `http://127.0.0.1:5000` si se ejecuta localmente.
2. Para ingresar con usuario y contraseña, completá ambos campos y presioná **Iniciar sesión**.
3. Si se configuró Google, también podés elegir **Ingresar con Google**. Seleccioná tu cuenta y aceptá el acceso.
4. Para utilizar Google, el administrador debe haber asociado previamente tu correo a una cuenta activa del sistema.

Si se rechaza el ingreso, verificá tus datos y consultá al administrador. El sistema no permite el acceso a cuentas no autorizadas.

## 3. Roles y permisos

**Administrador:** administra productos, categorías y usuarios; registra movimientos; consulta y exporta reportes; consulta la cotización externa.

**Encargado:** consulta productos, categorías, movimientos, alertas y reportes; también puede registrar entradas y salidas de stock. No puede crear ni modificar productos, categorías o usuarios.

## 4. Consultar productos

1. Elegí **Productos** en el menú principal.
2. Revisá el listado con código, nombre, categoría, precio y stock actual.
3. Para encontrar un producto, escribí su nombre o código, o elegí una categoría.
4. Presioná **Buscar** para aplicar el filtro.

Los productos desactivados no aparecen en el inventario vigente.

## 5. Crear un producto (administrador)

1. Desde **Categorías**, registrá una categoría si todavía no existe una activa.
2. Entrá a **Productos** y elegí **Nuevo producto**.
3. Completá código, nombre, categoría, precio, stock mínimo y stock inicial si corresponde.
4. Presioná **Guardar producto**.

El sistema informa si hay datos incorrectos o si el código ya se encuentra registrado.

## 6. Editar y dar de baja un producto

En el listado de **Productos**, elegí **Editar**, modificá los datos y guardá los cambios. Para retirar un producto del inventario, seleccioná **Dar de baja** y confirmá la operación. La baja conserva los movimientos históricos.

## 7. Registrar movimientos (administrador y encargado)

1. Entrá a **Movimientos** y seleccioná **Registrar movimiento**.
2. Elegí el producto y el tipo de operación: **Entrada** o **Salida**.
3. Escribí una cantidad entera mayor que cero. La observación es opcional.
4. Seleccioná **Guardar movimiento**.

Si la salida supera la cantidad disponible, el sistema no registra el movimiento.

## 8. Consultar alertas y reportes

**Inicio** muestra el resumen general y los productos con poco stock o sin unidades. **Reportes** muestra el inventario y permite descargar archivos CSV de productos y movimientos.

## 9. Consultar cotización externa (administrador)

En el menú, elegí **Cotización**. El sistema solicita una referencia cambiaria a un servicio público. Si la consulta falla, se muestra un aviso. Esta información es orientativa: **no cambia los precios ni el stock** de ningún producto.

## 10. Gestionar usuarios (administrador)

Desde **Usuarios**, registrá una cuenta con nombre, nombre de acceso, contraseña y rol. Si esa cuenta podrá ingresar con Google, indicá su correo verificado en el campo correspondiente y guardá. También podés desactivar cuentas existentes; no se elimina el historial.

## 11. Cerrar sesión

Presioná **Salir** en el encabezado al terminar.

## 12. Problemas frecuentes

| Situación | Qué revisar |
|---|---|
| No puedo iniciar sesión | Revisá credenciales; si usás Google, confirmá que tu correo esté habilitado por el administrador. |
| No tengo permiso para modificar productos o categorías | Esas tareas corresponden al administrador. El encargado puede registrar movimientos de stock. |
| No puedo registrar una salida | Verificá que haya stock suficiente. |
| No se crea un producto | Revisá campos obligatorios, código único y categoría activa. |
| La cotización no aparece | Puede haber un problema temporal con el servicio externo; intentá nuevamente. |
| Después de redesplegar desaparecieron datos | En Render gratuito el archivo SQLite puede perderse; consultá al equipo. |
