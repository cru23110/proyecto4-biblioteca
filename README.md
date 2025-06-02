# Proyecto Final - Biblioteca

Este proyecto fue desarrollado para el curso de Bases de Datos 1. Es un sistema CRUD completo que gestiona una biblioteca utilizando SQLite y SQLAlchemy como ORM. Cumple con todos los requisitos solicitados en el laboratorio, incluyendo relaciones, validaciones, restricciones, triggers, vistas y tipos personalizados.

## Archivos del repositorio

- `app/main.py`: Archivo principal para ejecutar la aplicación.
- `app/models.py`: Definición de los modelos ORM con relaciones.
- `schema.sql`: Script para crear toda la base de datos.
- `data.sql`: Script que inserta más de 1000 datos simulados.

## Requisitos

- Python 3
- SQLite
- SQLAlchemy

## Instrucciones para correr el sistema

1. Crear la base de datos vacía:
   ```bash
   sqlite3 biblioteca.db
   ```

2. Ejecutar el esquema:
   ```bash
   .read schema.sql
   ```

3. Cargar los datos:
   ```bash
   .read data.sql
   ```

4. Ejecutar el sistema:
   ```bash
   python app/main.py
   ```

## Créditos

Desarrollado por Juan Cruz 23110