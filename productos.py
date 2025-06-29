import json
import os
import tkinter as tk
from tkinter import ttk, messagebox


INVENTARIO_FILE = "inventario.json"

def cargar_inventario():
    if os.path.exists(INVENTARIO_FILE):
        try:
            with open(INVENTARIO_FILE, "r") as f:
                contenido = f.read()
                if contenido.strip() == "":
                    return []  # Archivo vacío → retorna lista vacía
                datos = json.loads(contenido)
                # Si el archivo no tiene "precio" en sus productos, lo agregamos
                for producto in datos:
                    if "precio" not in producto:
                        producto["precio"] = 0.0  # Valor por defecto
                return datos
        except json.JSONDecodeError:
            print("El archivo estaba corrupto. Se creará uno nuevo.")
            return []
    return []  # Si el archivo no existe

def guardar_inventario(inventario):
    with open(INVENTARIO_FILE, "w") as f:
        json.dump(inventario, f, indent=4)

def inicializar_inventario():
    if not os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, "w") as f:
            json.dump([], f)

# Llamar al inicio del programa
inicializar_inventario()

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


def agregar_producto():
    # Obtener valores (esto ya está bien)
    nombre = entry_nombre.get().strip()
    codigo = entry_codigo.get().strip()
    cantidad = entry_cantidad.get().strip()
    unidad = combo_unidades.get().strip()
    precio = entry_precio.get().strip()  # Asegúrate de que entry_precio esté definido antes
    
    # Validar campos vacíos (incluyendo precio)
    if not all([nombre, codigo, cantidad, unidad, precio]):  # precio ahora está incluido
        messagebox.showwarning("Error", "Todos los campos son obligatorios (incluyendo precio)")
        return
    
    # Validar tipos de datos (cantidad = entero, precio = float)
    try:
        cantidad = int(cantidad)
        precio = float(precio)  # Convertir a float
    except ValueError:
        messagebox.showwarning("Error", "Cantidad debe ser entero y Precio debe ser número (ej: 10.99)")
        return
    
    # Resto del código (verificación de código existente y guardado)...
    
    # Verificar si el código ya existe
    inventario = cargar_inventario()
    if any(producto["codigo"] == codigo for producto in inventario):
        messagebox.showwarning("Error", f"El código {codigo} ya existe")
        return
    
    # Crear nuevo producto
    nuevo_producto = {
        "nombre": nombre,
        "codigo": codigo,
        "cantidad": cantidad,
        "unidad": unidad,
        "precio": precio
    }
    
    # Actualizar inventario y tabla
    inventario.append(nuevo_producto)
    guardar_inventario(inventario)
    tabla.insert("", "end", values=(nombre, codigo, cantidad, unidad, precio))
    
    # Limpiar campos
    entry_nombre.delete(0, tk.END)
    entry_codigo.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    combo_unidades.set("")
    entry_precio.delete(0, tk.END)
    
    
   

def cargar_productos_en_tabla():
    """Carga los productos guardados en la tabla al iniciar."""
    inventario = cargar_inventario()
    for producto in inventario:
        tabla.insert("", "end", values=(producto["nombre"], producto["codigo"], producto["cantidad"], producto["unidad"], producto["precio"]))

def eliminar_producto():
    """Elimina un producto del inventario según su código."""
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



# Crear ventana
raiz = tk.Tk()
raiz.title("Inventario - Cosmos IA")
raiz.geometry("850x450")
raiz.config(bg="#d5f5e3")
raiz.iconbitmap("satur.ico.ico")

# Etiquetas y entradas para agregar productos
tk.Label(raiz, text="Nombre:", bg="#eafaf1").place(x=20 , y=20)
entry_nombre = tk.Entry(raiz)
entry_nombre.place(x=80 , y=20)

tk.Label(raiz, text="Código:",bg="#eafaf1").place(x=20 , y=40)
entry_codigo = tk.Entry(raiz)
entry_codigo.place(x=80 , y=40)

tk.Label(raiz, text="Cantidad:", bg="#eafaf1").place(x=20 , y=60)
entry_cantidad = tk.Entry(raiz)
entry_cantidad.place(x=80 , y=60)

# Etiquetas y campos para Unidad y Precio (código corregido):
tk.Label(raiz, text="Unidad:", bg="#eafaf1").place(x=350, y=10)
combo_unidades = ttk.Combobox(raiz, values=["Kg", "Lt", "Cantidad"], state="readonly")
combo_unidades.place(x=350, y=30)

tk.Label(raiz, text="Precio:", bg="#eafaf1").place(x=350, y=60)  # Cambiado a y=60
entry_precio = tk.Entry(raiz)
entry_precio.place(x=400, y=60)  # Ajustado para alinearse con su label

# Botón para agregar producto
btn_agregar = tk.Button(raiz, text="Agregar Producto", command=agregar_producto)
btn_agregar.place(x=350 , y=55)

# Tabla para mostrar productos
columnas = ("Nombre", "Código", "Cantidad", "Unidad", "Precio")
tabla = ttk.Treeview(raiz, columns=columnas, show="headings")
for col in columnas:
    tabla.heading(col, text=col)
    tabla.place(x=20 , y=100)

# Cargar productos guardados en la tabla
cargar_productos_en_tabla()

# Sección para eliminar productos
tk.Label(raiz, text="Código a eliminar:", bg="#eafaf1").place(x=20, y=350)
entry_eliminar_codigo = tk.Entry(raiz)
entry_eliminar_codigo.place(x=130, y=350)

btn_eliminar = tk.Button(raiz, text="Eliminar Producto", command=eliminar_producto)
btn_eliminar.place(x=280, y=345)

# Ejecutar ventana


