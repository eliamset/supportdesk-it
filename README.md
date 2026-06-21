# 📋 SupportDesk IT — Sistema de Gestión de Mesa de Ayuda

> Sistema web desarrollado en **Python + Flask** para la gestión integral de tickets de soporte técnico en empresas. Permite registrar incidentes, asignar técnicos, hacer seguimiento y generar reportes de desempeño.

---

## 🗂️ Tabla de Contenido

1. [Descripción General](#1-descripción-general)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Instalación y Configuración](#3-instalación-y-configuración)
4. [Estructura del Proyecto](#4-estructura-del-proyecto)
5. [Modelos de Datos](#5-modelos-de-datos)
6. [Roles de Usuario](#6-roles-de-usuario)
7. [Funcionalidades y Rutas](#7-funcionalidades-y-rutas)
8. [Reglas de Negocio](#8-reglas-de-negocio)
9. [Guía de Uso](#9-guía-de-uso)
10. [Datos de Prueba (Seed)](#10-datos-de-prueba-seed)

---

## 1. Descripción General

**SupportDesk IT** es una aplicación web de gestión de mesa de ayuda (Help Desk) que permite a las organizaciones gestionar el ciclo de vida completo de un ticket de soporte:

- ✅ Creación y registro de tickets por parte de empleados
- ✅ Asignación de técnicos especializados
- ✅ Registro de intervenciones y avances
- ✅ Control de estados y prioridades
- ✅ Reportes de desempeño por técnico
- ✅ Autenticación segura con roles

**Stack tecnológico:**

| Capa | Tecnología |
|---|---|
| Backend | Python 3, Flask 2.3 |
| ORM | Flask-SQLAlchemy 3.1 |
| Autenticación | Flask-Login 0.6 |
| Base de datos | MySQL (via PyMySQL) |
| Hashing | Werkzeug (PBKDF2) |
| Frontend | Jinja2 Templates + CSS/JS |

---

## 2. Requisitos del Sistema

Antes de instalar, asegúrate de tener:

- **Python 3.10+** instalado
- **MySQL 8.0+** (XAMPP, MySQL Workbench, o servidor dedicado)
- **pip** (gestor de paquetes de Python)
- Conexión a red local para acceso desde otros equipos (opcional)

---

## 3. Instalación y Configuración

### Paso 1 — Clonar / Ubicar el proyecto

El proyecto debe estar en:
```
C:\Users\Windows 10Pro\Desktop\Sistema de Gestión de Mesa de Ayuda — SupportDesk IT\
```

### Paso 2 — Crear entorno virtual (recomendado)

Abre una terminal (PowerShell) en la carpeta del proyecto:

```powershell
# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual
.\venv\Scripts\Activate
```

> Sabrás que está activo cuando veas `(venv)` al inicio de la línea en la terminal.

### Paso 3 — Instalar dependencias

```powershell
pip install -r requirements.txt
```

Esto instalará:

| Paquete | Versión | Función |
|---|---|---|
| Flask | 2.3.3 | Framework web |
| Flask-SQLAlchemy | 3.1.1 | ORM para base de datos |
| Flask-Login | 0.6.2 | Gestión de sesiones de usuario |
| PyMySQL | 1.1.0 | Conector MySQL para Python |
| python-dotenv | 1.0.0 | Variables de entorno |
| cryptography | 41.0.3 | Seguridad en conexión MySQL |

### Paso 4 — Configurar la Base de Datos MySQL

#### 4a. Crear la base de datos (Automático)

El archivo `run.py` está configurado para crear automáticamente la base de datos `supportdesk_db` al ejecutarse, siempre que los datos de conexión sean correctos. No necesitas hacerlo manualmente. 

Si prefieres hacerlo de forma manual, puedes usar tu cliente MySQL y ejecutar:
```sql
CREATE DATABASE IF NOT EXISTS supportdesk_db;
```

Abre el archivo `config.py` y verifica que la cadena de conexión coincida con tu MySQL:

```python
# config.py — Línea 11
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:SENA@localhost/supportdesk_db'
#                                           ^^^^  ^^^^
#                                           user  password
```

> **Importante:** Si tu MySQL tiene contraseña diferente a `SENA`, cámbiala aquí. Si no tiene contraseña, usa: `mysql+pymysql://root:@localhost/supportdesk_db`

#### 4c. Variable de entorno (opcional — más seguro)

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=mi-clave-secreta-muy-segura
DATABASE_URL=mysql+pymysql://root:mi_contraseña@localhost/supportdesk_db
```

### Paso 5 — Poblar la base de datos con datos de prueba

```powershell
python seed.py
```

Esto creará automáticamente:
- 👤 Usuarios de prueba (admin, técnicos, empleados)
- 🗂️ Categorías base (Hardware, Software, Red, Accesos, Otros)
- 👥 Empleados y técnicos de ejemplo
- 🎫 Tickets de prueba con diferentes estados
- 📝 Intervenciones registradas

### Paso 6 — Ejecutar la aplicación

```powershell
python run.py
```

La aplicación iniciará en modo desarrollo. Accede desde tu navegador:

```
http://127.0.0.1:5000
```

> Si ves `* Running on http://127.0.0.1:5000` en la terminal, ¡el sistema está listo!

---

## 4. Estructura del Proyecto

```
SupportDesk IT/
│
├── run.py                  # Punto de entrada — inicia la aplicación Flask
├── config.py               # Configuración: DB, clave secreta
├── seed.py                 # Script para poblar la BD con datos de prueba
├── requirements.txt        # Dependencias Python del proyecto
│
├── database/
│   └── schema.sql          # Script SQL para crear la base de datos y tablas
│
├── app/
│   ├── __init__.py         # App Factory: ensambla Flask, DB y Blueprints
│   │
│   ├── models/             # Capa de datos (ORM)
│   │   ├── __init__.py     # Exporta todos los modelos
│   │   ├── user.py         # Modelo Usuario + autenticación
│   │   ├── employee.py     # Modelo Empleado
│   │   ├── technician.py   # Modelo Técnico
│   │   ├── category.py     # Modelo Categoría
│   │   ├── ticket.py       # Modelo Ticket + tabla intermedia
│   │   └── intervention.py # Modelo Intervención
│   │
│   ├── routes/             # Controladores (Blueprints)
│   │   ├── __init__.py     # Exporta los blueprints
│   │   ├── auth.py         # Login / Logout
│   │   ├── user.py         # CRUD y Roles de Usuarios (Solo Admin)
│   │   ├── main.py         # Dashboard principal
│   │   ├── employee.py     # CRUD de Empleados
│   │   ├── technician.py   # CRUD de Técnicos
│   │   ├── category.py     # CRUD de Categorías
│   │   ├── ticket.py       # Gestión completa de Tickets
│   │   └── report.py       # Reportes y estadísticas
│   │
│   ├── templates/          # Plantillas HTML (Jinja2)
│   │   ├── base.html       # Plantilla base (navbar, layout)
│   │   ├── auth/           # Login
│   │   ├── user/           # Vistas de gestión de usuarios
│   │   ├── dashboard/      # Pantalla principal
│   │   ├── employee/       # Vistas de empleados
│   │   ├── technician/     # Vistas de técnicos
│   │   ├── category/       # Vistas de categorías
│   │   ├── ticket/         # Vistas de tickets (lista, detalle, formulario)
│   │   └── report/         # Vistas de reportes
│   │
│   └── static/             # Archivos estáticos
│       ├── css/            # Hojas de estilo
│       ├── js/             # Scripts JavaScript
│       └── img/            # Imágenes y logos
```

---

## 5. Modelos de Datos

### Diagrama de relaciones

```
usuarios ─────────────────────────────────────────
                                                  │ (autenticación separada)
empleados ──────────┐                             
                    │ tiene muchos                 
categorias ─────────┤                             
                    │                             
                  tickets ──────────── ticket_tecnico ──── tecnicos
                    │                  (N a N)
                    │ tiene muchos
                  intervenciones ────── tecnicos
```

### Tabla: `usuarios`

| Campo | Tipo | Descripción |
|---|---|---|
| id_usuario | INT PK | Identificador único |
| username | VARCHAR(50) | Nombre de usuario (único) |
| password | VARCHAR(255) | Contraseña hasheada (PBKDF2) |
| rol | ENUM | `admin`, `tecnico`, `empleado` |

### Tabla: `empleados`

| Campo | Tipo | Descripción |
|---|---|---|
| id_empleado | INT PK | Identificador único |
| nombre | VARCHAR(100) | Nombre completo |
| area | VARCHAR(100) | Departamento o área |
| correo | VARCHAR(100) | Email corporativo (único) |
| telefono | VARCHAR(20) | Teléfono de contacto |

### Tabla: `tecnicos`

| Campo | Tipo | Descripción |
|---|---|---|
| id_tecnico | INT PK | Identificador único |
| nombre | VARCHAR(100) | Nombre completo |
| especialidad | VARCHAR(100) | Área de expertise |
| estado | ENUM | `activo` / `inactivo` |

### Tabla: `categorias`

| Campo | Tipo | Descripción |
|---|---|---|
| id_categoria | INT PK | Identificador único |
| nombre_categoria | VARCHAR(100) | Nombre de la categoría |

Categorías base: **Hardware, Software, Red, Accesos, Otros**

### Tabla: `tickets`

| Campo | Tipo | Descripción |
|---|---|---|
| id_ticket | INT PK | Identificador único |
| descripcion | TEXT | Descripción del problema |
| prioridad | ENUM | `Baja`, `Media`, `Alta`, `Crítica` |
| estado | ENUM | `Abierto`, `En progreso`, `En espera`, `Resuelto`, `Cerrado` |
| fecha_creacion | DATETIME | Automático al crear |
| fecha_cierre | DATETIME | Se registra al cerrar el ticket |
| empleado_id | FK | Quién reportó el problema |
| categoria_id | FK | Tipo de problema |

### Tabla: `ticket_tecnico` (intermedia N:M)

| Campo | Tipo | Descripción |
|---|---|---|
| id_asignacion | INT PK | Identificador |
| ticket_id | FK | Ticket asignado |
| tecnico_id | FK | Técnico asignado |
| fecha_asignacion | DATETIME | Cuándo se asignó |

### Tabla: `intervenciones`

| Campo | Tipo | Descripción |
|---|---|---|
| id_intervencion | INT PK | Identificador único |
| ticket_id | FK | Ticket al que pertenece |
| tecnico_id | FK | Técnico que intervino |
| descripcion | TEXT | Descripción de la acción tomada |
| fecha | DATETIME | Fecha y hora de la intervención |

---

## 6. Roles de Usuario

| Rol | Descripción | Accesos |
|---|---|---|
| **admin** | Administrador del sistema | Acceso total: tickets, empleados, técnicos, categorías, reportes |
| **tecnico** | Técnico de soporte | Ver tickets, registrar intervenciones, actualizar estados |
| **empleado** | Empleado que reporta | Crear tickets propios, consultar estado |

> **Nota:** La lógica de restricción por rol se implementa en las rutas mediante el objeto `current_user` de Flask-Login.

---

## 7. Funcionalidades y Rutas

### Autenticación — `/`

| Método | URL | Descripción |
|---|---|---|
| GET/POST | `/login` | Pantalla de inicio de sesión |
| GET | `/logout` | Cerrar sesión |

### Dashboard — `/`

| Método | URL | Descripción |
|---|---|---|
| GET | `/` | Panel principal con resumen del sistema |

### Usuarios (Módulo Admin) — `/users`

| Método | URL | Descripción |
|---|---|---|
| GET | `/users/` | Listado general de usuarios y roles (Solo admin) |
| GET/POST | `/users/create` | Crear nuevo usuario con rol y contraseña |
| GET/POST | `/users/update/<id>` | Editar usuario y permisos |
| POST | `/users/delete/<id>` | Eliminar usuario |

### Tickets — `/tickets`

| Método | URL | Descripción |
|---|---|---|
| GET | `/tickets/` | Listado de tickets (con filtros por estado, prioridad, técnico) |
| GET/POST | `/tickets/create` | Formulario para crear un nuevo ticket |
| GET | `/tickets/view/<id>` | Vista detallada de un ticket |
| POST | `/tickets/assign/<id>` | Asignar un técnico a un ticket |
| POST | `/tickets/intervention/<id>` | Agregar una intervención al ticket |
| POST | `/tickets/update_status/<id>` | Cambiar el estado del ticket |
| POST | `/tickets/update_priority/<id>` | Cambiar la prioridad del ticket |

### Empleados — `/employees`

| Método | URL | Descripción |
|---|---|---|
| GET | `/employees/` | Listado de empleados |
| GET/POST | `/employees/create` | Crear empleado |
| GET/POST | `/employees/edit/<id>` | Editar empleado |
| POST | `/employees/delete/<id>` | Eliminar empleado |

### Técnicos — `/technicians`

| Método | URL | Descripción |
|---|---|---|
| GET | `/technicians/` | Listado de técnicos |
| GET/POST | `/technicians/create` | Crear técnico |
| GET/POST | `/technicians/edit/<id>` | Editar técnico |
| POST | `/technicians/delete/<id>` | Eliminar técnico |

### Categorías — `/categories`

| Método | URL | Descripción |
|---|---|---|
| GET | `/categories/` | Listado de categorías |
| GET/POST | `/categories/create` | Crear categoría |
| GET/POST | `/categories/edit/<id>` | Editar categoría |
| POST | `/categories/delete/<id>` | Eliminar categoría |

### Reportes — `/reports`

| Método | URL | Descripción |
|---|---|---|
| GET | `/reports/` | Dashboard de reportes: tickets por estado, desempeño por técnico, tiempo promedio de resolución |

---

## 8. Reglas de Negocio

El sistema aplica automáticamente estas reglas en el backend:

### 🎫 Regla 1 — Sin tickets duplicados
> No se permite crear un ticket con la misma descripción, empleado y categoría en el mismo día.

```python
# En routes/ticket.py — create()
duplicate = Ticket.query.filter(
    Ticket.empleado_id == empleado_id,
    Ticket.categoria_id == categoria_id,
    Ticket.descripcion == descripcion,
    db.func.date(Ticket.fecha_creacion) == today
).first()
```

### 🔒 Regla 2 — Tickets cerrados son inmutables
> Un ticket con estado `Cerrado` no puede ser modificado: no se le asignan técnicos, ni se agregan intervenciones, ni se cambia su estado o prioridad.

### 👷 Regla 3 — No asignar técnicos inactivos
> Solo se pueden asignar técnicos con estado `activo` a los tickets.

### 📝 Regla 4 — Requiere intervención para cerrar
> Un ticket no puede pasar al estado `Cerrado` si no tiene al menos una intervención registrada.

### 🔄 Regla 5 — Cambio automático de estado al intervenir
> Cuando se registra la primera intervención en un ticket `Abierto`, su estado cambia automáticamente a `En progreso`.

### ⚡ Regla 6 — Cambio de prioridad restringido
> La prioridad solo puede modificarse si el ticket está en estado `Abierto` o `En espera`.

---

## 9. Guía de Uso

### 🔐 Iniciar sesión

1. Accede a `http://127.0.0.1:5000/login`
2. Introduce tu usuario y contraseña
3. Serás redirigido al **Dashboard** principal

### 🎫 Crear un Ticket

1. En el menú, haz clic en **"Tickets"** → **"Nuevo Ticket"**
2. Completa el formulario:
   - **Empleado:** Quién reporta el problema
   - **Categoría:** Tipo de incidente (Hardware, Software, etc.)
   - **Prioridad:** Baja / Media / Alta / Crítica
   - **Descripción:** Detalle del problema
3. Haz clic en **"Crear"**

> ⚠️ Si ya existe un ticket igual creado hoy, el sistema lo rechazará.

### 👷 Asignar un Técnico

1. Abre el detalle de un ticket (desde la lista de tickets)
2. En la sección **"Asignar Técnico"**, selecciona el técnico del desplegable
3. Haz clic en **"Asignar"**

> Solo técnicos activos aparecen en la lista. La asignación es N:M (múltiples técnicos por ticket).

### 📝 Registrar una Intervención

1. Dentro del detalle del ticket, busca la sección **"Nueva Intervención"**
2. Escribe la descripción de las acciones realizadas
3. Selecciona el técnico que intervino
4. Haz clic en **"Registrar"**

> Al registrar la primera intervención, el ticket cambiará automáticamente a **"En progreso"**.

### 🔄 Cambiar Estado del Ticket

Los estados posibles y su flujo típico son:

```
Abierto → En progreso → En espera → Resuelto → Cerrado
```

1. En el detalle del ticket, busca la sección **"Actualizar Estado"**
2. Selecciona el nuevo estado
3. Haz clic en **"Actualizar"**

> Para cerrar un ticket, debe tener al menos una intervención registrada.

### 📊 Ver Reportes

1. En el menú, haz clic en **"Reportes"**
2. Verás:
   - **Tickets por Estado:** Distribución de todos los tickets
   - **Desempeño por Técnico:** Tickets resueltos, pendientes y tiempo promedio de resolución por cada técnico

---

## 10. Datos de Prueba (Seed)

Al ejecutar `python seed.py`, se crean los siguientes datos:

### Usuarios creados

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador |
| `tecnico01` | `user123` | Técnico |
| `tecnico02` | `user123` | Técnico |
| `empleado01` | `user123` | Empleado |
| `empleado02` | `user123` | Empleado |

### Empleados de prueba

| Nombre | Área |
|---|---|
| Juan Pérez | Contabilidad |
| María Gómez | Recursos Humanos |
| Carlos Ruiz | Operaciones |
| Laura Beltrán | Ventas |

### Técnicos de prueba

| Nombre | Especialidad |
|---|---|
| Luis Torres | Hardware y Soporte Físico |
| Ana Martínez | Redes y Conectividad |
| Jorge Díaz | Sistemas de Software |

### Tickets de prueba

| # | Estado | Prioridad | Descripción breve |
|---|---|---|---|
| 1 | En progreso | Alta | Pantalla no enciende (Hardware) |
| 2 | Abierto | Media | Error de acceso a Outlook (Accesos) |
| 3 | Resuelto | Crítica | Impresora sin conexión de red (Red) |
| 4 | Cerrado | Baja | Instalación de ERP + firma digital (Software) |

---

## ⚡ Comandos Rápidos de Referencia

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate

# Instalar dependencias
pip install -r requirements.txt

# Crear la base de datos (desde MySQL)
mysql -u root -p < database\schema.sql

# Poblar con datos de prueba
python seed.py

# Iniciar el servidor de desarrollo
python run.py
```

---

> **Desarrollado con Flask + Python + MySQL** | SupportDesk IT © 2026
