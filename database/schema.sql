-- StockManager / Team RCP
-- Motor: SQLite 3.37+ (archivos .db)
-- Todas las conexiones Python deben ejecutar: PRAGMA foreign_keys = ON;
-- El stock se calcula desde el historial: no se actualiza manualmente.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL COLLATE NOCASE UNIQUE
        CHECK (nombre IN ('administrador', 'encargado')),
    descripcion TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) BETWEEN 1 AND 120),
    usuario TEXT NOT NULL COLLATE NOCASE UNIQUE
        CHECK (length(trim(usuario)) BETWEEN 3 AND 32),
    password_hash TEXT NOT NULL CHECK (length(password_hash) >= 40),
    rol_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
    creado_en TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
) STRICT;

CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol_id);

CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL COLLATE NOCASE UNIQUE
        CHECK (length(trim(nombre)) BETWEEN 1 AND 80),
    descripcion TEXT,
    activa INTEGER NOT NULL DEFAULT 1 CHECK (activa IN (0, 1))
) STRICT;

CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL COLLATE NOCASE UNIQUE
        CHECK (length(trim(codigo)) BETWEEN 1 AND 40),
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) BETWEEN 1 AND 120),
    descripcion TEXT,
    categoria_id INTEGER NOT NULL REFERENCES categorias(id) ON DELETE RESTRICT,
    precio_centavos INTEGER NOT NULL CHECK (precio_centavos >= 0),
    stock_minimo INTEGER NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0),
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
    creado_en TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    actualizado_en TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
) STRICT;

CREATE INDEX IF NOT EXISTS idx_productos_categoria_activo
    ON productos(categoria_id, activo);
CREATE INDEX IF NOT EXISTS idx_productos_nombre ON productos(nombre COLLATE NOCASE);

CREATE TABLE IF NOT EXISTS movimientos_stock (
    id INTEGER PRIMARY KEY,
    producto_id INTEGER NOT NULL REFERENCES productos(id) ON DELETE RESTRICT,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE RESTRICT,
    tipo TEXT NOT NULL CHECK (tipo IN ('ENTRADA', 'SALIDA')),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    observacion TEXT,
    creado_en TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
) STRICT;

CREATE INDEX IF NOT EXISTS idx_movimientos_producto_fecha
    ON movimientos_stock(producto_id, creado_en DESC);
CREATE INDEX IF NOT EXISTS idx_movimientos_usuario ON movimientos_stock(usuario_id);
CREATE INDEX IF NOT EXISTS idx_movimientos_fecha ON movimientos_stock(creado_en DESC);

-- Un encargado no puede registrar movimientos, aunque se lo intente por SQL
-- usando su propio usuario. La app debe autorizar TODOS los demás cambios.
CREATE TRIGGER IF NOT EXISTS validar_nuevo_movimiento
BEFORE INSERT ON movimientos_stock
BEGIN
    SELECT CASE
        WHEN NOT EXISTS (
            SELECT 1 FROM productos
            WHERE id = NEW.producto_id AND activo = 1
        ) THEN RAISE(ABORT, 'El producto no existe o esta inactivo')
    END;

    SELECT CASE
        WHEN NOT EXISTS (
            SELECT 1 FROM usuarios u JOIN roles r ON r.id = u.rol_id
            WHERE u.id = NEW.usuario_id AND u.activo = 1
              AND r.nombre = 'administrador'
        ) THEN RAISE(ABORT, 'Solo un administrador puede registrar movimientos')
    END;

    SELECT CASE
        WHEN NEW.tipo = 'SALIDA'
          AND NEW.cantidad > COALESCE((
              SELECT SUM(CASE WHEN tipo = 'ENTRADA' THEN cantidad ELSE -cantidad END)
              FROM movimientos_stock
              WHERE producto_id = NEW.producto_id
          ), 0)
        THEN RAISE(ABORT, 'Stock insuficiente')
    END;
END;

-- El historial es inmutable. Una corrección se registra con un movimiento inverso.
CREATE TRIGGER IF NOT EXISTS bloquear_edicion_movimiento
BEFORE UPDATE ON movimientos_stock
BEGIN
    SELECT RAISE(ABORT, 'Los movimientos historicos no se modifican');
END;

CREATE TRIGGER IF NOT EXISTS bloquear_borrado_movimiento
BEFORE DELETE ON movimientos_stock
BEGIN
    SELECT RAISE(ABORT, 'Los movimientos historicos no se eliminan');
END;

-- Conservamos el historial mediante baja logica de productos y usuarios.
CREATE TRIGGER IF NOT EXISTS bloquear_borrado_producto
BEFORE DELETE ON productos
BEGIN
    SELECT RAISE(ABORT, 'Desactivar el producto (activo=0), no eliminarlo');
END;

CREATE TRIGGER IF NOT EXISTS bloquear_borrado_usuario
BEFORE DELETE ON usuarios
BEGIN
    SELECT RAISE(ABORT, 'Desactivar el usuario (activo=0), no eliminarlo');
END;

-- Fuente unica de verdad del stock: las entradas y salidas historicas.
CREATE VIEW IF NOT EXISTS vw_inventario AS
WITH existencias AS (
    SELECT producto_id,
           SUM(CASE WHEN tipo = 'ENTRADA' THEN cantidad ELSE -cantidad END) AS stock_actual
    FROM movimientos_stock
    GROUP BY producto_id
)
SELECT
    p.id AS producto_id,
    p.codigo,
    p.nombre,
    p.descripcion,
    c.id AS categoria_id,
    c.nombre AS categoria,
    p.precio_centavos,
    p.stock_minimo,
    COALESCE(e.stock_actual, 0) AS stock_actual,
    CASE
        WHEN COALESCE(e.stock_actual, 0) = 0 THEN 'SIN_STOCK'
        WHEN COALESCE(e.stock_actual, 0) < p.stock_minimo THEN 'STOCK_BAJO'
        ELSE 'NORMAL'
    END AS estado_stock
FROM productos p
JOIN categorias c ON c.id = p.categoria_id
LEFT JOIN existencias e ON e.producto_id = p.id
WHERE p.activo = 1;

CREATE VIEW IF NOT EXISTS vw_resumen_inventario AS
SELECT
    COUNT(*) AS total_productos,
    COALESCE(SUM(stock_actual), 0) AS total_unidades,
    COALESCE(SUM(CASE WHEN estado_stock = 'SIN_STOCK' THEN 1 ELSE 0 END), 0) AS productos_sin_stock,
    COALESCE(SUM(CASE WHEN estado_stock = 'STOCK_BAJO' THEN 1 ELSE 0 END), 0) AS productos_stock_bajo,
    COALESCE(SUM(stock_actual * precio_centavos), 0) AS valor_inventario_centavos
FROM vw_inventario;

CREATE VIEW IF NOT EXISTS vw_reporte_movimientos AS
SELECT
    m.id AS movimiento_id,
    m.creado_en AS fecha,
    p.codigo AS codigo_producto,
    p.nombre AS producto,
    m.tipo,
    m.cantidad,
    u.usuario AS registrado_por,
    m.observacion
FROM movimientos_stock m
JOIN productos p ON p.id = m.producto_id
JOIN usuarios u ON u.id = m.usuario_id;

INSERT INTO roles(nombre, descripcion)
VALUES ('administrador', 'Gestion integral de productos, categorias, movimientos y usuarios'),
       ('encargado', 'Solo consultas y reportes')
ON CONFLICT(nombre) DO NOTHING;
