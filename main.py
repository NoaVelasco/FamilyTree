#!/usr/bin/env python3
# Python 3.10.2 UTF-8
# 2022, noave
# pylint: disable=C0103


"""
Recupera información sobre un miembro de la familia basada en el nombre seleccionado
de la base de datos y llena varios elementos de GUI con la información recuperada.
"""

import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText

# -----------------------------CONEXION BBDD------------------------------

# Se conecta a la base de datos de SQLite y recupera los nombres de los miembros
# de la familia de la tabla "FAMILIA". Luego, los nombres se ordenan alfabéticamente
# y se agregan a la lista "opciones".


opciones = []
actualizado = "09-04-2024"

miConex = sqlite3.connect("familia.db")
cursor = miConex.cursor()

sql = "SELECT nombre FROM FAMILIA"
cursor.execute(sql)
nombres = cursor.fetchall()

# Para que los nombres no aparezcan entre llaves y salgan ordenados alf.
for nombre in sorted(nombres):
    opciones.append(nombre[0])


# ------------FUNCION-------------------------------------------


def buscaFamiliar(event):
    """
    Define la función "buscaFamiliar" que se ejecuta en respuesta a un evento.
    Toma el nombre seleccionado de un combo box y ejecuta una consulta
    SQL para recuperar todos los campos de la tabla "FAMILIA"
    donde el nombre coincide con el nombre seleccionado.
    Luego, borra el contenido de varios elementos de GUI y actualiza
    el contenido de otros elementos de GUI con la información recuperada.
    """

    opcion = mycombo.get()
    cursor.execute(f"SELECT * FROM FAMILIA WHERE nombre='{opcion}'")
    campos = cursor.fetchall()

    ent4pad.delete(1.0, END)
    ent5hij.delete(1.0, END)
    ent6her.delete(1.0, END)
    ent7con.delete(1.0, END)

    # No hacer caso del warning. Así sí funciona, de la otra forma, no.
    nacPrint.set(campos[0][2]) if campos[0][2] != "NULL" else nacPrint.set("?")
    defPrint.set(campos[0][3]) if campos[0][3] != "NULL" else defPrint.set("")


    if isinstance(campos[0][4], int):
        padres = campos[0][4]
        cursor.execute("SELECT NOMBRE FROM FAMILIA WHERE ID=" + str(padres))
        resultpadres = cursor.fetchone()

        ent4pad.insert(1.0, resultpadres[0])

    else:
        if campos[0][4] != "NULL":

            padres = tuple(campos[0][4].split(", "))

            indexCont = 0

            for padre in padres:
                padre = int(padre)
                cursor.execute(
                    "SELECT NOMBRE FROM FAMILIA WHERE ID=" + padres[indexCont]
                )
                resultpadres = cursor.fetchone()

                ent4pad.insert(1.0, resultpadres[0] + "\n")
                indexCont += 1

    if isinstance(campos[0][5], int):
        hijos = campos[0][5]
        cursor.execute("SELECT NOMBRE FROM FAMILIA WHERE ID=" + str(hijos))
        resultHijos = cursor.fetchone()

        ent5hij.insert(1.0, resultHijos[0])

    else:
        if campos[0][5] != "NULL":

            hijos = tuple(campos[0][5].split(", "))

            indexCont = 0

            for hijo in hijos:
                hijo = int(hijo)
                cursor.execute(
                    "SELECT NOMBRE FROM FAMILIA WHERE ID=" + hijos[indexCont]
                )
                resultHijos = cursor.fetchone()

                # print(resultHijos[0])
                ent5hij.insert(1.0, resultHijos[0] + "\n")
                indexCont += 1

    if isinstance(campos[0][6], int):
        hermanos = campos[0][6]
        cursor.execute("SELECT NOMBRE FROM FAMILIA WHERE ID=" + str(hermanos))
        resultHermanos = cursor.fetchone()

        ent6her.insert(1.0, resultHermanos[0])

    else:
        if campos[0][6] != "NULL":

            hermanos = tuple(campos[0][6].split(", "))

            indexCont = 0

            for hermano in hermanos:
                hermano = int(hermano)
                cursor.execute(
                    "SELECT NOMBRE FROM FAMILIA WHERE ID=" + hermanos[indexCont]
                )
                resultHermanos = cursor.fetchone()

                # print(resultHermanos[0])
                ent6her.insert(1.0, resultHermanos[0] + "\n")
                indexCont += 1

    if isinstance(campos[0][7], int):
        conyug = campos[0][7]
        cursor.execute("SELECT NOMBRE FROM FAMILIA WHERE ID=" + str(conyug))
        resultconyug = cursor.fetchone()

        # print(resultconyug[0])
        ent7con.insert(1.0, resultconyug[0])

    else:
        if campos[0][7] != "NULL":

            conyug = tuple(campos[0][7].split(", "))

            indexCont = 0

            for con in conyug:
                con = int(con)
                cursor.execute(
                    "SELECT NOMBRE FROM FAMILIA WHERE ID=" + conyug[indexCont]
                )
                resultconyug = cursor.fetchone()

                # print(resultconyug[0])
                ent7con.insert(1.0, resultconyug[0] + "\n")
                indexCont += 1


