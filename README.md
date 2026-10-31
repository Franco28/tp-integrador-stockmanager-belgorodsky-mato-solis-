## Descripción del proyecto

**StockManager** es un sistema de gestión de inventario orientado a organizaciones que necesitan administrar productos y controlar las existencias disponibles de manera centralizada.

El sistema busca reducir los errores derivados de registros manuales y facilitar el acceso a información actualizada sobre productos, stock y movimientos de inventario.

El desarrollo se realiza de manera incremental, utilizando **Scrum** como marco de trabajo y **Trello** como herramienta para la organización y seguimiento de las Historias de Usuario.

## Objetivo general

Desarrollar un sistema funcional de gestión de inventario que permita administrar de manera centralizada los productos y controlar las existencias disponibles, facilitando el acceso a la información y reduciendo errores en la gestión del stock.

## Objetivos específicos

- Centralizar la información correspondiente a los productos.
- Permitir altas, bajas, modificaciones y consultas de productos.
- Mantener actualizado el stock disponible.
- Registrar movimientos de entrada y salida.
- Identificar productos con stock insuficiente.
- Facilitar la búsqueda y consulta de productos.
- Reducir errores derivados de registros manuales.
- Brindar información actualizada que facilite la toma de decisiones.
- Mantener la persistencia de la información del inventario.
- Permitir el acceso al sistema mediante autenticación de usuarios.

## Alcance

Para el primer Producto Mínimo Viable (**MVP**), el sistema contempla las siguientes funcionalidades:

- Alta de productos.
- Consulta de productos.
- Modificación de información de productos.
- Baja de productos.
- Búsqueda de productos.
- Registro de entradas de stock.
- Registro de salidas de stock.
- Consulta de stock disponible.
- Detección de productos con stock mínimo.
- Consulta del historial de movimientos de inventario.
- Persistencia de los datos.
- Inicio de sesión de usuarios.

El alcance se encuentra enfocado específicamente en la gestión del inventario. Funcionalidades correspondientes a otros dominios de negocio, como ventas, facturación, compras o gestión contable, no forman parte del MVP actual.

## Actores del sistema

Durante el análisis del sistema se identificaron dos actores externos principales.

### Administrador

El administrador puede realizar operaciones de gestión sobre los productos y el inventario, entre ellas:

- Registrar productos.
- Modificar productos.
- Eliminar productos.
- Registrar entradas de stock.
- Registrar salidas de stock.
- Consultar información de productos.
- Consultar stock disponible.
- Consultar alertas de bajo stock.
- Consultar movimientos de inventario.

### Encargado

El encargado utiliza el sistema principalmente para realizar consultas relacionadas con el inventario.

Entre sus acciones se encuentran:

- Consultar productos.
- Consultar stock disponible.
- Consultar productos con bajo stock.
- Consultar movimientos de inventario.

## Metodología de trabajo

El proyecto se desarrolla utilizando un enfoque ágil basado en **Scrum**.

## Gestión del proyecto

La organización de tareas se realiza utilizando **Trello**.

El tablero se encuentra dividido en las siguientes columnas:

1. **Product Backlog**
2. **Sprint Backlog (To Do)**
3. **In Progress**
4. **Code Review / Testing**
5. **Done**

### Tablero Trello

https://trello.com/b/D6cUCTrH/team-rcp-gestor-de-inventario-tp-integrador

## Tecnologías

El proyecto se desarrolla utilizando las tecnologías trabajadas durante la cursada.

### Backend

- Python
- Flask

### Persistencia

- SQLite
- SQLAlchemy / Flask-SQLAlchemy

### Presentación

- HTML
- Jinja2
- CSS

### Comunicación HTTP

El sistema puede utilizar los métodos HTTP convencionales de acuerdo con las operaciones realizadas:

| Operación | Método HTTP |
|---|---|
| Consultar información | `GET` |
| Crear información | `POST` |
| Actualizar información | `PUT` / `PATCH` |
| Eliminar información | `DELETE` |

Estas operaciones se corresponden con el modelo CRUD utilizado para la gestión de productos.

## Persistencia de datos

La información del inventario debe mantenerse almacenada independientemente de la ejecución de la aplicación.

La persistencia contempla principalmente información correspondiente a:

- Productos.
- Stock disponible.
- Movimientos de inventario.
- Usuarios del sistema.

El uso de una base de datos permite conservar la información luego de cerrar y volver a ejecutar la aplicación.

## Gestión de productos

Los productos constituyen una de las entidades principales del sistema.

De manera general, cada producto debe disponer de información suficiente para permitir su identificación y administración, incluyendo datos como:

- Identificador.
- Código.
- Nombre.
- Precio.
- Stock disponible.
- Stock mínimo.
- Categoría, cuando corresponda.

El sistema debe permitir realizar las operaciones CRUD correspondientes:

- **Create:** registrar un producto.
- **Read:** consultar uno o más productos.
- **Update:** modificar un producto existente.
- **Delete:** eliminar un producto.

## Gestión del stock

El sistema permite registrar movimientos que afectan las existencias de los productos.

### Entrada de stock

Una entrada representa el ingreso de unidades de un producto al inventario.

