from tkinter import *
from tkinter import messagebox

def abrir_registro():
    """Cierra la ventana actual y abre la ventana de registro."""
    raiz.destroy()  # Cierra la ventana actual
    ventana_registro()  # Llama a la nueva ventana

def ventana_registro():
    """Crea la ventana de registro."""
    registro = Tk()
    registro.title("Registro de Usuario")
    registro.geometry("400x500")
    registro.config(bg="#d4e157")

    Label(registro, text="Registro de Usuario", font=("Arial", 16), bg="#d4e157").pack(pady=20)
    
    # Campos de entrada
    Label(registro, text="Nombre:", font=("Arial", 12), bg="#d4e157").pack()
    Entry(registro).pack()

    Label(registro, text="Cédula:", font=("Arial", 12), bg="#d4e157").pack()
    Entry(registro).pack()

    # Botón para volver a la ventana de inicio
    Button(registro, text="Volver", font=("Arial", 12), command=lambda: [registro.destroy(), ventana_inicio()]).pack(pady=20)

    registro.mainloop()

def ventana_inicio():
    """Crea la ventana de inicio."""
    global raiz
    raiz = Tk()
    raiz.title("Inicio de Sesión")
    raiz.geometry("400x500")
    raiz.config(bg="#abebc6")

    Label(raiz, text="Inicio de Sesión", font=("Arial", 16), bg="#abebc6").pack(pady=20)

    Label(raiz, text="Usuario:", font=("Arial", 12), bg="#abebc6").pack()
    Entry(raiz).pack()

    Label(raiz, text="Cédula:", font=("Arial", 12), bg="#abebc6").pack()
    Entry(raiz).pack()

    # Botón para ir a la ventana de registro
    Button(raiz, text="Registrarse", font=("Arial", 12), command=abrir_registro).pack(pady=20)

    raiz.mainloop()

# Inicia la primera ventana
ventana_inicio()
