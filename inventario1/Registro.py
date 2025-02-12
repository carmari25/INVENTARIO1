from tkinter import*
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import inicio

USUARIOS_FILE = "USUARIO.json"

def ventana_registro():
    inicio.ventana_inicio()

def guardar_usuario(usuario):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuario, f, indent=4)

def actualizar_stock(cedula):
    usuario = cargar_usuario()
    for personal in usuario:
        if personal["cedula"] == cedula:
                guardar_usuario(usuario)
                return True
        else:
                return False
    return None

def cargar_usuario():
    """Carga los usuarios desde el archivo JSON."""
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    return []  # Si el JSON no es una lista, retornar lista vacía
            except json.JSONDecodeError:
                return []  # Si hay error en el JSON, retornar lista vacía
    return []  # Si el archivo no existe, retornar lista vacía

def agregar_usuario():
    """Añade un usuario al registro y verifica si la cédula ya está registrada."""
    nombre = codigo2.get().strip()
    apellido = codigo3.get().strip()
    cedula = codigo4.get().strip()
    numero = codigo5.get().strip()
    
    
    if not nombre or not apellido or not cedula or not numero:
        messagebox.showwarning("Error", "Todos los campos son obligatorios")
        return
  
    usuario = cargar_usuario()

    # Verificar que la estructura del usuario sea una lista de diccionarios
    if not isinstance(usuario, list):
        usuario = []

    # Verificar si la cédula ya está registrada
    for personal in usuario:
        if isinstance(personal, dict) and personal.get("cedula") == cedula:
            messagebox.showwarning("Error", f"La cédula {cedula} ya está registrada.")
            return
    
    # Agregar el usuario
    nuevo_usuario = {"nombre": nombre, "apellido": apellido, "cedula": cedula, "numero": numero}
    usuario.append(nuevo_usuario)
    guardar_usuario(usuario)

    messagebox.showinfo("Éxito", "Usuario registrado correctamente.")

    # Limpiar entradas
    codigo2.delete(0, tk.END)
    codigo3.delete(0, tk.END)
    codigo4.delete(0, tk.END)
    codigo5.delete(0, tk.END)

        

raiz=Tk()

raiz.iconbitmap("inventario1/satur.ico.ico")


raiz.title("COSMOS IA")


frame1=Frame(raiz, width=400 , height=500)
frame1.config(bg="#abebc6")
frame1.pack()

label2=Label(frame1, text= "Nombre", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6" )
label2.place(x=165,y=10 )

codigo2=Entry(frame1)
codigo2.place(x=130 , y=35)

label3=Label(frame1, text= "Apellido", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6" )
label3.place(x=165,y=90 )

codigo3=Entry(frame1)
codigo3.place(x=130 , y=115)

label4=Label(frame1, text= "cedula", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6" )
label4.place(x=165,y=170 )

codigo4=Entry(frame1)
codigo4.place(x=130 , y=195)

label5=Label(frame1, text= "Numero", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6" )
label5.place(x=165,y=250 )

codigo5=Entry(frame1)
codigo5.place(x=130 , y=275)




botonregis=Button(frame1, text="Agregar",fg="#006064", font=("Josefin Sans", 13), command=agregar_usuario )
botonregis.place(x=150,y=350 )

botoneli=Button(frame1, text="Eliminar",fg="#006064", font=("Josefin Sans", 13) )
botoneli.place(x=150,y=400 )



raiz.mainloop()