Al registrar una entrada, la cantidad disponible del producto debe incrementarse.

### Salida de stock

Una salida representa la disminución de unidades disponibles.

El sistema debe validar que exista stock suficiente antes de realizar la operación.

### Stock mínimo

El sistema permite identificar aquellos productos cuya cantidad disponible se encuentra por debajo del nivel mínimo establecido.

Esta funcionalidad permite detectar productos que requieren reposición.

## Movimientos de inventario

Los movimientos permiten mantener trazabilidad sobre las modificaciones realizadas al stock.

Un movimiento puede representar:

- Entrada de unidades.
- Salida de unidades.

El historial de movimientos permite consultar las operaciones realizadas sobre el inventario y conocer cómo se modificaron las existencias de los productos.

## Autenticación

El sistema contempla autenticación de usuarios para restringir el acceso a las funcionalidades correspondientes.

El flujo general consiste en:

1. El usuario ingresa sus credenciales.
2. El sistema verifica la información proporcionada.
3. Si las credenciales son válidas, se inicia la sesión.
4. Si las credenciales son incorrectas, el acceso es rechazado.
5. Las funcionalidades protegidas solo pueden utilizarse con una sesión activa.

Por razones de seguridad, las contraseñas no deben almacenarse en texto plano. Deben almacenarse mediante mecanismos de hashing.

## Arquitectura general

El sistema se plantea como una aplicación web desarrollada con Flask.

De forma conceptual, la interacción sigue el ciclo:

```text
Usuario
   ↓
Interfaz Web
   ↓
Flask
   ↓
Lógica del sistema
   ↓
Persistencia de datos
   ↓
SQLite / SQLAlchemy
```

Flask recibe las solicitudes realizadas por los usuarios, ejecuta la lógica correspondiente y devuelve una respuesta.

La información persistente es gestionada mediante la capa de acceso a datos.

## Análisis del sistema

Durante el desarrollo se utilizan diferentes herramientas de análisis y modelado vistas durante la materia.

Entre ellas se encuentran:

- Diagrama de Contexto.
- Diagramas de Flujo de Datos (DFD).
- Diccionario de Datos.
- Diagrama Entidad-Relación (DER).
- Historias de Usuario.
- Criterios de aceptación.
- Modelado estructurado.
- Modelado orientado a objetos.

Estos modelos permiten analizar el sistema desde diferentes perspectivas y mantener coherencia entre requisitos, procesos, información y posterior implementación.

## Diagrama de contexto

El Diagrama de Contexto representa a **StockManager** como un único proceso y permite visualizar su interacción con las entidades externas.

Los actores identificados son:

- Administrador.
- Encargado.

El diagrama permite delimitar el alcance del sistema y establecer qué información ingresa y qué respuestas devuelve StockManager.

## Estructura del proyecto

La estructura podrá evolucionar durante el desarrollo según las necesidades del sistema.

Una organización general compatible con lo trabajado durante la cursada es:

```text
StockManager/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
│
├── instance/
│
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

La separación en módulos permite evitar que toda la aplicación quede concentrada en un único archivo y facilita su mantenimiento.

## Instalación

Los siguientes comandos se ejecutan desde la carpeta raíz del proyecto.

### 1. Crear y activar un entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell, activar el entorno con:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Instalar las dependencias

```bash
python -m pip install -r requerimiento.txt
```

### 3. Preparar la base de datos

Si se necesita crear o actualizar la base de datos, ejecutar:

```bash
python3 scripts/inicializar_db.py
```

El script trabaja sobre `instance/StockManager.db`. Si se desea conservar la base de datos incluida en el repositorio, no ejecutar este paso.

### 4. Iniciar Flask

El comando previsto es:

```bash
flask --app 'app:create_app' run --debug
```

Sin embargo, la aplicación todavía no arranca con la versión actual: las rutas importan `app/security.py`, archivo que no está incluido. Después de completar ese módulo, Flask quedará disponible en `http://127.0.0.1:5000`.

También faltan algunas plantillas para utilizar todas las secciones, por lo que podrían aparecer errores al abrir esas rutas incluso después de resolver el inicio de sesión.

## Requisitos

- Python 3.10 o superior.
- Gestor de paquetes `pip`.
- Entorno virtual recomendado.
- Dependencias especificadas en `requerimiento.txt`.

## Criterios generales de calidad

Durante el desarrollo se busca mantener:

- Código claro y legible.
- Separación de responsabilidades.
- Validación de los datos ingresados.
- Manejo adecuado de errores.
- Persistencia consistente.
- Seguridad en el almacenamiento de credenciales.
- Trazabilidad entre requisitos y funcionalidades.
- Pruebas de las funcionalidades implementadas.
- Actualización continua del tablero Trello.
- Documentación coherente con el estado actual del sistema.

## Estado del proyecto

El proyecto se encuentra en desarrollo incremental.

Las funcionalidades se incorporan progresivamente de acuerdo con los Sprints definidos por el equipo y las entregas establecidas durante la cursada.

## Equipo

### Integrantes

- Lara Belgorodsky
- Franco Mato
- Romina Solis

## Docente

**Florencio Elías Contrera**
