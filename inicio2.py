from tkinter import *
from tkinter import messagebox
import json
import os



USUARIOS_FILE = "USUARIO.json"



# Función para cargar usuarios desde el archivo JSON
def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                pass
    return []

# Función para guardar un nuevo usuario en el archivo JSON
def guardar_usuario(nombre, apellido, cedula, numero):
    usuarios = cargar_usuarios()  # Cargar usuarios existentes

    # Verificar si el usuario ya está registrado
    for user in usuarios:
        if user["cedula"] == cedula:
            messagebox.showerror("Error", "Esta cédula ya está registrada")
            return

    # Crear un nuevo usuario
    nuevo_usuario = {
        "nombre": nombre,
        "apellido": apellido,
        "cedula": cedula,
        "numero": numero
    }
    
    usuarios.append(nuevo_usuario)  # Agregar usuario a la lista

    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)  # Guardar en el archivo JSON

    messagebox.showinfo("Éxito", "Usuario registrado correctamente")
    
# Función para abrir la ventana de registro
def abrir_registro():
    inicio.destroy()
    ventana_registro()

# Ventana de Registro
def ventana_registro():
    registro = Tk()
    registro.iconbitmap("satur.ico.ico")
    registro.title("Registro - COSMOS IA")
    registro.geometry("400x500")
    registro.config(bg="#abebc6")

    frame1 = Frame(registro, width=400, height=500, bg="#abebc6")
    frame1.pack()

    Label(frame1, text="Nombre", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6").place(x=165, y=10)
    entry_nombre = Entry(frame1)
    entry_nombre.place(x=130, y=35)

    Label(frame1, text="Apellido", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6").place(x=165, y=90)
    entry_apellido = Entry(frame1)
    entry_apellido.place(x=130, y=115)

    Label(frame1, text="Cédula", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6").place(x=165, y=170)
    entry_cedula = Entry(frame1)
    entry_cedula.place(x=130, y=195)

    Label(frame1, text="Número", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6").place(x=165, y=250)
    entry_numero = Entry(frame1)
    entry_numero.place(x=130, y=275)

    # Función para guardar usuario al presionar "Agregar"
    def agregar_usuario():
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        cedula = entry_cedula.get().strip()
        numero = entry_numero.get().strip()

        if not nombre or not apellido or not cedula or not numero:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        guardar_usuario(nombre, apellido, cedula, numero)
        registro.destroy()
        ventana_inicio()

    # Botón para guardar usuario
    Button(frame1, text="Agregar", fg="#006064", font=("Josefin Sans", 13), command=agregar_usuario).place(x=150, y=350)
    
    # Botón para volver a la ventana de inicio
    Button(registro, text="Volver", font=("Arial", 12), command=lambda: [registro.destroy(), ventana_inicio()]).pack(pady=20)

    registro.mainloop()




#from tkinter import *
from tkinter import messagebox
import json
import os

USUARIOS_FILE = "USUARIO.json"

# [Mantén aquí todas tus otras funciones: cargar_usuarios, guardar_usuario, etc...]

def ventana_inicio():
    global inicio
    
    def on_closing():
        inicio.destroy()
        # Para manejar correctamente el cierre en sistemas con múltiples hilos
        if 'login_exitoso' in locals():
            return login_exitoso
        return False

    inicio = Tk()
    inicio.title("INICIO")
    inicio.geometry("400x500")
    inicio.config(bg="#d5f5e3")

    frame1 = Frame(inicio, width=400, height=500, bg="#abebc6")
    frame1.pack()

    Label(frame1, text="Usuario", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6").place(x=70, y=300)
    entry_usuario = Entry(frame1)
    entry_usuario.place(x=140, y=300)

    Label(frame1, text="Cédula", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6").place(x=70, y=350)
    entry_cedula = Entry(frame1)
    entry_cedula.place(x=140, y=350)

    try:
        usuario_img = PhotoImage(file="usuario.png")
        Label(frame1, image=usuario_img).place(x=120, y=100)
    except:
        pass

    login_exitoso = False

    def iniciar_sesion():
        nonlocal login_exitoso
        nombre = entry_usuario.get().strip()
        cedula = entry_cedula.get().strip()

        if not nombre or not cedula:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return False

        usuarios = cargar_usuarios()
        for user in usuarios:
            if user["nombre"] == nombre and user["cedula"] == cedula:
                messagebox.showinfo("Acceso Concedido", "Bienvenido al sistema")
                login_exitoso = True
                inicio.destroy()
                return True

        messagebox.showerror("Error", "Usuario o cédula incorrectos.")
        return False

    inicio.protocol("WM_DELETE_WINDOW", on_closing)
    Button(inicio, text="Aceptar", command=iniciar_sesion).place(x=150, y=400)
    Button(inicio, text="Registrarse", command=abrir_registro).place(x=140, y=450)

    inicio.mainloop()
    return login_exitoso

# [Mantén aquí tus otras funciones como ventana_registro()]

# Elimina la llamada a ventana_inicio() al final del archivo
# para que no se ejecute automáticamente al importar