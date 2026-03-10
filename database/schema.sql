-- ============================================================
-- ModuloDeposito - Esquema de Base de Datos
-- ============================================================

-- --------------------------------
-- Tabla: depositos
-- Representa los depósitos físicos donde se almacenan los ítems
-- --------------------------------
CREATE TABLE IF NOT EXISTS depositos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    ubicacion   VARCHAR(200),
    descripcion TEXT,
    activo      BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- --------------------------------
-- Tabla: usuarios
-- Representa las personas que pueden recibir ítems de los depósitos
-- --------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    apellido    VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    telefono    VARCHAR(20),
    activo      BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- --------------------------------
-- Tabla: items
-- Representa los ítems o artículos almacenados en los depósitos
-- --------------------------------
CREATE TABLE IF NOT EXISTS items (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    codigo          VARCHAR(50) NOT NULL UNIQUE,
    nombre          VARCHAR(150) NOT NULL,
    descripcion     TEXT,
    cantidad        INT NOT NULL DEFAULT 0,
    deposito_id     INT NOT NULL,
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_items_deposito
        FOREIGN KEY (deposito_id) REFERENCES depositos(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- --------------------------------
-- Tabla: asignacion_items
-- Registra la extracción y traslado de ítems desde un depósito a un usuario
-- --------------------------------
CREATE TABLE IF NOT EXISTS asignacion_items (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id      INT NOT NULL,
    item_id         INT NOT NULL,
    deposito_id     INT NOT NULL,
    cantidad        INT NOT NULL DEFAULT 1,
    estado          ENUM('pendiente', 'entregado', 'devuelto', 'cancelado') NOT NULL DEFAULT 'pendiente',
    notas           TEXT,
    asignado_en     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_asignacion_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_asignacion_item
        FOREIGN KEY (item_id) REFERENCES items(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_asignacion_deposito
        FOREIGN KEY (deposito_id) REFERENCES depositos(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- --------------------------------
-- Índices adicionales para mejorar las búsquedas
-- --------------------------------
CREATE INDEX idx_items_deposito ON items(deposito_id);
CREATE INDEX idx_asignacion_usuario ON asignacion_items(usuario_id);
CREATE INDEX idx_asignacion_item ON asignacion_items(item_id);
CREATE INDEX idx_asignacion_deposito ON asignacion_items(deposito_id);
CREATE INDEX idx_asignacion_estado ON asignacion_items(estado);
