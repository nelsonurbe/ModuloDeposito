# Item Model

class Item:
    id: int (PK, auto-increment)
    codigo: str (required, max 50, unique)
    nombre: str (required, max 150)
    descripcion: str (optional, text)
    cantidad: int (default 0, min 0)
    deposito_id: int (FK -> Deposito, required)
    activo: bool (default True)
    creado_en: datetime (auto)
    actualizado_en: datetime (auto-update)

    Relations:
        - deposito: Deposito  (many-to-one)
        - asignaciones: List[AsignacionItem]  (one-to-many)

    Methods:
        - crear(codigo, nombre, descripcion?, cantidad, deposito_id) -> Item
        - actualizar(id, datos) -> Item
        - eliminar(id) -> bool
        - obtener(id) -> Item
        - listar(deposito_id?, activo?) -> List[Item]
        - actualizar_cantidad(id, delta) -> Item
