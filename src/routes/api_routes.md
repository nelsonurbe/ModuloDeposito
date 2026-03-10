# API Routes - ModuloDeposito

## Depósitos

| Método | Ruta                          | Descripción                         |
|--------|-------------------------------|-------------------------------------|
| GET    | /api/depositos                | Listar todos los depósitos          |
| GET    | /api/depositos/:id            | Obtener un depósito por ID          |
| POST   | /api/depositos                | Crear un nuevo depósito             |
| PUT    | /api/depositos/:id            | Actualizar un depósito              |
| DELETE | /api/depositos/:id            | Eliminar (desactivar) un depósito   |
| GET    | /api/depositos/:id/items      | Listar ítems de un depósito         |

## Usuarios

| Método | Ruta                              | Descripción                          |
|--------|-----------------------------------|--------------------------------------|
| GET    | /api/usuarios                     | Listar todos los usuarios            |
| GET    | /api/usuarios/:id                 | Obtener un usuario por ID            |
| POST   | /api/usuarios                     | Crear un nuevo usuario               |
| PUT    | /api/usuarios/:id                 | Actualizar un usuario                |
| DELETE | /api/usuarios/:id                 | Eliminar (desactivar) un usuario     |
| GET    | /api/usuarios/:id/asignaciones    | Listar asignaciones de un usuario    |

## Ítems

| Método | Ruta                          | Descripción                         |
|--------|-------------------------------|-------------------------------------|
| GET    | /api/items                    | Listar todos los ítems              |
| GET    | /api/items/:id                | Obtener un ítem por ID              |
| POST   | /api/items                    | Crear un nuevo ítem                 |
| PUT    | /api/items/:id                | Actualizar un ítem                  |
| DELETE | /api/items/:id                | Eliminar (desactivar) un ítem       |

## Asignaciones

| Método | Ruta                                      | Descripción                              |
|--------|-------------------------------------------|------------------------------------------|
| GET    | /api/asignaciones                         | Listar todas las asignaciones            |
| GET    | /api/asignaciones/:id                     | Obtener una asignación por ID            |
| POST   | /api/asignaciones                         | Crear una nueva asignación               |
| PUT    | /api/asignaciones/:id/estado              | Actualizar el estado de una asignación   |
| DELETE | /api/asignaciones/:id                     | Cancelar una asignación                  |
