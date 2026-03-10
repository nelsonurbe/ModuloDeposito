# Deposito Model

class Deposito:
    id: int (PK, auto-increment)
    nombre: str (required, max 100)
    ubicacion: str (optional, max 200)
    descripcion: str (optional, text)
    activo: bool (default True)
    creado_en: datetime (auto)
    actualizado_en: datetime (auto-update)

    Relations:
        - items: List[Item]  (one-to-many)
        - asignaciones: List[AsignacionItem]  (one-to-many)

    Methods:
        - crear(nombre, ubicacion?, descripcion?) -> Deposito
        - actualizar(id, datos) -> Deposito
        - eliminar(id) -> bool
        - obtener(id) -> Deposito
        - listar(activo?) -> List[Deposito]
        - obtener_items(id) -> List[Item]
