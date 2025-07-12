from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import inicio2
import sys

login_exitoso = inicio2.ventana_inicio()  # Ejecuta la ventana de inicio de sesión

# Si el login falla o se cierra la ventana, terminamos el programa
if not login_exitoso:
    sys.exit()

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

def inicializar_inventario():
    if not os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, "w") as f:
            json.dump([], f)

# Llamar al inicio del programa
inicializar_inventario()



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
    almacenes.geometry("1050x600")
    almacenes.config(bg="#d5f5e3")
    
    # --- Frame para campos de entrada ---
    frame_entradas = tk.Frame(almacenes, bg="#eafaf1", padx=10, pady=10)
    frame_entradas.place(x=0, y=0, width=1050, height=120)

    # Widgets de entrada
    tk.Label(frame_entradas, text="Nombre:").grid(row=0, column=0, sticky="w")
    entry_nombre = tk.Entry(frame_entradas)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame_entradas, text="Código:").grid(row=1, column=0, sticky="w")
    entry_codigo = tk.Entry(frame_entradas)
    entry_codigo.grid(row=1, column=1)

    tk.Label(frame_entradas, text="Cantidad:").grid(row=2, column=0, sticky="w")
    entry_cantidad = tk.Entry(frame_entradas)
    entry_cantidad.grid(row=2, column=1)

    tk.Label(frame_entradas, text="Unidad:").grid(row=0, column=2, padx=(20,0))
    combo_unidades = ttk.Combobox(frame_entradas, values=["Kg", "Lt", "Cantidad"], state="readonly")
    combo_unidades.grid(row=0, column=3)

    tk.Label(frame_entradas, text="Precio:").grid(row=1, column=2, padx=(20,0))
    entry_precio = tk.Entry(frame_entradas)
    entry_precio.grid(row=1, column=3)

    # --- Frame para tabla ---
    frame_tabla = tk.Frame(almacenes)
    frame_tabla.place(x=10, y=130, width=1030, height=400)

    columnas = ("Nombre", "Código", "Cantidad", "Unidad", "Precio")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
    
    # Configuración de columnas
    tabla.column("Nombre", width=300, anchor="w")
    tabla.column("Código", width=100, anchor="center")
    tabla.column("Cantidad", width=100, anchor="center")
    tabla.column("Unidad", width=100, anchor="center")
    tabla.column("Precio", width=100, anchor="e")
    
    for col in columnas:
        tabla.heading(col, text=col)
    
    # Scrollbar
    scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    scroll.pack(side="right", fill="y")
    tabla.configure(yscrollcommand=scroll.set)
    tabla.pack(fill="both", expand=True)

    # --- Sección para eliminar productos ---
    frame_eliminar = tk.Frame(almacenes, bg="#d5f5e3")
    frame_eliminar.place(x=10, y=540, width=1030, height=50)

    tk.Label(frame_eliminar, text="Código a eliminar:").grid(row=0, column=0)
    entry_eliminar_codigo = tk.Entry(frame_eliminar)
    entry_eliminar_codigo.grid(row=0, column=1, padx=5)

    # --- Funciones ---
    

    def agregar_producto():
        """Agrega un nuevo producto al inventario."""
        nombre = entry_nombre.get().strip()
        codigo = entry_codigo.get().strip()
        cantidad = entry_cantidad.get().strip()
        unidad = combo_unidades.get().strip()
        precio = entry_precio.get().strip()

        # Validación
        if not all([nombre, codigo, cantidad, unidad, precio]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showwarning("Error", "Cantidad y precio deben ser números válidos")
            return

        inventario = cargar_inventario()
        
        # Verificar código duplicado
        if any(p["codigo"] == codigo for p in inventario):
            messagebox.showwarning("Error", f"El código {codigo} ya existe")
            return

        # Agregar producto
        nuevo_producto = {
            "nombre": nombre,
            "codigo": codigo,
            "cantidad": cantidad,
            "unidad": unidad,
            "precio": precio
        }
        inventario.append(nuevo_producto)
        guardar_inventario(inventario)
        
        # Actualizar tabla
        tabla.insert("", "end", values=(nombre, codigo, cantidad, unidad, precio))
    def cargar_productos_en_tabla():
        
        
        # Limpiar campos
        entry_nombre.delete(0, tk.END)
        entry_codigo.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        combo_unidades.set("")
        entry_precio.delete(0, tk.END)

    def cargar_productos_en_tabla():
        """Carga los productos del JSON en la tabla."""
        tabla.delete(*tabla.get_children())
        inventario = cargar_inventario()
        for producto in inventario:
            tabla.insert("", "end", values=(
                producto["nombre"],
                producto["codigo"],
                producto["cantidad"],
                producto["unidad"],
                producto["precio"]
            ))
    

    def eliminar_producto():
        """Elimina un producto del inventario."""
        codigo = entry_eliminar_codigo.get().strip()

        if not codigo:
            messagebox.showwarning("Error", "Ingrese un código para eliminar")
            return

        inventario = cargar_inventario()
        
        if not any(p["codigo"] == codigo for p in inventario):
            messagebox.showwarning("Error", f"No existe un producto con código {codigo}")
            return

        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", f"¿Eliminar producto {codigo}?"):
            return

        nuevo_inventario = [p for p in inventario if p["codigo"] != codigo]
        guardar_inventario(nuevo_inventario)
        
        # Actualizar tabla
        for item in tabla.get_children():
            if tabla.item(item, "values")[1] == codigo:
                tabla.delete(item)
        
        entry_eliminar_codigo.delete(0, tk.END)
        messagebox.showinfo("Éxito", "Producto eliminado")

    # --- Botones ---
    btn_agregar = tk.Button(
        frame_entradas, 
        text="Agregar Producto", 
        command=agregar_producto
    )
    btn_agregar.grid(row=2, column=3, pady=5)

    btn_eliminar = tk.Button(
        frame_eliminar,
        text="Eliminar Producto",
        command=eliminar_producto
    )
    btn_eliminar.grid(row=0, column=2, padx=10)

    # --- Carga inicial ---
    cargar_productos_en_tabla()
    almacenes.mainloop()


def vender_productos(tabla):
        inventario = cargar_inventario()
        productos_vendidos = []
        productos_no_existentes = []
        productos_sin_stock = []

        # Primera pasada: Verificar todo antes de hacer cambios
        for item in tabla.get_children():
            valores = tabla.item(item, "values")
            nombre, codigo, cantidad, unidad = valores
            cantidad = int(cantidad)
            
            # Buscar producto en inventario
            producto_en_inventario = None
            for producto in inventario:
                if producto["codigo"] == codigo:
                    producto_en_inventario = producto
                    break
            
            if not producto_en_inventario:
                productos_no_existentes.append(nombre)
                continue
                
            if producto_en_inventario["cantidad"] < cantidad:
                productos_sin_stock.append(nombre)
                continue

        # Mostrar errores si hay productos problemáticos
        mensajes_error = []
        if productos_no_existentes:
            mensajes_error.append(f"Productos no existentes: {', '.join(productos_no_existentes)}")
        if productos_sin_stock:
            mensajes_error.append(f"Productos sin stock suficiente: {', '.join(productos_sin_stock)}")
        
        if mensajes_error:
            messagebox.showerror("Error en venta", "\n".join(mensajes_error))
            return

        # Segunda pasada: Realizar la venta si todo está bien
        for item in tabla.get_children():
            valores = tabla.item(item, "values")
            nombre, codigo, cantidad, unidad = valores
            cantidad = int(cantidad)
            
            for producto in inventario:
                if producto["codigo"] == codigo:
                    producto["cantidad"] -= cantidad
                    productos_vendidos.append(codigo)
                    break

        # Filtrar productos agotados
        inventario = [prod for prod in inventario if prod["cantidad"] > 0]

        guardar_inventario(inventario)

        # Eliminar productos vendidos de la lista de compras
        for item in tabla.get_children():
            valores = tabla.item(item, "values")
            if valores[1] in productos_vendidos:
                tabla.delete(item)

        messagebox.showinfo("Venta realizada", "Los productos han sido vendidos y actualizados en el inventario.")
def agregar_producto(entry_nombre, entry_codigo, entry_cantidad, combo_unidades, entry_precio,tabla):
        nombre = entry_nombre.get()
        codigo = entry_codigo.get()
        cantidad = entry_cantidad.get()
        unidad = combo_unidades.get()
        precio = entry_precio.get() # Asegura que esto se obtiene correctamente

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
        nuevo_producto = {"nombre": nombre, "codigo": codigo, "cantidad": cantidad, "unidad": unidad, "precio": precio}
        inventario.append(nuevo_producto)
        guardar_inventario(inventario)

        # Insertar en la tabla
        tabla.insert("", "end", values=(nombre, codigo, cantidad, unidad, precio))

        # Limpiar entradas
        entry_nombre.delete(0, tk.END)
        entry_codigo.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        combo_unidades.set("")
        entry_precio.delete(0, tk.END)


def ventana_inventario():
        """Ventana principal de inventario."""
        raiz = tk.Tk()
        raiz.iconbitmap("satur.ico.ico")
        raiz.geometry("870x500")
        raiz.title("COSMOS IA - Lista de Compras")
        raiz.config(bg="#d5f5e3")

        # ==================== MENÚ PRINCIPAL ====================
        menu_principal = tk.Menu(raiz)
        raiz.config(menu=menu_principal)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menu_principal, tearoff=0)
        menu_archivo.add_command(label="Nuevo Archivo")
        menu_archivo.add_command(label="Nueva Ventana")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Cerrar sesión", command=raiz.quit)
        
        # Menú Almacén
        menu_almacen = tk.Menu(menu_principal, tearoff=0)
        menu_almacen.add_command(label="Inventario", command=productos_almacen)
        
        # Añadir menús a la barra principal
        menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
        menu_principal.add_cascade(label="Almacén", menu=menu_almacen)

        # ==================== FRAME PRINCIPAL ====================
        frame_principal = tk.Frame(raiz, bg="#eafaf1", bd=10, relief="ridge")
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # ==================== SECCIÓN DE AGREGAR PRODUCTOS ====================
        tk.Label(frame_principal, text="Agregar a Lista de Compras", 
                fg="#006064", font=("Josefin Sans", 12, "bold"), 
                bg="#eafaf1").grid(row=0, column=0, columnspan=3, pady=5, sticky="w")

        # Campos de entrada
        tk.Label(frame_principal, text="Nombre:", bg="#eafaf1").grid(row=1, column=0, sticky="w")
        entry_nombre = tk.Entry(frame_principal)
        entry_nombre.grid(row=1, column=1, pady=2, sticky="ew")

        tk.Label(frame_principal, text="Código:", bg="#eafaf1").grid(row=2, column=0, sticky="w")
        entry_codigo = tk.Entry(frame_principal)
        entry_codigo.grid(row=2, column=1, pady=2, sticky="ew")

        tk.Label(frame_principal, text="Cantidad:", bg="#eafaf1").grid(row=3, column=0, sticky="w")
        entry_cantidad = tk.Entry(frame_principal)
        entry_cantidad.grid(row=3, column=1, pady=2, sticky="ew")

        tk.Label(frame_principal, text="Unidad:", bg="#eafaf1").grid(row=4, column=0, sticky="w")
        combo_unidades = ttk.Combobox(frame_principal, values=["Kg", "Lt", "Unidad"], state="readonly")
        combo_unidades.grid(row=4, column=1, pady=2, sticky="ew")

        # Botón de agregar a lista
        btn_agregar = tk.Button(
            frame_principal, 
            text="Agregar a Lista", 
            command=lambda: agregar_a_lista_compras(
                entry_nombre, entry_codigo, entry_cantidad, 
                combo_unidades, tabla
            ),
            bg="#2ecc71", fg="white"
        )
        btn_agregar.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        # ==================== TABLA DE LISTA DE COMPRAS ====================
        frame_tabla = tk.Frame(frame_principal)
        frame_tabla.grid(row=6, column=0, columnspan=3, pady=10, sticky="nsew")

        columnas = ("Nombre", "Código", "Cantidad", "Unidad")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)
        
        # Configurar columnas
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=120, anchor="center")
        tabla.column("Nombre", width=200)

        # Scrollbar
        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        scroll.pack(side="right", fill="y")
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(fill="both", expand=True)

        # ==================== SECCIÓN DE ELIMINACIÓN ====================
        frame_acciones = tk.Frame(frame_principal, bg="#eafaf1")
        frame_acciones.grid(row=7, column=0, columnspan=3, pady=10, sticky="ew")

        # Botón para eliminar producto seleccionado
        btn_eliminar = tk.Button(
            frame_acciones, 
            text="Eliminar Seleccionado", 
            command=lambda: eliminar_seleccionado(tabla),
            bg="#e74c3c", fg="white"
        )
        btn_eliminar.pack(side="left", padx=5)

        # Botón para vaciar toda la lista
        btn_vaciar = tk.Button(
            frame_acciones,
            text="Vaciar Lista",
            command=lambda: vaciar_lista(tabla),
            bg="#f39c12", fg="white"
        )
        btn_vaciar.pack(side="left", padx=5)

        # ==================== BOTÓN DE VENTA ====================
        btn_vender = tk.Button(
            frame_principal,
            text="Realizar Venta",
            command=lambda: vender_productos(tabla),
            bg="#3498db", fg="white"
        )
        btn_vender.grid(row=8, column=0, columnspan=3, pady=10, sticky="ew")

        # ==================== FUNCIONES ADICIONALES ====================
        def eliminar_seleccionado(tabla):
            """Elimina el producto seleccionado de la lista de compras."""
            seleccionado = tabla.selection()
            if not seleccionado:
                messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
                return
            tabla.delete(seleccionado)

        def vaciar_lista(tabla):
            """Elimina todos los productos de la lista de compras."""
            if not messagebox.askyesno("Confirmar", "¿Vaciar toda la lista de compras?"):
                return
            for item in tabla.get_children():
                tabla.delete(item)

        # Configurar grid
        frame_principal.grid_columnconfigure(1, weight=1)
                
   # Cargar productos guardados en la tabla
        raiz.mainloop()

ventana_inventario()
