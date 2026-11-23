# Despliegue de StockManager en Render

En esta sección explicamos cómo publicar StockManager en Render para poder acceder al sistema desde Internet, sin necesidad de ejecutarlo de forma local.

Para el despliegue utilizamos **Render**, que permite alojar aplicaciones desarrolladas con Python y Flask.

## 1. Preparación del proyecto

Antes de publicar la aplicación, tenemos que asegurarnos de que el código esté actualizado en GitHub.

También debemos verificar que no se suban archivos con información privada, como:

- `.env`, que contiene las variables de entorno.
- Archivos `.db` de la base de datos local.
- Contraseñas o credenciales de acceso.

Estos archivos deben estar excluidos mediante `.gitignore`.

## 2. Configuración del inicio de sesión con Google

Para que los usuarios puedan ingresar con Google, necesitamos crear las credenciales OAuth desde Google Cloud.

Una vez que tengamos el nombre del servicio en Render, debemos configurar las siguientes direcciones:

**Origen autorizado:**

`https://TU-SERVICIO.onrender.com`

**URI de redireccionamiento autorizada:**

`https://TU-SERVICIO.onrender.com/login/google/callback`

Estas direcciones deben coincidir con la URL donde se encuentre publicada la aplicación.

## 3. Creación del servicio en Render

Para publicar StockManager, tenemos que ingresar a Render y conectar nuestro repositorio de GitHub.

El proyecto incluye el archivo `render.yaml`, que contiene la configuración necesaria para crear el servicio web.

Después de conectar el repositorio, debemos completar las variables de entorno que utiliza la aplicación.

| Variable                      | Descripción                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| `STOCKMANAGER_PUBLIC_URL`     | Dirección pública de nuestra aplicación en Render.                                  |
| `GOOGLE_CLIENT_ID`            | Identificador de la aplicación de Google.                                           |
| `GOOGLE_CLIENT_SECRET`        | Clave privada para la autenticación con Google.                                     |
| `STOCKMANAGER_ADMIN_NOMBRE`   | Nombre del administrador inicial.                                                   |
| `STOCKMANAGER_ADMIN_USUARIO`  | Usuario del administrador inicial.                                                  |
| `STOCKMANAGER_ADMIN_PASSWORD` | Contraseña del administrador inicial.                                               |
| `STOCKMANAGER_SECRET_KEY`     | Clave utilizada por Flask para manejar las sesiones. Se genera desde `render.yaml`. |

Las credenciales y contraseñas se configuran directamente en Render para evitar que queden expuestas en el repositorio.

## 4. Inicialización de la base de datos

StockManager utiliza **SQLite** para almacenar los productos, usuarios, categorías y movimientos del inventario.

Al iniciar la aplicación, se ejecuta el proceso de inicialización de la base de datos, que crea las tablas necesarias.

También se verifica si existe un administrador activo. Si no existe, se crea una cuenta inicial utilizando los datos configurados en las variables de entorno.

De esta manera, podemos preparar el sistema para su primer uso sin tener que subir una base de datos con usuarios y contraseñas al repositorio.

## 5. Comprobación del despliegue

Una vez publicada la aplicación, tenemos que comprobar que funcione correctamente.

Primero podemos verificar que las siguientes direcciones respondan:

- `/health`: para comprobar el estado de la aplicación.
- `/login`: para acceder a la pantalla de inicio de sesión.
- `/login/google/callback`: dirección utilizada por Google para completar la autenticación. Se debe comprobar mediante el flujo de inicio de sesión con Google, no ingresando directamente.

Después, revisamos estas funciones desde la aplicación:

1. Iniciar sesión con el administrador.
2. Comprobar el ingreso mediante Google con una cuenta autorizada.
3. Crear una categoría y registrar un producto.
4. Registrar una entrada y una salida de stock.
5. Consultar el inventario y verificar las cantidades disponibles.
6. Consultar los reportes.
7. Consultar la cotización mediante la API externa.
8. Cerrar sesión y volver a ingresar.

Estas comprobaciones permiten verificar que las funcionalidades principales trabajen correctamente desde Render.

## 6. Consideraciones sobre SQLite en Render

Un aspecto que tenemos que tener en cuenta es que SQLite guarda la información en un archivo local.

En el servicio gratuito de Render, el almacenamiento es efímero. Por este motivo, aunque los productos y movimientos se guarden correctamente mientras funciona la aplicación, los datos pueden perderse cuando el servicio se reinicia o se vuelve a desplegar.

Esto no afecta la lógica del sistema, pero sí representa una limitación para conservar los registros a largo plazo.

En el archivo [PERSISTENCIA_RENDER.md](PERSISTENCIA_RENDER.md) explicamos con más detalle esta situación y las comprobaciones manuales disponibles.

Si el sistema se utilizara en un entorno real, sería necesario contar con una alternativa de almacenamiento persistente.

## 7. Preparación de la entrega

Cuando la aplicación esté publicada y hayamos verificado su funcionamiento, debemos guardar la URL real de Render en el archivo TXT correspondiente.

También tenemos que comprobar que el proyecto pueda ejecutarse localmente y que se encuentren incluidos los archivos necesarios, como `requirements.txt`, `.env.example` y la documentación.

Por último, debemos registrar el resultado de la revisión, especialmente lo relacionado con el inicio de sesión, el funcionamiento del inventario y la persistencia de los datos.

Con esto dejamos documentado cómo realizamos el despliegue de StockManager y qué aspectos tuvimos en cuenta para su funcionamiento en Render.
