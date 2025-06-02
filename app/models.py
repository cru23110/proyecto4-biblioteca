from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Enum, Boolean, Table
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Enums
class RolUsuarioEnum(enum.Enum):
    lector = "lector"
    administrador = "administrador"
    invitado = "invitado"

class EstadoLibroEnum(enum.Enum):
    activo = "activo"
    danado = "danado"
    perdido = "perdido"

# Tablas intermedias
libro_autor = Table(
    "libro_autor", Base.metadata,
    Column("libro_id", ForeignKey("libros.id"), primary_key=True),
    Column("autor_id", ForeignKey("autores.id"), primary_key=True)
)

libro_categoria = Table(
    "libro_categoria", Base.metadata,
    Column("libro_id", ForeignKey("libros.id"), primary_key=True),
    Column("categoria_id", ForeignKey("categorias.id"), primary_key=True)
)

# Tablas principales

class TipoDocumento(Base):
    __tablename__ = "tipos_documento"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20))
    rol = Column(Enum(RolUsuarioEnum), nullable=False)
    tipo_documento_id = Column(Integer, ForeignKey("tipos_documento.id"))

    tipo_documento = relationship("TipoDocumento")
    direccion = relationship("Direccion", back_populates="usuario", uselist=False)
    prestamos = relationship("Prestamo", back_populates="usuario")
    comentarios = relationship("Comentario", back_populates="usuario")
    sanciones = relationship("Sancion", back_populates="usuario")

class Direccion(Base):
    __tablename__ = "direcciones"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    calle = Column(String(100))
    ciudad = Column(String(50))
    pais = Column(String(50))

    usuario = relationship("Usuario", back_populates="direccion")

class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True)
    titulo = Column(String(150), nullable=False)
    isbn = Column(String(50), nullable=False, unique=True)
    anio_publicacion = Column(Integer)
    editorial_id = Column(Integer, ForeignKey("editoriales.id"))
    estado = Column(Enum(EstadoLibroEnum), nullable=False)

    editorial = relationship("Editorial", back_populates="libros")
    autores = relationship("Autor", secondary=libro_autor, back_populates="libros")
    categorias = relationship("Categoria", secondary=libro_categoria, back_populates="libros")
    detalles_prestamo = relationship("DetallePrestamo", back_populates="libro")
    comentarios = relationship("Comentario", back_populates="libro")

class Editorial(Base):
    __tablename__ = "editoriales"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

    libros = relationship("Libro", back_populates="editorial")

class Prestamo(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_prestamo = Column(Date)
    fecha_entrega = Column(Date)

    usuario = relationship("Usuario", back_populates="prestamos")
    detalles = relationship("DetallePrestamo", back_populates="prestamo")

class DetallePrestamo(Base):
    __tablename__ = "detalle_prestamo"
    id = Column(Integer, primary_key=True)
    prestamo_id = Column(Integer, ForeignKey("prestamos.id"))
    libro_id = Column(Integer, ForeignKey("libros.id"))

    prestamo = relationship("Prestamo", back_populates="detalles")
    libro = relationship("Libro", back_populates="detalles_prestamo")
    devolucion = relationship("Devolucion", back_populates="detalle", uselist=False)

class Devolucion(Base):
    __tablename__ = "devoluciones"
    id = Column(Integer, primary_key=True)
    detalle_prestamo_id = Column(Integer, ForeignKey("detalle_prestamo.id"))
    fecha_devolucion = Column(Date)
    observaciones = Column(Text)

    detalle = relationship("DetallePrestamo", back_populates="devolucion")

class Autor(Base):
    __tablename__ = "autores"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

    libros = relationship("Libro", secondary=libro_autor, back_populates="autores")

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

    libros = relationship("Libro", secondary=libro_categoria, back_populates="categorias")

class Comentario(Base):
    __tablename__ = "comentarios"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    libro_id = Column(Integer, ForeignKey("libros.id"))
    contenido = Column(Text)
    fecha = Column(Date)

    usuario = relationship("Usuario", back_populates="comentarios")
    libro = relationship("Libro", back_populates="comentarios")

class Sancion(Base):
    __tablename__ = "sanciones"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    motivo = Column(String(255))
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    activa = Column(Boolean)

    usuario = relationship("Usuario", back_populates="sanciones")

class LogEvento(Base):
    __tablename__ = "log_eventos"
    id = Column(Integer, primary_key=True)
    entidad = Column(String(100))
    accion = Column(String(50))
    fecha = Column(Date)
