# Proyecto Final - Biblioteca

Este proyecto fue desarrollado para el curso de Bases de Datos 1. Consiste en un sistema CRUD completo para la gestión de una biblioteca utilizando SQLite y SQLAlchemy como ORM. El proyecto cumple con todos los requisitos establecidos en las instrucciones, incluyendo la creación de vistas, validaciones, restricciones, triggers y funciones.

## Estructura del Proyecto

- `main.py`: Archivo principal para ejecutar la aplicación.
- `models.py`: Definición de los modelos ORM con relaciones.
- `functions.py`: Contiene funciones auxiliares y de negocio.
- `schema.sql`: Script para crear toda la base de datos con tablas, vistas, triggers y funciones.
- `data.sql`: Script para poblar la base de datos con más de 1000 datos simulados.
- `diagrama.png`: Diagrama E-R de la base de datos.
- `capturas/`: Carpeta con evidencias del funcionamiento del sistema.
- `informe.pdf`: Documento con introducción, diagrama, capturas y reflexión.
- `README.md`: Este archivo.

## Requisitos

- Python 3
- SQLite
- SQLAlchemy

## Instrucciones de ejecución

1. Crear la base de datos con el esquema:

   ```bash
   sqlite3 biblioteca.db < schema.sql
   ```

2. Insertar los datos:

   ```bash
   sqlite3 biblioteca.db < data.sql
   ```

3. Ejecutar el sistema:
   ```bash
   python main.py
   ```

## Créditos

Desarrollado por Juan Cruz 23110
