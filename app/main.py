from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Usuario, Libro, Editorial, RolUsuarioEnum, EstadoLibroEnum

engine = create_engine("sqlite:///biblioteca.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def crear_usuario():
    print("\n--- Crear Usuario ---")
    nombre = input("Nombre: ")
    email = input("Email: ")
    telefono = input("Teléfono: ")
    rol = input("Rol (lector, administrador, invitado): ")

    if rol not in RolUsuarioEnum.__members__:
        print("Rol inválido.")
        return

    usuario = Usuario(
        nombre=nombre,
        email=email,
        telefono=telefono,
        rol=RolUsuarioEnum[rol]
    )
    session.add(usuario)
    session.commit()
    print("Usuario creado con éxito.")

def ver_usuarios():
    print("\n--- Lista de Usuarios ---")
    usuarios = session.query(Usuario).all()
    for u in usuarios:
        print(f"{u.id} - {u.nombre} ({u.email}) - {u.rol.value}")

def crear_libro():
    print("\n--- Crear Libro ---")
    titulo = input("Título: ")
    isbn = input("ISBN: ")
    anio = int(input("Año de publicación: "))
    estado = input("Estado (activo, danado, perdido): ")

    if estado not in EstadoLibroEnum.__members__:
        print("Estado inválido.")
        return

    nombre_editorial = input("Nombre de la editorial: ")

    # Reutilizar editorial si ya existe
    editorial = session.query(Editorial).filter_by(nombre=nombre_editorial).first()
    if not editorial:
        editorial = Editorial(nombre=nombre_editorial)
        session.add(editorial)
        session.commit()

    libro = Libro(
        titulo=titulo,
        isbn=isbn,
        anio_publicacion=anio,
        estado=EstadoLibroEnum[estado],
        editorial=editorial
    )
    session.add(libro)
    session.commit()
    print("Libro creado con exito.")

def ver_libros():
    print("\n--- Lista de Libros ---")
    libros = session.query(Libro).all()
    for l in libros:
        print(f"{l.id} - {l.titulo} ({l.estado.value}) - {l.editorial.nombre}")

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Crear usuario")
        print("2. Ver usuarios")
        print("3. Crear libro")
        print("4. Ver libros")
        print("5. Salir")
        opcion = input("Elige una opcion: ")

        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            ver_usuarios()
        elif opcion == "3":
            crear_libro()
        elif opcion == "4":
            ver_libros()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida")

if __name__ == "__main__":
    menu()
