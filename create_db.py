"""
Crea una conexión a la base de datos SQLite y crea una tabla llamada "FAMILIA" 
con los siguientes campos:
- ID: un número entero que actúa como clave primaria y se autoincrementa.
- NOMBRE: una cadena de caracteres de hasta 50 caracteres que no puede ser nula.
- NACIMIENTO: una fecha.
- DEFUNCION: una fecha.
- PADRES: un número entero que hace referencia al campo "ID" de la tabla "FAMILIA".
- HIJOS: un número entero que hace referencia al campo "ID" de la tabla "FAMILIA".
- HERMANOS: un número entero que hace referencia al campo "ID" de la tabla "FAMILIA".
- CONYUGE: un número entero que hace referencia al campo "ID" de la tabla "FAMILIA".

Además, se crean datos ficticios para probar la base de datos.
"""

import sqlite3

# -----------------------------CONEXION BBDD------------------------------
personas = []

miConex = sqlite3.connect("familia.db")
cursor = miConex.cursor()
print("Successfully Connected to SQLite")

# esquema de la base de datos
cursor.execute(
                """--sql
                CREATE TABLE FAMILIA (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE VARCHAR(50) NOT NULL,
                NACIMIENTO DATE,
                DEFUNCION DATE,
                PADRES INTEGER REFERENCES FAMILIA(ID),
                HIJOS INTEGER REFERENCES FAMILIA(ID),
                HERMANOS INTEGER REFERENCES FAMILIA(ID),
                CONYUGE INTEGER REFERENCES FAMILIA(ID))
                """
)

# Datos ficticios para probar
inputSQL = [
    (1, "Peter Johnson", "1960-05-20", "2010-07-20", "NULL", "3, 4, 5", "NULL", 2),
    (2, "Sarah Thompson", "1965-09-10", "2015-03-15", "NULL", "3, 4, 5", "NULL", 1),
    (3, "Adam Johnson", "1985-03-25", "NULL", "1, 2", "NULL", "4, 5", "NULL"),
    (4, "Emily Johnson", "1990-07-15", "2020-01-05", "1, 2", "NULL", "3, 5", "NULL"),
    (5, "Daniel Johnson", "1995-11-30", "NULL", "1, 2", "7, 8, 9", "3, 4", 6),
    (6, "Laura Miller", "1997-04-05", "NULL", "NULL", "7, 8, 9", "NULL", 5),
    (7, "Liam Johnson", "2020-02-12", "NULL", "5, 6", "NULL", "8, 9", "NULL"),
    (8, "Sophia Johnson", "2022-08-20", "NULL", "5, 6", "NULL", "7, 9", "NULL"),
    (9, "Mia Johnson", "2024-01-10", "NULL", "5, 6", "NULL", "7, 8", "NULL"),
]

cursor.executemany("INSERT INTO FAMILIA VALUES (?,?,?,?,?,?,?,?)", inputSQL)

miConex.commit()

print("La base de datos se ha creado")

# comprobamos que se han insertado los datos
cursor.execute("SELECT nombre FROM FAMILIA")
nombres = cursor.fetchall()
print(nombres[0:5])


miConex.close()