# ------------TKINTER CONFIG 1------------------------------
win = Tk()
win.config(bg="#054a61")
win.geometry("720x500")
win.title("Árbol genealógico")
win.iconbitmap("tree.ico")


opts = StringVar()
nomPrint = StringVar()
nacPrint = StringVar()
defPrint = StringVar()


tipoGr = Font(family="Roboto Cn", size=12)
tipoPeq = Font(family="Roboto Cn", size=10)

wrapper1 = LabelFrame(
    win, text="Miembro", font=tipoGr, fg="whitesmoke", bg="#054a61", labelanchor="ne"
)
wrapper2 = LabelFrame(
    win,
    text="Relaciones familiares",
    font=tipoGr,
    fg="whitesmoke",
    bg="#054a61",
    width="300",
    labelanchor="ne",
)


wrapper1.pack(padx=10, pady=10, ipadx=10, ipady=10, side="left", anchor="n")
wrapper2.pack(padx=10, pady=10, ipadx=10, ipady=10, side="right", anchor="n")


# ------------FRAME 1--------------------------------
Label(
    wrapper1, text="Selecciona un familiar", font=tipoPeq, fg="whitesmoke", bg="#054a61"
).grid(row=0, column=0, padx=10, pady=5, sticky="ws")

mycombo = ttk.Combobox(wrapper1, textvariable=opts, width=30, font=tipoGr)
mycombo["values"] = opciones
mycombo.grid(row=1, column=0, padx=10, pady=10)
# Si quiero que ponga por defecto una opción del combobox:
# mycombo.current(0)
mycombo.bind("<<ComboboxSelected>>", buscaFamiliar)

lbl2nac = Label(
    wrapper1,
    text="Nacimiento (año-mes-día)",
    font=tipoPeq,
    fg="whitesmoke",
    bg="#054a61",
)
lbl2nac.grid(row=2, column=0, padx=10, pady=2, sticky="w")
ent2nac = Entry(wrapper1, textvariable=nacPrint, width="32", font=tipoGr)
ent2nac.grid(row=3, column=0, padx=10, pady=2, sticky="w")

lbl3def = Label(
    wrapper1,
    text="Defunción (año-mes-día)",
    font=tipoPeq,
    fg="whitesmoke",
    bg="#054a61",
)
lbl3def.grid(row=4, column=0, padx=10, pady=2, sticky="w")
ent3def = Entry(wrapper1, textvariable=defPrint, width="32", font=tipoGr)
ent3def.grid(row=5, column=0, padx=10, pady=2, sticky="w")


# ------------FRAME 2--------------------------------


lbl4pad = Label(wrapper2, text="Padres", font=tipoPeq, fg="whitesmoke", bg="#054a61")
lbl4pad.grid(row=6, column=0, padx=10, pady=2, sticky="w")
ent4pad = Text(wrapper2, width="32", height="2", font=tipoGr)
ent4pad.grid(row=7, column=0, padx=10, pady=2, sticky="w")

lbl5hij = Label(wrapper2, text="Hijos", font=tipoPeq, fg="whitesmoke", bg="#054a61")
lbl5hij.grid(row=8, column=0, padx=10, pady=2, sticky="w")
ent5hij = ScrolledText(wrapper2, width="32", height="5", font=tipoGr)
ent5hij.grid(row=9, column=0, padx=10, pady=2, sticky="w")

lbl6her = Label(wrapper2, text="Hermanos", font=tipoPeq, fg="whitesmoke", bg="#054a61")
lbl6her.grid(row=10, column=0, padx=10, pady=2, sticky="w")
ent6her = ScrolledText(wrapper2, width="32", height="5", font=tipoGr)
ent6her.grid(row=11, column=0, padx=10, pady=2, sticky="w")

lbl7con = Label(
    wrapper2, text="Cónyuge o pareja", font=tipoPeq, fg="whitesmoke", bg="#054a61"
)
lbl7con.grid(row=12, column=0, padx=10, pady=2, sticky="w")
ent7con = Text(wrapper2, width="32", height="2", font=tipoGr)
ent7con.grid(row=13, column=0, padx=10, pady=2, sticky="w")


lbl8info = Label(
    wrapper2,
    text=f"Última actualización: {actualizado}\nnoave",
    font=("Consolas", 8),
    fg="steelblue",
    justify="right",
    bg="#054a61",
)
lbl8info.grid(row=14, column=0, padx=10, pady=20, sticky="se")


# -------------------------FINAL---------------------------------

win.mainloop()
miConex.close()
