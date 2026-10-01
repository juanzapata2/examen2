import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conexion = sqlite3.connect("estudiantes.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    edad INTEGER,
    curso TEXT,
    nota REAL
)
""")

conexion.commit()

ventana = tk.Tk()
ventana.title("Sistema de Registro de Estudiantes")
ventana.geometry("1100x620")
ventana.configure(bg="#f4f8fc")
ventana.resizable(False, False)


titulo = tk.Label(
    ventana,
    text="Sistema de Registro de Estudiantes",
    font=("Arial", 24, "bold"),
    bg="#1769aa",
    fg="white",
    pady=12
)
titulo.pack(fill="x")


principal = tk.Frame(
    ventana,
    bg="#f4f8fc"
)
principal.pack(
    fill="both",
    expand=True,
    padx=18,
    pady=12
)


izquierda = tk.Frame(
    principal,
    bg="white",
    relief="solid",
    borderwidth=1
)
izquierda.pack(
    side="left",
    fill="y",
    padx=(0, 12)
)


datos_titulo = tk.Label(
    izquierda,
    text="Datos del estudiante",
    font=("Arial", 15, "bold"),
    bg="#dceeff",
    fg="#174a7c",
    pady=8
)
datos_titulo.pack(fill="x")


tk.Label(
    izquierda,
    text="Nombre:",
    font=("Arial", 11),
    bg="white"
).pack(anchor="w", padx=14, pady=(12, 3))

entrada_nombre = tk.Entry(
    izquierda,
    font=("Arial", 11),
    width=27
)
entrada_nombre.pack(padx=14)


tk.Label(
    izquierda,
    text="Edad:",
    font=("Arial", 11),
    bg="white"
).pack(anchor="w", padx=14, pady=(9, 3))

entrada_edad = tk.Entry(
    izquierda,
    font=("Arial", 11),
    width=27
)
entrada_edad.pack(padx=14)


tk.Label(
    izquierda,
    text="Curso:",
    font=("Arial", 11),
    bg="white"
).pack(anchor="w", padx=14, pady=(9, 3))

curso = ttk.Combobox(
    izquierda,
    values=[
        "Matemáticas",
        "Lenguaje",
        "Ciencias",
        "Inglés",
        "Historia",
        "Computación"
    ],
    font=("Arial", 11),
    width=25,
    state="readonly"
)
curso.pack(padx=14)


tk.Label(
    izquierda,
    text="Nota:",
    font=("Arial", 11),
    bg="white"
).pack(anchor="w", padx=14, pady=(9, 3))

entrada_nota = tk.Entry(
    izquierda,
    font=("Arial", 11),
    width=27
)
entrada_nota.pack(padx=14)


def guardar():
    nombre = entrada_nombre.get()
    edad = entrada_edad.get()
    curso_seleccionado = curso.get()
    nota = entrada_nota.get()

    if nombre == "" or edad == "" or curso_seleccionado == "" or nota == "":
        messagebox.showwarning(
            "Aviso",
            "Completa todos los campos",
            parent=ventana
        )
        return

    cursor.execute(
        "INSERT INTO estudiantes (nombre, edad, curso, nota) VALUES (?, ?, ?, ?)",
        (nombre, edad, curso_seleccionado, nota)
    )

    conexion.commit()

    messagebox.showinfo(
        "Información",
        "Estudiante guardado correctamente.",
        parent=ventana
    )

    limpiar()
    actualizar_tabla()


def actualizar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)

    cursor.execute("SELECT * FROM estudiantes")
    estudiantes = cursor.fetchall()

    for estudiante in estudiantes:
        tabla.insert(
            "",
            "end",
            values=estudiante
        )


def buscar():
    texto = entrada_buscar.get()

    if texto == "":
        messagebox.showwarning(
            "Aviso",
            "Escribe un nombre para buscar.",
            parent=ventana
        )
        return

    for fila in tabla.get_children():
        tabla.delete(fila)

    cursor.execute(
        "SELECT * FROM estudiantes WHERE nombre LIKE ?",
        ("%" + texto + "%",)
    )

    estudiantes = cursor.fetchall()

    for estudiante in estudiantes:
        tabla.insert(
            "",
            "end",
            values=estudiante
        )

    if len(estudiantes) > 0:

        primera_fila = tabla.get_children()[0]

        tabla.selection_set(primera_fila)
        tabla.focus(primera_fila)
        tabla.see(primera_fila)

        messagebox.showinfo(
            "Información",
            "Estudiante encontrado correctamente.",
            parent=ventana
        )

    else:

        messagebox.showinfo(
            "Información",
            "Estudiante no encontrado.",
            parent=ventana
        )


def eliminar():
    seleccionado = tabla.selection()

    if seleccionado == ():
        messagebox.showwarning(
            "Aviso",
            "Selecciona un estudiante",
            parent=ventana
        )
        return

    fila = tabla.item(seleccionado)
    id_estudiante = fila["values"][0]

    cursor.execute(
        "DELETE FROM estudiantes WHERE id = ?",
        (id_estudiante,)
    )

    conexion.commit()

    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        cursor.execute(
            "DELETE FROM sqlite_sequence WHERE name='estudiantes'"
        )
        conexion.commit()

    messagebox.showinfo(
        "Información",
        "Estudiante eliminado correctamente.",
        parent=ventana
    )

    actualizar_tabla()


def limpiar():
    entrada_nombre.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    curso.set("")
    entrada_nota.delete(0, tk.END)


boton_guardar = tk.Button(
    izquierda,
    text="💾  Guardar",
    font=("Arial", 11, "bold"),
    bg="#20a66a",
    fg="white",
    width=24,
    pady=5,
    command=guardar
)
boton_guardar.pack(pady=(14, 5))


boton_eliminar = tk.Button(
    izquierda,
    text="▣  Eliminar",
    font=("Arial", 11, "bold"),
    bg="#ed3b3b",
    fg="white",
    width=24,
    pady=5,
    command=eliminar
)
boton_eliminar.pack(pady=5)


boton_limpiar = tk.Button(
    izquierda,
    text="↻  Limpiar",
    font=("Arial", 11, "bold"),
    bg="#687583",
    fg="white",
    width=24,
    pady=5,
    command=limpiar
)
boton_limpiar.pack(pady=5)


derecha = tk.Frame(
    principal,
    bg="white",
    relief="solid",
    borderwidth=1
)
derecha.pack(
    side="left",
    fill="both",
    expand=True
)


lista_titulo = tk.Label(
    derecha,
    text="Lista de estudiantes",
    font=("Arial", 15, "bold"),
    bg="#dceeff",
    fg="#174a7c",
    pady=8
)
lista_titulo.pack(fill="x")


marco_tabla = tk.Frame(
    derecha,
    bg="white",
    relief="solid",
    borderwidth=1
)
marco_tabla.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


estilo = ttk.Style()

estilo.map(
    "Treeview",
    background=[
        ("selected", "#1976d2")
    ],
    foreground=[
        ("selected", "white")
    ]
)


tabla = ttk.Treeview(
    marco_tabla,
    columns=("ID", "Nombre", "Edad", "Curso", "Nota"),
    show="headings",
    height=9
)

tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Edad", text="Edad")
tabla.heading("Curso", text="Curso")
tabla.heading("Nota", text="Nota")

tabla.column("ID", width=45)
tabla.column("Nombre", width=175)
tabla.column("Edad", width=60)
tabla.column("Curso", width=135)
tabla.column("Nota", width=65)

tabla.pack(
    side="left",
    fill="both",
    expand=True
)


barra = ttk.Scrollbar(
    marco_tabla,
    orient="vertical",
    command=tabla.yview
)

barra.pack(
    side="right",
    fill="y"
)

tabla.configure(
    yscrollcommand=barra.set
)


buscar_marco = tk.Frame(
    derecha,
    bg="#f0efff",
    relief="solid",
    borderwidth=1
)
buscar_marco.pack(
    fill="x",
    padx=10,
    pady=(0, 10)
)


tk.Label(
    buscar_marco,
    text="Buscar estudiante",
    font=("Arial", 13, "bold"),
    bg="#f0efff",
    fg="#174a7c"
).pack(
    anchor="w",
    padx=12,
    pady=6
)


entrada_buscar = tk.Entry(
    buscar_marco,
    font=("Arial", 11),
    width=35
)

entrada_buscar.pack(
    side="left",
    padx=(12, 5),
    pady=(0, 9)
)


boton_buscar = tk.Button(
    buscar_marco,
    text="⌕  Buscar",
    font=("Arial", 11, "bold"),
    bg="#2684e8",
    fg="white",
    width=11,
    command=buscar
)

boton_buscar.pack(
    side="left",
    pady=(0, 9)
)


pie = tk.Label(
    ventana,
    text="Sistema desarrollado en Python",
    font=("Arial", 10),
    bg="#1769aa",
    fg="white",
    pady=6
)

pie.pack(fill="x")


actualizar_tabla()

ventana.mainloop()