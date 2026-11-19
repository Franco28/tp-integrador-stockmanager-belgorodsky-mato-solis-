# SQLite y el despliegue en Render

StockManager utiliza **SQLite** como base de datos para almacenar la información de productos, usuarios y movimientos de inventario.

SQLite guarda los datos en un archivo local, lo que facilita su implementación y permite trabajar sin configurar un servidor de base de datos independiente.

Al publicar la aplicación en **Render**, es importante considerar que el almacenamiento del plan gratuito es efímero. Esto significa que los datos pueden perderse cuando el servicio se reinicia o se realiza un nuevo despliegue.

Para facilitar la ejecución, el sistema cuenta con un proceso de inicialización que crea las tablas necesarias y permite configurar una cuenta administradora sin incluir contraseñas directamente en el código.

Durante el funcionamiento de una misma instancia, la información se conserva en la base de datos. Sin embargo, esto no garantiza que los registros permanezcan disponibles después de reiniciar el servicio.

## Verificación del funcionamiento

Para comprobar el comportamiento de la base de datos en Render, se pueden realizar las siguientes pruebas:

1. Iniciar sesión con una cuenta administradora.
2. Registrar un producto y realizar un movimiento de stock.
3. Actualizar la página y verificar que la información siga disponible.
4. Cerrar sesión, volver a ingresar y comprobar que los registros se mantienen.
5. Reiniciar el servicio desde Render y verificar nuevamente los datos almacenados.

Estas pruebas permiten comprobar el funcionamiento de la aplicación y observar cómo se comporta el almacenamiento durante su ejecución.

## Consideraciones sobre la persistencia

Para un entorno de producción donde sea necesario conservar los datos de manera permanente, se debería utilizar un almacenamiento persistente compatible con SQLite o evaluar una solución de base de datos adecuada para el hosting.

En la versión actual, el uso de SQLite permite trabajar con una estructura sencilla, aplicar las operaciones del sistema y demostrar la integración entre Flask, SQLAlchemy y la base de datos.

Como medida de seguridad, **el archivo de base de datos que contiene cuentas o información real no debe subirse al repositorio de GitHub**. La estructura puede generarse mediante los scripts de inicialización incluidos en el proyecto.