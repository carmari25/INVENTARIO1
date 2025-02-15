from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

INVENTARIO_FILE = "inventario.json"
    


def almacen():
        productos_almacen()

def productos_almacen():
            

            almacenes = tk.Tk()
            almacenes.title("Inventario - Cosmos IA")
            almacenes.geometry("850x450")
            almacenes.config(bg="#d5f5e3")
            almacenes.iconbitmap("satur.ico.ico")

            def agregar_producto():
            #Añade un producto al inventario y lo muestra en la tabla."""
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

            # Etiquetas y entradas para agregar productos
            tk.Label(almacenes, text="Nombre:", bg="#eafaf1").place(x=20 , y=20)
            entry_nombre = tk.Entry(almacenes)
            entry_nombre.place(x=80 , y=20)

            tk.Label(almacenes, text="Código:",bg="#eafaf1").place(x=20 , y=40)
            entry_codigo = tk.Entry(almacenes)
            entry_codigo.place(x=80 , y=40)

            tk.Label(almacenes, text="Cantidad:", bg="#eafaf1").place(x=20 , y=60)
            entry_cantidad = tk.Entry(almacenes)
            entry_cantidad.place(x=80 , y=60)

            tk.Label(almacenes, text="Unidad:", bg="#eafaf1").place(x=350 , y=10)
            combo_unidades = ttk.Combobox(almacenes, values=["Kg", "Lt", "Cantidad"], state="readonly")
            combo_unidades.place(x=350 , y=30)

            # Botón para agregar producto
            btn_agregar = tk.Button(almacenes, text="Agregar Producto", command=agregar_producto)
            btn_agregar.place(x=350 , y=55)

            # Tabla para mostrar productos
            columnas = ("Nombre", "Código", "Cantidad", "Unidad")
            tabla = ttk.Treeview(almacenes, columns=columnas, show="headings")
            for col in columnas:
                tabla.heading(col, text=col)
            tabla.place(x=20 , y=100)

            # Cargar productos guardados en la tabla
            cargar_productos_en_tabla()

            # Sección para eliminar productos
            tk.Label(almacenes, text="Código a eliminar:", bg="#eafaf1").place(x=20, y=350)
            entry_eliminar_codigo = tk.Entry(almacenes)
            entry_eliminar_codigo.place(x=130, y=350)

            btn_eliminar = tk.Button(almacenes, text="Eliminar Producto", command=eliminar_producto)
            btn_eliminar.place(x=280, y=345)

            def cargar_productos_en_tabla():
            #Carga los productos guardados en la tabla al iniciar."""
                inventario = cargar_inventario()
                for producto in inventario:
                    tabla.insert("", "end", values=(producto["nombre"], producto["codigo"], producto["cantidad"], producto["unidad"]))

        
            
            def eliminar_producto():
            #Elimina un producto del inventario según su código.
                codigo = entry_eliminar_codigo.get()
            
                if not codigo:
                    messagebox.showwarning("Error", "Debe ingresar un código para eliminar un producto.")
                    return
            
                inventario = cargar_inventario()
                
                # Verificar si el producto existe
                if not any(prod["codigo"] == codigo for prod in inventario):
                    messagebox.showwarning("Error", f"No se encontró un producto con el código {codigo}.")
                    return
                
                # Crear un nuevo inventario sin el producto eliminado
                nuevo_inventario = [prod for prod in inventario if prod["codigo"] != codigo]
                
                # Guardar los cambios en el JSON
                guardar_inventario(nuevo_inventario)
                
                # Eliminar de la tabla
                for item in tabla.get_children():
                    if tabla.item(item, "values")[1] == codigo:  # Índice 1 es el código en la tabla
                        tabla.delete(item)
                
                    entry_eliminar_codigo.delete(0, tk.END)  # Limpiar el campo de entrada
                    messagebox.showinfo("Éxito", f"Producto con código {codigo} eliminado correctamente.")

            # Ejecutar ventana
            almacenes.mainloop()

def ventana_inventario():


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

    def cargar_inventario():
        if os.path.exists(INVENTARIO_FILE):
            with open(INVENTARIO_FILE, "r") as f:
                return json.load(f)
        return []

    def guardar_inventario(inventario):
                    with open(INVENTARIO_FILE, "w") as f:
                        json.dump(inventario, f, indent=4)

    def actualizar_stock(codigo, cantidad_vendida):
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
    
        

    def actualizar_tabla():
            """Actualiza la tabla con los productos actuales del inventario."""
            for row in tabla.get_children():
                tabla.delete(row)
            inventario = cargar_inventario()
            for producto in inventario:
                tabla.insert("", "end", values=(producto["nombre"], producto["codigo"], producto["cantidad"], producto["unidad"]))


        # Crear ventana principal
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
        almacenes.add_command(label="inventario" , command=almacen)

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
ventana_inventario()