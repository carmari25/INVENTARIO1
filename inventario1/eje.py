from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Archivo de inventario
INVENTARIO_FILE = "inventario.json"


def cargar_inventario():
    """Carga los productos desde el archivo JSON."""
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, "r") as f:
            return json.load(f)
    return []


def guardar_inventario(inventario):
    """Guarda el inventario en el archivo JSON."""
    with open(INVENTARIO_FILE, "w") as f:
        json.dump(inventario, f, indent=4)


def actualizar_stock(codigo, cantidad_vendida):
    """Actualiza la cantidad de un producto tras una venta."""
    inventario = cargar_inventario()
    for producto in inventario:
        if producto["codigo"] == codigo:
            if producto["cantidad"] >= cantidad_vendida:
                producto["cantidad"] -= cantidad_vendida
                guardar_inventario(inventario)
                return True
            else:
                return False
    return None

def agregar_a_lista_compras(entry_nombre, entry_codigo, entry_cantidad, combo_unidades, tabla):
    """Añade productos a la lista de compras sin afectar el inventario general."""
    nombre = entry_nombre.get()
    codigo = entry_codigo.get()
    cantidad = entry_cantidad.get()
    unidad = combo_unidades.get()

    if not codigo or not nombre or not  cantidad :
        messagebox.showwarning("Error", "Se requiere mas informacion")
        return

    try:
        cantidad = int(cantidad)
    except ValueError:
        messagebox.showwarning("Error", "La cantidad debe ser un número")
        return

    # Verificar si el producto ya está en la lista de compras
    for item in tabla.get_children():
        valores = tabla.item(item, "values")
        if valores[1] == codigo:
            messagebox.showwarning("Error", f"El producto con código {codigo} ya está en la lista de compras.")
            return

    # Insertar en la tabla de lista de compras
    tabla.insert("", "end", values=(nombre, codigo, cantidad, unidad))

    # Limpiar entradas
    entry_nombre.delete(0, tk.END)
    entry_codigo.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    combo_unidades.set("")




