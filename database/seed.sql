-- ============================================================
-- ModuloDeposito - Datos de Ejemplo (Seed)
-- ============================================================

-- Depósitos
INSERT INTO depositos (nombre, ubicacion, descripcion) VALUES
('Depósito Central', 'Edificio A, Planta Baja', 'Depósito principal de la empresa'),
('Depósito Norte', 'Edificio B, Piso 1', 'Depósito para materiales del sector norte'),
('Depósito Sur', 'Edificio C, Piso 2', 'Depósito para materiales del sector sur');

-- Usuarios
INSERT INTO usuarios (nombre, apellido, email, telefono) VALUES
('Juan', 'Pérez', 'juan.perez@empresa.com', '555-1001'),
('María', 'García', 'maria.garcia@empresa.com', '555-1002'),
('Carlos', 'López', 'carlos.lopez@empresa.com', '555-1003');

-- Ítems
INSERT INTO items (codigo, nombre, descripcion, cantidad, deposito_id) VALUES
('IT-001', 'Laptop Dell XPS', 'Laptop para uso corporativo', 10, 1),
('IT-002', 'Mouse Inalámbrico', 'Mouse ergonómico inalámbrico', 50, 1),
('IT-003', 'Teclado Mecánico', 'Teclado mecánico retroiluminado', 30, 2),
('IT-004', 'Monitor 27"', 'Monitor Full HD de 27 pulgadas', 15, 2),
('IT-005', 'Cargador USB-C', 'Cargador universal USB-C 65W', 40, 3);

-- Asignaciones de ítems
INSERT INTO asignacion_items (usuario_id, item_id, deposito_id, cantidad, estado, notas) VALUES
(1, 1, 1, 1, 'entregado', 'Asignado para teletrabajo'),
(1, 2, 1, 1, 'entregado', 'Accesorio para laptop'),
(2, 3, 2, 1, 'entregado', 'Reemplazo de teclado antiguo'),
(3, 4, 2, 1, 'pendiente', 'Pendiente de retiro'),
(2, 5, 3, 2, 'entregado', 'Cargadores de repuesto');
