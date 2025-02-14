import tkinter as tk
from tkinter import ttk, messagebox
from productos import actualizar_stock, cargar_inventario



def actualizar_interfaz():
    """Actualiza el Combobox y muestra el Spinbox si es necesario."""
    seleccion = opcion.get()
    combobox.set("")

    if seleccion == 1:  # Cantidad
        combobox["values"] = []
        spinbox.place(x=400, y=50)  # Mostrar Spinbox
        
    elif seleccion == 2:  # Kg
        combobox["values"] = ["Gramo", "Kilogramo", "Miligramo"]
        spinbox.place(x=400, y=50)  # Mostrar Spinbox

    elif seleccion == 3:  # Lt
        combobox["values"] = ["Litro", "Galón", "Mililitro"]
        spinbox.place(x=400, y=50)  # Mostrar Spinbox

def cargar_productos_en_tabla():
    """Carga los productos almacenados en la tabla al iniciar."""
    for producto in inventario:
        tabla.insert("", "end", values=(producto["nombre"], producto["codigo"], producto["cantidad"], producto["unidad"]))

def agregar_producto():
    """Agrega un producto a la lista y lo muestra en la tabla."""
    nombre = codigo1.get().strip()
    codigo = codigo2.get().strip()
    cantidad = spinbox.get().strip()
    unidad = combobox.get().strip()
    cantidad_vendida = spinbox.get().strip()

    if not codigo or not cantidad_vendida:
        messagebox.showwarning("Error", "Ingrese un código y cantidad")
        return
    
    try:
        cantidad_vendida = int(cantidad_vendida)
    except ValueError:
        messagebox.showwarning("Error", "La cantidad debe ser un número")
        return

    resultado = actualizar_stock(codigo, cantidad_vendida)

    if resultado is True:
        messagebox.showinfo("Éxito", f"Se vendieron {cantidad_vendida} unidades")
        actualizar_tabla()
    elif resultado is False:
        messagebox.showwarning("Error", "No hay suficiente stock")
    else:
        messagebox.showwarning("Error", "Producto no encontrado")

    inventario_actual = cargar_inventario()
    producto_encontrado = next((p for p in inventario_actual if p["codigo"] == codigo), None)

    if producto_encontrado is None:
        messagebox.showwarning("Error", "El producto no está en el inventario")
        return
    
    if cantidad > producto_encontrado["cantidad"]:
        messagebox.showwarning("Error", "No hay suficiente stock")
        return

    # Agregar el producto a la lista
    nuevo_producto = {"nombre": nombre, "codigo": codigo, "cantidad": cantidad, "unidad": unidad}
    inventario.append(nuevo_producto)

    # Insertar en la tabla
    tabla.insert("", "end", values=(nombre, codigo, cantidad, unidad))

    # Limpiar entradas
    codigo1.delete(0, tk.END)
    codigo2.delete(0, tk.END)
    spinbox.delete(0, tk.END)

    messagebox.showinfo("Éxito", "Producto agregado correctamente")

# Lista donde se almacenarán los productos ingresados
inventario = []


    

def actualizar_tabla():
    """Actualiza la tabla con los productos actuales del inventario."""
    for row in tabla.get_children():
        tabla.delete(row)
    inventario = cargar_inventario()
    for producto in inventario:
        tabla.insert("", "end", values=(producto["nombre"], producto["codigo"], producto["cantidad"], producto["unidad"]))

# Configuración de la ventana

# Crear ventana principal
raiz = tk.Tk()
raiz.iconbitmap("satur.ico.ico")
raiz.geometry("1000x500")
raiz.title("COSMOS IA")
raiz.config(bg="#d5f5e3")

# Crear marco para los controles
miFrame = tk.Frame(raiz, bg="#eafaf1", width=500, height=600, bd=20, relief="ridge", cursor="arrow")
miFrame.pack(fill="x", expand=True)

tk.Label(miFrame, text="Bienvenido", fg="#006064", font=("Josefin Sans", 15), bg="#eafaf1").place(x=10, y=10)

tk.Label(miFrame, text="Producto:", fg="#006064", font=("Josefin Sans", 10), bg="#eafaf1").place(x=10, y=40)
codigo1 = tk.Entry(miFrame)
codigo1.place(x=80, y=40)

tk.Label(miFrame, text="Código:", fg="#006064", font=("Josefin Sans", 10), bg="#eafaf1").place(x=10, y=70)
codigo2 = tk.Entry(miFrame)
codigo2.place(x=80, y=70)

tk.Label(miFrame, text="En qué unidades:", bg="#eafaf1").place(x=230, y=10)
opcion = tk.IntVar()

tk.Radiobutton(miFrame, text="Cantidad", bg="#eafaf1", variable=opcion, value=1, command=actualizar_interfaz).place(x=250, y=30)
tk.Radiobutton(miFrame, text="Kg", bg="#eafaf1", variable=opcion, value=2, command=actualizar_interfaz).place(x=250, y=50)
tk.Radiobutton(miFrame, text="Lt", bg="#eafaf1", variable=opcion, value=3, command=actualizar_interfaz).place(x=250, y=70)

combobox = ttk.Combobox(miFrame, state="readonly", width=15)
combobox.place(x=400, y=20)

spinbox = tk.Spinbox(miFrame, from_=0, to=100, width=5)
spinbox.place(x=400, y=50)

# Botón para agregar productos
btn_agregar = tk.Button(miFrame, text="Agregar Producto", command=agregar_producto)
btn_agregar.place(x=400, y=90)

# Tabla para mostrar productos agregados
columnas = ("Nombre", "Código", "Cantidad", "Unidad")
tabla = ttk.Treeview(raiz, columns=columnas, show="headings")
for col in columnas:
    tabla.heading(col, text=col)
tabla.place(x=30, y=150)




# Cargar productos guardados en la tabla
cargar_productos_en_tabla()

raiz.mainloop()