def productos_almacen():
    """Ventana del inventario."""
    almacenes = tk.Tk()
    almacenes.title("Inventario - Cosmos IA")
    almacenes.geometry("850x450")
    almacenes.config(bg="#d5f5e3")
    almacenes.iconbitmap("satur.ico.ico")

    def agregar_producto():
        """Añade un producto al inventario."""
        nombre = entry_nombre.get()
        codigo = entry_codigo.get()
        cantidad = entry_cantidad.get()
        unidad = combo_unidades.get()

        if not nombre or not codigo or not cantidad or not unidad:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showwarning("Error", "La cantidad debe ser un número")
            return

        inventario = cargar_inventario()

        # Verificar si el producto ya existe
        for producto in inventario:
            if producto["codigo"] == codigo:
                messagebox.showwarning("Error", f"El producto con código {codigo} ya existe.")
                return

        # Agregar el producto
        nuevo_producto = {"nombre": nombre, "codigo": codigo, "cantidad": cantidad, "unidad": unidad}
        inventario.append(nuevo_producto)
        guardar_inventario(inventario)

        # Insertar en la tabla
        tabla.insert("", "end", values=(nombre, codigo, cantidad, unidad))

        # Limpiar entradas
        entry_nombre.delete(0, tk.END)
        entry_codigo.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        combo_unidades.set("")

    def cargar_productos_en_tabla():
        """Carga los productos guardados en la taabla al iniciar."""
        inventario = cargar_inventario()
        for producto in inventario:
            tabla.insert("", "end", values=(producto["nombre"], producto["codigo"], producto["cantidad"], producto["unidad"]))

    def eliminar_producto():
        """Elimina un producto del inventario según su código."""
        codigo = entry_eliminar_codigo.get()

        if not codigo:
            messagebox.showwarning("Error", "Debe ingresar un código para eliminar un producto.")
            return

        inventario = cargar_inventario()

        if not any(prod["codigo"] == codigo for prod in inventario):
            messagebox.showwarning("Error", f"No se encontró un producto con el código {codigo}.")
            return

        nuevo_inventario = [prod for prod in inventario if prod["codigo"] != codigo]
        guardar_inventario(nuevo_inventario)

        for item in tabla.get_children():
            if tabla.item(item, "values")[1] == codigo:
                tabla.delete(item)

        entry_eliminar_codigo.delete(0, tk.END)
        messagebox.showinfo("Éxito", f"Producto con código {codigo} eliminado correctamente.")

    # Interfaz gráfica
    tk.Label(almacenes, text="Nombre:", bg="#eafaf1").place(x=20, y=20)
    entry_nombre = tk.Entry(almacenes)
    entry_nombre.place(x=80, y=20)

    tk.Label(almacenes, text="Código:", bg="#eafaf1").place(x=20, y=40)
    entry_codigo = tk.Entry(almacenes)
    entry_codigo.place(x=80, y=40)

    tk.Label(almacenes, text="Cantidad:", bg="#eafaf1").place(x=20, y=60)
    entry_cantidad = tk.Entry(almacenes)
    entry_cantidad.place(x=80, y=60)

    tk.Label(almacenes, text="Unidad:", bg="#eafaf1").place(x=350, y=10)
    combo_unidades = ttk.Combobox(almacenes, values=["Kg", "Lt", "Cantidad"], state="readonly")
    combo_unidades.place(x=350, y=30)

    btn_agregar = tk.Button(almacenes, text="Agregar Producto", command=agregar_producto)
    btn_agregar.place(x=350, y=55)

    # Tabla
    columnas = ("Nombre", "Código", "Cantidad", "Unidad")
    tabla = ttk.Treeview(almacenes, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
    tabla.place(x=20, y=100)

    cargar_productos_en_tabla()

    tk.Label(almacenes, text="Código a eliminar:", bg="#eafaf1").place(x=20, y=350)
    entry_eliminar_codigo = tk.Entry(almacenes)
    entry_eliminar_codigo.place(x=130, y=350)

    btn_eliminar = tk.Button(almacenes, text="Eliminar Producto", command=eliminar_producto)
    btn_eliminar.place(x=280, y=345)

    almacenes.mainloop()


def vender_productos(tabla):
    """Retira del inventario los productos de la lista de compras."""
    inventario = cargar_inventario()
    productos_vendidos = []

    for item in tabla.get_children():
        valores = tabla.item(item, "values")
        nombre, codigo, cantidad, unidad = valores
        cantidad = int(cantidad)

        for producto in inventario:
            if producto["codigo"] == codigo:
                if producto["cantidad"] >= cantidad:
                    producto["cantidad"] -= cantidad
                    productos_vendidos.append(codigo)
                else:
                    messagebox.showwarning("Error", f"No hay suficiente stock para {nombre}.")
                    return

    # Filtrar productos agotados
    inventario = [prod for prod in inventario if prod["cantidad"] > 0]

    guardar_inventario(inventario)

    # Eliminar productos vendidos de la lista de compras
    for item in tabla.get_children():
         valores = tabla.item(item, "values")
    if valores[1] in productos_vendidos:
            tabla.delete(item)

    messagebox.showinfo("Venta realizada", "Los productos han sido vendidos y actualizados en el inventario.")

def agregar_producto(entry_nombre, entry_codigo, entry_cantidad, combo_unidades, tabla):
    nombre = entry_nombre.get()
    codigo = entry_codigo.get()
    cantidad = entry_cantidad.get()
    unidad = combo_unidades.get()  # Asegura que esto se obtiene correctamente

    if not codigo or not cantidad or not unidad:
        messagebox.showwarning("Error", "Se requiere mas informacion")
        return

    try:
        cantidad = int(cantidad)
    except ValueError:
        messagebox.showwarning("Error", "La cantidad debe ser un número")
        return

    inventario = cargar_inventario()

    # Verificar si el producto ya existe
    for producto in inventario:
        if producto["codigo"] == codigo:
            messagebox.showwarning("Error", f"El producto con código {codigo} ya existe.")
            return

    # Agregar el producto
    nuevo_producto = {"nombre": nombre, "codigo": codigo, "cantidad": cantidad, "unidad": unidad}
    inventario.append(nuevo_producto)
    guardar_inventario(inventario)

    # Insertar en la tabla
    tabla.insert("", "end", values=(nombre, codigo, cantidad, unidad))

    # Limpiar entradas
    entry_nombre.delete(0, tk.END)
    entry_codigo.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    combo_unidades.set("")


def ventana_inventario():
    """Ventana principal de inventario."""
    raiz = tk.Tk()
    raiz.iconbitmap("satur.ico.ico")
    raiz.geometry("1000x500")
    raiz.title("COSMOS IA")
    raiz.config(bg="#d5f5e3")

    menu=Menu(raiz)
    raiz.config(menu=menu)
        #menu

    archivo =Menu(menu, tearoff=0)
    archivo.add_command(label="Nuevo Archivo")
    archivo.add_command(label="Nueva Ventana")
    archivo.add_command(label="Crear Archivo TXT")
    archivo.add_separator()
    archivo.add_command(label="Cerrar sesion")


    almacenes =Menu(menu, tearoff=0)
    almacenes.add_command(label="inventario" , command=productos_almacen)

    ventas =Menu(menu, tearoff=0)
    ventas.add_command(label="Hoy")
    ventas.add_command(label="ayer")
    ventas.add_command(label="Esta semana")
    ventas.add_command(label="Este mes")

    ayuda=Menu(menu, tearoff=0)
    ayuda.add_command(label="Contacto")

    menu.add_cascade(label ="Archivo", menu_=archivo)
    menu.add_cascade(label="Almacen", menu_=almacenes)
    menu.add_cascade(label="Ventas", menu_=ventas)
    menu.add_cascade(label="Ayuda", menu_=ayuda)

        # Crear marco para los controles
    miFrame = tk.Frame(raiz, bg="#eafaf1", width=500, height=600, bd=20, relief="ridge", cursor="arrow")
    miFrame.pack(fill="x", expand=True)

    tk.Label(miFrame, text="Bienvenido", fg="#006064", font=("Josefin Sans", 15), bg="#eafaf1").place(x=10, y=10) 

    tk.Label(miFrame, text="Producto:", fg="#006064", font=("Josefin Sans", 10), bg="#eafaf1").place(x=10, y=40)
    entry_nombre = tk.Entry(miFrame)
    entry_nombre.place(x=80, y=40)

    tk.Label(miFrame, text="Código:", fg="#006064", font=("Josefin Sans", 10), bg="#eafaf1").place(x=10, y=70)
    entry_codigo = tk.Entry(miFrame)
    entry_codigo.place(x=80, y=70)

    tk.Label(miFrame, text="Cantidad:", fg="#006064", font=("Josefin Sans", 10), bg="#eafaf1").place(x=10, y=100)
    entry_cantidad = tk.Entry(miFrame)
    entry_cantidad.place(x=80, y=100)

    combobox = ttk.Combobox(miFrame, state="readonly", width=15)
    combobox.place(x=400, y=20)

    def actualizar_interfaz():
            """Actualiza el Combobox y muestra el Spinbox si es necesario."""
            seleccion = opcion.get()
            combobox.set("")

            if seleccion == 1:  # Cantidad
                combobox["values"] = ["N"]
                  # Mostrar Spinbox
                
            elif seleccion == 2:  # Kg
                combobox["values"] = ["Gramo", "Kilogramo", "Miligramo"]
                  # Mostrar Spinbox

            elif seleccion == 3:  # Lt
                combobox["values"] = ["Litro", "Galón", "Mililitro"]
                  # Mostrar Spinbox

    def eliminar_producto():
        """Elimina un producto del inventario según su código."""
        codigo = entry_eliminar_codigo.get()

        if not codigo:
            messagebox.showwarning("Error", "Debe ingresar un código para eliminar un producto.")
            return

        inventario = cargar_inventario()

        if not any(prod["codigo"] == codigo for prod in inventario):
            messagebox.showwarning("Error", f"No se encontró un producto con el código {codigo}.")
            return

        nuevo_inventario = [prod for prod in inventario if prod["codigo"] != codigo]
        guardar_inventario(nuevo_inventario)

        for item in tabla.get_children():
            if tabla.item(item, "values")[1] == codigo:
                tabla.delete(item)

        entry_eliminar_codigo.delete(0, tk.END)
        messagebox.showinfo("Éxito", f"Producto con código {codigo} eliminado correctamente.")
    # Tabla para mostrar productos agregados
    columnas = ("Nombre", "Código", "Cantidad", "Unidad")
    tabla = ttk.Treeview(raiz, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
    tabla.place(x=30, y=150)

    # Botón para agregar productos
    btn_agregar = tk.Button(
    miFrame, 
    text="Agregar Producto", 
    command=lambda: agregar_a_lista_compras(entry_nombre, entry_codigo, entry_cantidad, combobox, tabla)
)
    btn_agregar.place(x=400, y=90)

    
    tk.Label(miFrame, text="En qué unidades:", bg="#eafaf1").place(x=230, y=10)
    opcion = tk.IntVar()

    tk.Radiobutton(miFrame, text="Cantidad", bg="#eafaf1", variable=opcion, value=1, command=actualizar_interfaz).place(x=250, y=30)
    tk.Radiobutton(miFrame, text="Kg", bg="#eafaf1", variable=opcion, value=2,command=actualizar_interfaz).place(x=250, y=50)
    tk.Radiobutton(miFrame, text="Lt", bg="#eafaf1", variable=opcion, value=3,command=actualizar_interfaz).place(x=250, y=70)


    tk.Label(almacenes, text="Código a eliminar:", bg="#eafaf1").place(x=20, y=350)
    entry_eliminar_codigo = tk.Entry(almacenes)
    entry_eliminar_codigo.place(x=130, y=350)

    btn_eliminar = tk.Button(almacenes, text="Eliminar Producto", command=eliminar_producto)
    btn_eliminar.place(x=600, y=400)

    btn_vender = tk.Button(miFrame, text="Vender", command=lambda: vender_productos(tabla))
    btn_vender.place(x=700, y=400)


        # Cargar productos guardados en la tabla
    raiz.mainloop()

ventana_inventario()
