from tkinter import*
from tkinter import messagebox
import json
import os

# Archivo donde se guardan los usuarios
USUARIOS_FILE = "USUARIO.json"

# Función para cargar los usuarios desde el JSON
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

# Función para verificar inicio de sesión
def iniciar_sesion():
    usuario = entry_usuario.get().strip()
    cedula = entry_cedula.get().strip()

    if not usuario or not cedula:
        messagebox.showwarning("Error", "Todos los campos son obligatorios")
        return

    usuarios = cargar_usuarios()

    # Buscar coincidencia en la lista de usuarios registrados
    for personal in usuarios:
        if personal.get("nombre") == usuario and personal.get("cedula") == cedula:
            messagebox.showinfo("Acceso Concedido", "Bienvenido al sistema")
            raiz.destroy()  # Cierra la ventana de inicio de sesión
            abrir_ventana_principal()
            return

    messagebox.showerror("Error", "Usuario o cédula incorrectos. Verifique sus datos.")

# Función para abrir la ventana principal (luego de iniciar sesión)
def abrir_ventana_principal():
    ventana = Tk()
    ventana.title("Sistema de Inventario")
    ventana.geometry("400x500")
    Label(ventana, text="¡Bienvenido al Sistema de Inventario!", font=("Arial", 14)).pack(pady=20)
    ventana.mainloop()
    

raiz=Tk()

raiz.iconbitmap("inventario1/satur.ico.ico")


raiz.title("COSMOS IA")



frame1=Frame(raiz, width=400 , height=500)
frame1.config(bg="#abebc6")
frame1.pack()

label2=Label(frame1, text= "Usuario", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6" )
label2.place(x=70,y=300 )

usuario=Entry(frame1)
usuario.place(x=140 , y=300)

label2=Label(frame1, text= "Cedula", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6" )
label2.place(x=40,y=350 )

cedula=Entry(frame1)
cedula.place(x=140 , y=350)


botonregis=Button(frame1, text="Registrar",fg="#006064", font=("Josefin Sans", 13) )
botonregis.place(x=150,y=400 )

usuario=PhotoImage(file="inicio/usuario.png")
Label(frame1 , image= usuario).place(x=120, y=100)




botonent= Button(raiz, text="Aceptar" )
botonent.pack()



raiz.mainloop()