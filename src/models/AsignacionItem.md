# AsignacionItem Model

class AsignacionItem:
    id: int (PK, auto-increment)
    usuario_id: int (FK -> Usuario, required)
    item_id: int (FK -> Item, required)
    deposito_id: int (FK -> Deposito, required)
    cantidad: int (required, min 1)
    estado: enum ['pendiente', 'entregado', 'devuelto', 'cancelado'] (default 'pendiente')
    notas: str (optional, text)
    asignado_en: datetime (auto)
    actualizado_en: datetime (auto-update)

    Relations:
        - usuario: Usuario  (many-to-one)
        - item: Item  (many-to-one)
        - deposito: Deposito  (many-to-one)

    Methods:
        - crear(usuario_id, item_id, deposito_id, cantidad, notas?) -> AsignacionItem
        - actualizar_estado(id, estado) -> AsignacionItem
        - cancelar(id) -> AsignacionItem
        - obtener(id) -> AsignacionItem
        - listar(usuario_id?, deposito_id?, estado?) -> List[AsignacionItem]

    Business Rules:
        - Al crear: verificar que el item pertenece al deposito indicado
        - Al crear: verificar que hay suficiente cantidad disponible en el item
        - Al crear: decrementar la cantidad disponible del item
        - Al cambiar estado a 'devuelto': incrementar la cantidad disponible del item
        - Al cambiar estado a 'cancelado': incrementar la cantidad disponible del item
