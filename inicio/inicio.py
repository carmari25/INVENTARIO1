from tkinter import*

raiz=Tk()

raiz.iconbitmap("inventario1/satur.ico.ico")


raiz.title("COSMOS IA")



frame1=Frame(raiz, width=400 , height=500)
frame1.config(bg="#abebc6")
frame1.pack()

label2=Label(frame1, text= "Usuario", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6" )
label2.place(x=70,y=300 )

codigo=Entry(frame1)
codigo.place(x=140 , y=300)

label2=Label(frame1, text= "Contraseña", fg="#006064", font=("Josefin Sans", 13), bg="#abebc6" )
label2.place(x=40,y=350 )

codigo=Entry(frame1)
codigo.place(x=140 , y=350)
codigo.config(show="*")

usuario=PhotoImage(file="inicio/usuario.png")
Label(frame1 , image= usuario).place(x=120, y=100)




botonent= Button(raiz, text="Aceptar" )
botonent.pack()



raiz.mainloop()