# StockManager - Trabajo Práctico Integrador

**Materia:** Análisis y Metodologías de Sistemas | **Carrera:** Analista de Sistemas | **Escuela Da Vinci**

**Equipo RCP:** Lara Belgorodsky, Franco Mato y Romina Solis.

StockManager es una aplicación de control de inventario hecha en Python y Flask. Permite dar de alta y modificar productos, registrar movimientos, calcular el stock disponible y consultar reportes.

## Funcionalidades

- Productos: alta, consulta, búsqueda, modificación, baja lógica y categorías.
- Movimientos: entradas, salidas y bloqueo cuando el stock no alcanza.
- Reportes: resumen, alertas y exportación de inventario y movimientos a CSV.
- Usuarios: administrador (gestión) y encargado (consultas).
- Autenticación local y acceso con Google para cuentas previamente autorizadas.
- Consulta de cotización desde una API pública, independiente del stock.

## Tecnologías

- Python 3.10+, Flask, Jinja2, HTML, CSS.
- Flask-SQLAlchemy y SQLite (incluye vistas y restricciones SQL).
- Authlib para Google (OAuth/OIDC), Requests para la API externa.
- `unittest` para pruebas y Gunicorn para el despliegue.
- Trello para las historias de usuario y la planificación de Sprints.

## Instalación local

Desde la raíz del proyecto:

```bash
python -m venv .venv
```

Activá el entorno: en Windows PowerShell, `.\.venv\Scripts\Activate.ps1`; en Linux/macOS, `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
```

Copiá `.env.example` como `.env`. Para usar el login local no necesitás completar Google. Podés dejar `STOCKMANAGER_SECRET_KEY` vacío en desarrollo, pero debe configurarse en producción. **Nunca subas `.env` a GitHub.**

Inicializá la base y creá el primer administrador:

```bash
python scripts/inicializar_db.py
python scripts/crear_admin.py
```

Para cargar un catálogo local de demostración con iPhone y MacBook:

```bash
python scripts/seed_demo.py
```

El seed se puede ejecutar más de una vez: agrega los productos que falten y registra las entradas iniciales con un administrador activo. Los precios son valores de muestra. No lo ejecutes en producción.

Desde **Productos**, un administrador puede cargar una imagen JPEG, PNG o WebP de hasta 5 MB. El formulario muestra una vista previa y el catálogo presenta las imágenes en tarjetas adaptables. En desarrollo se guardan en `app/static/uploads/productos`; Render gratuito utiliza almacenamiento efímero, por lo que esas imágenes no están respaldadas entre despliegues.

Ejecutá:

```bash
flask --app wsgi run --debug
```

Abrí `http://127.0.0.1:5000`. `--debug` es solo para desarrollo local.

## Ingreso con Google

La aplicación permite iniciar sesión usando Google, pero no crea usuarios por sí sola: primero un administrador debe registrar el correo autorizado desde **Usuarios**. De ese modo se respetan los roles existentes.

1. Creá las credenciales de OAuth en Google Cloud.
2. Configurá `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` en `.env` o Render.
3. En la configuración de Google autorizá el callback local `http://127.0.0.1:5000/login/google/callback` (y la URL HTTPS real cuando se publique).
4. Probá el acceso con un usuario que tenga su correo Google vinculado.

El login tradicional se mantiene y no depende de Google.

## Consumo de API

Desde **Cotización**, el administrador consulta datos de referencia usando `COTIZACION_API_URL` (por defecto `https://dolarapi.com/v1/dolares/oficial`). La aplicación controla errores y establece un tiempo límite de espera. Esta consulta **no modifica** precios, productos ni stock.

## Despliegue en Render

Incluimos `render.yaml` y [una guía](docs/DESPLIEGUE_RENDER.md). Para publicar hay que configurar la URL pública, credenciales Google y datos de la cuenta administradora inicial en las variables privadas del servicio. El servicio arranca con Gunicorn y sin modo debug.

**Limitación de SQLite en Render gratuito:** el archivo de base de datos se puede perder al reiniciar o redesplegar si el almacenamiento es efímero. Esta versión permite una demostración del sistema, pero la persistencia duradera requiere almacenamiento apropiado. Ver [explicación y comprobaciones](docs/PERSISTENCIA_RENDER.md). No declaramos probada la publicación hasta obtener una URL real y ejecutar las pruebas correspondientes.

## Estructura principal

```text
app/                 # Rutas, modelos, seguridad y plantillas
  auth/              # Login local y Google
  usuarios/          # Cuentas, permisos y vinculación Google
  productos/         # Gestión de productos
  movimientos/       # Entradas y salidas
  categorias/        # Categorías
  reportes/          # Consultas y CSV
  cotizaciones/      # Consulta API externa
database/schema.sql  # Tablas, vistas, restricciones y roles
scripts/             # Inicialización y creación de administrador
instance/            # Datos locales generados, no distribuir
docs/                # Manual, análisis y despliegue
tests/               # Pruebas unittest
requirements.txt
render.yaml
.env.example
wsgi.py
```

## Documentación

- [Manual](docs/MANUAL_DE_USUARIO.md).
- [Análisis del sistema y contexto](docs/ANALISIS_DEL_SISTEMA.md).
- [Despliegue en Render](docs/DESPLIEGUE_RENDER.md).
- [Historias en Trello](https://trello.com/b/D6cUCTrH/team-rcp-gestor-de-inventario-tp-integrador).
- [Repositorio de GitHub](https://github.com/Franco28/tp-integrador-stockmanager-belgorodsky-mato-solis-).

## Alcance y entrega

El proyecto no incluye facturación, ventas, gestión de proveedores ni un módulo contable. Está desarrollado como un TP incremental. **Antes del segundo parcial**.
