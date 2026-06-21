CREATE DATABASE IF NOT EXISTS supportdesk_db;
USE supportdesk_db;

-- Tabla de Usuarios (Autenticación)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'tecnico', 'empleado') DEFAULT 'tecnico'
);

-- Tabla de Empleados
CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    area VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20)
);

-- Tabla de Técnicos
CREATE TABLE IF NOT EXISTS tecnicos (
    id_tecnico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo'
);

-- Tabla de Categorías
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL
);

-- Tabla de Tickets
CREATE TABLE IF NOT EXISTS tickets (
    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    prioridad ENUM('Baja', 'Media', 'Alta', 'Crítica') DEFAULT 'Baja',
    estado ENUM('Abierto', 'En progreso', 'En espera', 'Resuelto', 'Cerrado') DEFAULT 'Abierto',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_cierre DATETIME NULL,
    empleado_id INT NOT NULL,
    categoria_id INT NOT NULL,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id_categoria)
);

-- Tabla Intermedia (Muchos a muchos: Tickets ↔ Técnicos)
CREATE TABLE IF NOT EXISTS ticket_tecnico (
    id_asignacion INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    tecnico_id INT NOT NULL,
    fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id_ticket),
    FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id_tecnico)
);

-- Tabla de Intervenciones
CREATE TABLE IF NOT EXISTS intervenciones (
    id_intervencion INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    tecnico_id INT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id_ticket),
    FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id_tecnico)
);

-- Datos de prueba iniciales
INSERT INTO usuarios (username, password, rol) VALUES ('admin', 'pbkdf2:sha256:600000$yourhashedpassword', 'admin');
INSERT INTO categorias (nombre_categoria) VALUES ('Hardware'), ('Software'), ('Red'), ('Accesos'), ('Otros');
