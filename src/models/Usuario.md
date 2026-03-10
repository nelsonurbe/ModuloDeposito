# Usuario Model

class Usuario:
    id: int (PK, auto-increment)
    nombre: str (required, max 100)
    apellido: str (required, max 100)
    email: str (required, max 150, unique)
    telefono: str (optional, max 20)
    activo: bool (default True)
    creado_en: datetime (auto)
    actualizado_en: datetime (auto-update)

    Relations:
        - asignaciones: List[AsignacionItem]  (one-to-many)

    Methods:
        - crear(nombre, apellido, email, telefono?) -> Usuario
        - actualizar(id, datos) -> Usuario
        - eliminar(id) -> bool
        - obtener(id) -> Usuario
        - listar(activo?) -> List[Usuario]
        - obtener_asignaciones(id) -> List[AsignacionItem]
