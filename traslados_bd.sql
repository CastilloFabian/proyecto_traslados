-- ----------------------------------------------
-- BASE DE DATOS: traslados_bd (versión corregida)
-- ----------------------------------------------

-- Eliminar y crear base de datos
DROP DATABASE IF EXISTS traslados_bd;
CREATE DATABASE traslados_bd CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
USE traslados_bd;

-- Tabla: hospitales
CREATE TABLE hospitales (
  id_hospital INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  direccion VARCHAR(100),
  email VARCHAR(100)
);

-- Tabla: beneficiario
CREATE TABLE beneficiario (
  id_beneficiario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  dni VARCHAR(20) NOT NULL,
  fecha_nacimiento DATE,
  sexo ENUM('M', 'F', 'Otro'),
  diagnostico_emisor TEXT,
  diagnostico_receptor TEXT,
  fecha_ingreso DATE,
  fecha_egreso DATE
);

-- Tabla: camas
CREATE TABLE camas (
  id_cama INT AUTO_INCREMENT PRIMARY KEY,
  id_hospital INT NOT NULL,
  id_beneficiario INT DEFAULT NULL,
  numero_cama VARCHAR(10),
  estado ENUM('Libre','Ocupada') DEFAULT 'Libre',
  tipo_cama ENUM('UCI','Normal','Pediátrica','Otro'),
  FOREIGN KEY (id_hospital) REFERENCES hospitales(id_hospital),
  FOREIGN KEY (id_beneficiario) REFERENCES beneficiario(id_beneficiario)
);

-- Tabla: especialistas
CREATE TABLE especialistas (
  id_especialista INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  especialidad VARCHAR(50),
  telefono VARCHAR(20),
  email VARCHAR(100),
  id_hospital INT,
  FOREIGN KEY (id_hospital) REFERENCES hospitales(id_hospital)
);

-- ---------------------------------------
-- DATOS DE EJEMPLO
-- ---------------------------------------

-- Hospitales
INSERT INTO hospitales (nombre, direccion, email) VALUES
('LLANO', 'LLANO 100', 'llano@gmail.com'),
('ESCUELA', 'ESCUELA 100', 'escuela@gmail.com');

-- Beneficiarios
INSERT INTO beneficiario (nombre, apellido, dni, fecha_nacimiento, sexo, diagnostico_emisor, diagnostico_receptor, fecha_ingreso, fecha_egreso) VALUES
('SOFIA', 'LLANES', '12345678', '1990-05-10', 'F', 'Dolor abdominal', 'Apendicitis', '2025-09-01', '2025-09-05'),
('FABIAN', 'CASTILLO', '36316013', '1991-06-04', 'M', 'Insuficiencia respiratoria', 'Neumonía', '2025-09-10', NULL),
('LUNA', 'CASTILLO', '20231234', '2023-08-15', 'P', 'Fiebre alta', 'Infección viral', '2025-09-15', NULL),
('YUNI', 'MACIEL', '19913456', NULL, NULL, '', '', NULL, NULL);

-- Camas
INSERT INTO camas (id_hospital, id_beneficiario, numero_cama, estado, tipo_cama) VALUES
(1, 1, 'C101', 'Ocupada', 'UCI'),
(2, 2, 'C202', 'Ocupada', 'Normal'),
(2, 3, 'C203', 'Ocupada', 'Pediátrica'),
(2, NULL, 'C204', 'Libre', 'Normal'),
(1, NULL, 'C105', 'Libre', 'UCI');

-- Especialistas
INSERT INTO especialistas (nombre, especialidad, telefono, email, id_hospital) VALUES
('Dr. Juan Pérez', 'Cardiología', '123456789', 'juan.perez@hospital.com', 1),
('Dra. Laura Gómez', 'Pediatría', '987654321', 'laura.gomez@hospital.com', 2);
