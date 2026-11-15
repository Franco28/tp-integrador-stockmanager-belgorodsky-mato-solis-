# StockManager

**Trabajo Práctico Integrador — Análisis y Metodologías de Sistemas**  
Carrera: Analista de Sistemas · Escuela Da Vinci

StockManager es una aplicación web para registrar productos, controlar las existencias y consultar los movimientos del inventario. El objetivo es mantener la información centralizada y reducir los errores asociados a registros manuales.

El proyecto fue desarrollado en Python y se organiza mediante historias de usuario y Sprints, siguiendo los contenidos de la materia.

## Funcionalidades

- Inicio y cierre de sesión con dos roles: **administrador** y **encargado**.
- Alta, consulta, búsqueda, modificación y baja lógica de productos.
- Gestión de categorías y stock mínimo por producto.
- Registro de entradas y salidas de unidades.
- Validación para evitar salidas superiores al stock disponible.
- Historial de movimientos, resumen de inventario y alertas de stock bajo.
- Exportación de inventario y movimientos a CSV.
- Persistencia de la información con SQLite.

El **administrador** puede modificar productos, categorías, usuarios y movimientos. El **encargado** solo puede consultar productos, categorías, movimientos y reportes. Las operaciones de ventas, compras y facturación quedan fuera del alcance de este trabajo.

## Tecnologías

- **Python 3.10 o superior** y **Flask** para la aplicación web.
- **Flask-SQLAlchemy** y **SQLite 3.37 o superior** para persistencia.
- **Jinja2, HTML y CSS** para las páginas del sistema.
- **Trello** para organizar las historias de usuario.

No se utilizan servicios externos ni una arquitectura de microservicios: es una única aplicación organizada en módulos mediante Blueprints, como se trabajó en las clases.

## Instalación y puesta en marcha

Los comandos se ejecutan desde la carpeta raíz del proyecto.

### 1. Crear el entorno virtual

```bash
python -m venv .venv
```

Activación en Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 3. Inicializar la base de datos

```bash
python scripts/inicializar_db.py
```

El script crea `instance/StockManager.db` con las tablas, restricciones, vistas y los roles. Se puede volver a ejecutar sin borrar los registros existentes.

### 4. Crear la primera cuenta administradora

```bash
python scripts/crear_admin.py
```

El programa solicita nombre, usuario y contraseña (mínimo 12 caracteres). **El proyecto no incluye usuarios ni contraseñas predeterminadas.**

### 5. Ejecutar Flask

```bash
flask --app wsgi run --debug
```

Abrir **http://127.0.0.1:5000** en el navegador e iniciar sesión con la cuenta creada. `--debug` se usa solo durante el desarrollo local.

## Uso básico

1. El administrador inicia sesión y crea al menos una **categoría**.
2. Registra un **producto**, indicando código, nombre, categoría, precio, stock mínimo y, si corresponde, stock inicial.
3. Desde **Movimientos** registra entradas y salidas. El stock se calcula automáticamente a partir de esos registros.
4. Consulta el inventario desde **Productos** o **Inicio** y verifica las alertas de bajo stock.
5. Desde **Reportes** puede consultar los datos y descargar archivos CSV.
6. El administrador puede crear cuentas de tipo encargado, para permitir consultas sin autorización para modificar datos.

El producto se da de baja en lugar de borrarse físicamente para conservar sus movimientos anteriores. Antes de la baja se muestra una página de confirmación.

Para una explicación paso a paso, consultar [Manual de usuario](docs/MANUAL_DE_USUARIO.md).

## Estructura principal

```text
StockManager/
├── app/
│   ├── auth/                 # Inicio y cierre de sesión
│   ├── categorias/           # Gestión de categorías
│   ├── main/                 # Resumen del inventario
│   ├── movimientos/          # Entradas, salidas e historial
│   ├── productos/            # Gestión de productos
│   ├── reportes/             # Consultas y CSV
│   ├── usuarios/             # Administración de cuentas
│   ├── static/css/           # Estilos
│   ├── templates/            # Páginas HTML con Jinja2
│   ├── models.py             # Tablas representadas como clases
│   ├── security.py           # Sesiones, permisos y formularios
│   ├── validaciones.py       # Validación de datos
│   └── __init__.py           # Configuración y Blueprints
├── database/schema.sql      # Estructura de la base de datos
├── scripts/                 # Inicialización y primer administrador
├── docs/                    # Análisis y documentación
├── tests/                   # Pruebas del sistema
├── instance/                # Base de datos local (se genera al iniciar)
├── requirements.txt
├── wsgi.py
└── README.md
```

## Cómo se mantiene actualizado el stock

Los movimientos tienen un tipo (**ENTRADA** o **SALIDA**) y una cantidad positiva. La vista `vw_inventario` calcula el stock de cada producto sumando las entradas y restando las salidas. Una restricción en la base de datos evita registrar salidas cuando las unidades disponibles son insuficientes.

Las contraseñas se almacenan mediante un hash y las funciones administrativas verifican el rol del usuario. Los formularios incluyen un token para evitar envíos no autorizados desde otros sitios.

## Pruebas

Con el entorno virtual activo y las dependencias instaladas:

```bash
python -m unittest discover -s tests -v
```

Las pruebas cubren reglas del stock, persistencia y recorridos principales de la aplicación. También se recomienda hacer una prueba manual de las pantallas con ambas clases de usuario.

## Documentación y metodología

- [Análisis y alcance](docs/ANALISIS_DEL_SISTEMA.md)
- [Manual de usuario](docs/MANUAL_DE_USUARIO.md)
- [Guía del código](docs/GUIA_DE_CODIGO.md)
- [Rutas y plantillas](docs/RUTAS_Y_VISTAS.md)
- [Tablero Trello](https://trello.com/b/D6cUCTrH/team-rcp-gestor-de-inventario-tp-integrador)

El tablero está organizado en **Product Backlog, Sprint Backlog (To Do), In Progress, Code Review / Testing y Done**. Cada historia tiene criterios de aceptación y se considera terminada después de su implementación y revisión.

## Equipo

- Lara Belgorodsky
- Franco Mato
- Romina Solis

**Docente:** Florencio Elías Contrera.

Este proyecto se realizó con fines académicos como parte del Trabajo Práctico Integrador de la materia.
