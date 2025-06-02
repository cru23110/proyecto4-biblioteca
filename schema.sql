PRAGMA foreign_keys = ON;

-- ENUM simulados (en SQLite no se permite CREATE TYPE, pero lo validamos desde la app)

CREATE TABLE tipos_documento (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

CREATE TABLE editoriales (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE categorias (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE autores (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);

CREATE TABLE usuarios (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  telefono VARCHAR(20),
  rol TEXT CHECK(rol IN ('lector', 'administrador', 'invitado')) NOT NULL,
  tipo_documento_id INTEGER,
  FOREIGN KEY (tipo_documento_id) REFERENCES tipos_documento(id)
);

CREATE TABLE direcciones (
  id INTEGER PRIMARY KEY,
  usuario_id INTEGER,
  calle TEXT,
  ciudad TEXT,
  pais TEXT,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE libros (
  id INTEGER PRIMARY KEY,
  titulo TEXT NOT NULL,
  isbn TEXT UNIQUE NOT NULL,
  anio_publicacion INTEGER,
  estado TEXT CHECK(estado IN ('activo', 'danado', 'perdido')) NOT NULL,
  editorial_id INTEGER,
  FOREIGN KEY (editorial_id) REFERENCES editoriales(id)
);

CREATE TABLE libro_autor (
  libro_id INTEGER,
  autor_id INTEGER,
  PRIMARY KEY (libro_id, autor_id),
  FOREIGN KEY (libro_id) REFERENCES libros(id),
  FOREIGN KEY (autor_id) REFERENCES autores(id)
);

CREATE TABLE libro_categoria (
  libro_id INTEGER,
  categoria_id INTEGER,
  PRIMARY KEY (libro_id, categoria_id),
  FOREIGN KEY (libro_id) REFERENCES libros(id),
  FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE prestamos (
  id INTEGER PRIMARY KEY,
  usuario_id INTEGER,
  fecha_prestamo DATE NOT NULL,
  fecha_devolucion DATE,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE detalle_prestamo (
  prestamo_id INTEGER,
  libro_id INTEGER,
  PRIMARY KEY (prestamo_id, libro_id),
  FOREIGN KEY (prestamo_id) REFERENCES prestamos(id),
  FOREIGN KEY (libro_id) REFERENCES libros(id)
);

CREATE TABLE devoluciones (
  id INTEGER PRIMARY KEY,
  prestamo_id INTEGER,
  fecha_devolucion DATE NOT NULL,
  observaciones TEXT,
  FOREIGN KEY (prestamo_id) REFERENCES prestamos(id)
);

CREATE TABLE sanciones (
  id INTEGER PRIMARY KEY,
  usuario_id INTEGER,
  motivo TEXT NOT NULL,
  fecha DATE NOT NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE comentarios (
  id INTEGER PRIMARY KEY,
  usuario_id INTEGER,
  libro_id INTEGER,
  comentario TEXT,
  fecha DATE,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (libro_id) REFERENCES libros(id)
);

CREATE TABLE log_eventos (
  id INTEGER PRIMARY KEY,
  entidad TEXT NOT NULL,
  accion TEXT NOT NULL,
  fecha DATE DEFAULT CURRENT_DATE
);

-- === TRIGGERS ===

CREATE TRIGGER log_prestamo_insert
AFTER INSERT ON prestamos
BEGIN
  INSERT INTO log_eventos (entidad, accion, fecha)
  VALUES ('prestamos', 'insert', CURRENT_DATE);
END;

CREATE TRIGGER log_libro_delete
AFTER DELETE ON libros
BEGIN
  INSERT INTO log_eventos (entidad, accion, fecha)
  VALUES ('libros', 'delete', CURRENT_DATE);
END;

CREATE TRIGGER log_usuario_insert
AFTER INSERT ON usuarios
BEGIN
  INSERT INTO log_eventos (entidad, accion, fecha)
  VALUES ('usuarios', 'insert', CURRENT_DATE);
END;

-- === VIEWS (simulan funciones) ===

-- View: cantidad de préstamos por usuario
CREATE VIEW vista_prestamos_por_usuario AS
SELECT u.id AS usuario_id, u.nombre, COUNT(p.id) AS cantidad_prestamos
FROM usuarios u
LEFT JOIN prestamos p ON u.id = p.usuario_id
GROUP BY u.id;

-- View: nombre de editorial por libro
CREATE VIEW vista_editorial_por_libro AS
SELECT l.id AS libro_id, l.titulo, e.nombre AS editorial
FROM libros l
JOIN editoriales e ON l.editorial_id = e.id;
