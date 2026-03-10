# ModuloDeposito

Módulo de registro de depósitos, ítems y usuarios. Permite asignar ítems a usuarios, registrando el depósito de origen y el traslado correspondiente.

---

## Estructura del Proyecto

```
ModuloDeposito/
├── database/
│   ├── schema.sql        # Definición de tablas y relaciones
│   └── seed.sql          # Datos de ejemplo
├── src/
│   ├── models/
│   │   ├── Deposito.md
│   │   ├── Usuario.md
│   │   ├── Item.md
│   │   └── AsignacionItem.md
│   ├── controllers/      # Lógica de negocio
│   ├── routes/
│   │   └── api_routes.md # Definición de endpoints REST
│   ├── middleware/       # Middleware (auth, validación, etc.)
│   └── config/           # Configuración de la aplicación
└── docs/
    └── diagrama_ER.txt   # Diagrama Entidad-Relación
```

---

## Entidades

### Depósito (`depositos`)
Representa los depósitos físicos donde se almacenan los ítems.

| Campo           | Tipo         | Descripción                     |
|-----------------|--------------|---------------------------------|
| id              | INT (PK)     | Identificador único             |
| nombre          | VARCHAR(100) | Nombre del depósito             |
| ubicacion       | VARCHAR(200) | Ubicación física                |
| descripcion     | TEXT         | Descripción detallada           |
| activo          | BOOLEAN      | Estado activo/inactivo          |
| creado_en       | DATETIME     | Fecha de creación               |
| actualizado_en  | DATETIME     | Fecha de última actualización   |

---

### Usuario (`usuarios`)
Personas que pueden recibir ítems extraídos de los depósitos.

| Campo           | Tipo         | Descripción                     |
|-----------------|--------------|---------------------------------|
| id              | INT (PK)     | Identificador único             |
| nombre          | VARCHAR(100) | Nombre                          |
| apellido        | VARCHAR(100) | Apellido                        |
| email           | VARCHAR(150) | Email único                     |
| telefono        | VARCHAR(20)  | Teléfono de contacto            |
| activo          | BOOLEAN      | Estado activo/inactivo          |
| creado_en       | DATETIME     | Fecha de creación               |
| actualizado_en  | DATETIME     | Fecha de última actualización   |

---

### Ítem (`items`)
Artículos o materiales almacenados en los depósitos.

| Campo           | Tipo         | Descripción                         |
|-----------------|--------------|-------------------------------------|
| id              | INT (PK)     | Identificador único                 |
| codigo          | VARCHAR(50)  | Código único del ítem               |
| nombre          | VARCHAR(150) | Nombre del ítem                     |
| descripcion     | TEXT         | Descripción detallada               |
| cantidad        | INT          | Cantidad disponible                 |
| deposito_id     | INT (FK)     | Depósito al que pertenece           |
| activo          | BOOLEAN      | Estado activo/inactivo              |
| creado_en       | DATETIME     | Fecha de creación                   |
| actualizado_en  | DATETIME     | Fecha de última actualización       |

---

### Asignación de Ítems (`asignacion_items`)
Registro de extracción y traslado de ítems desde un depósito hacia un usuario.

| Campo           | Tipo         | Descripción                                          |
|-----------------|--------------|------------------------------------------------------|
| id              | INT (PK)     | Identificador único                                  |
| usuario_id      | INT (FK)     | Usuario que recibe el ítem                           |
| item_id         | INT (FK)     | Ítem asignado                                        |
| deposito_id     | INT (FK)     | Depósito de origen                                   |
| cantidad        | INT          | Cantidad asignada                                    |
| estado          | ENUM         | `pendiente`, `entregado`, `devuelto`, `cancelado`    |
| notas           | TEXT         | Observaciones adicionales                            |
| asignado_en     | DATETIME     | Fecha de la asignación                               |
| actualizado_en  | DATETIME     | Fecha de última actualización                        |

---

## Diagrama Entidad-Relación

```
depositos ──< items ──< asignacion_items >── usuarios
                              │
                              └──> depositos
```

- Un **depósito** puede tener muchos **ítems**.
- Un **ítem** puede tener muchas **asignaciones**.
- Un **usuario** puede tener muchas **asignaciones**.
- Una **asignación** registra el depósito de origen, el ítem y el usuario destinatario.

---

## Base de Datos

El esquema SQL completo se encuentra en [`database/schema.sql`](database/schema.sql).  
Datos de ejemplo para pruebas en [`database/seed.sql`](database/seed.sql).

---

## API REST

Los endpoints disponibles se detallan en [`src/routes/api_routes.md`](src/routes/api_routes.md).

### Resumen de rutas

| Recurso        | Prefijo             |
|----------------|---------------------|
| Depósitos      | `/api/depositos`    |
| Usuarios       | `/api/usuarios`     |
| Ítems          | `/api/items`        |
| Asignaciones   | `/api/asignaciones` |
