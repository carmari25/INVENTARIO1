from tkinter import*

raiz=Tk()

raiz.iconbitmap("inventario1/satur.ico.ico")

raiz.geometry("1000x500")

raiz.title("COSMOS IA")

raiz.config(bg="#d5f5e3")

miFrame=Frame()
miFrame.pack(fill="x", expand="True")
miFrame.config(bg="#eafaf1")
miFrame.config(width="500", height="600")
miFrame.config(bd=20)
miFrame.config(relief="ridge")
miFrame.config(cursor="arrow")



miLabel=Label(miFrame, text= "Bienvenido", fg="#006064", font=("Josefin Sans", 15) )
miLabel.config(bg="#eafaf1")
miLabel.place(x=10 , y=10)

label2=Label(miFrame, text= "Producto", fg="#006064", font=("Josefin Sans", 10), bg="#eafaf1" )
label2.place(x=10,y=40 )

codigo=Entry(miFrame)
codigo.place(x=70 , y=40)


label2=Label(miFrame, text= "codigo", fg="#006064", font=("Josefin Sans", 10), bg="#eafaf1" )
label2.place(x=10,y=70 )

codigo=Entry(miFrame)
codigo.place(x=60 , y=70)

label3=Label(miFrame, text="En que unidades:",bg="#eafaf1").place(x=230,y=10)

opcion=IntVar()

Radiobutton(raiz, text="Cantidad", bg="#eafaf1", variable=opcion, value=1).place(x=250, y=50)
Radiobutton(raiz, text="Kg", bg="#eafaf1", variable=opcion, value=2).place(x=250, y=80)
Radiobutton(raiz, text="Lt", bg="#eafaf1", variable=opcion, value=3).place(x=250, y=110)

menu1=Menu(raiz)
raiz.config( menu=menu1, width=300, height=300 )

archivo=Menu(menu1)
ventas=Menu(menu1)
herramienta=Menu(menu1)
total=Menu(menu1)
inventario=Menu(menu1)

menu1.add_cascade(label="Archivo", menu=archivo)
menu1.add_cascade(label="Ventas", menu=ventas)
menu1.add_cascade(label="Herramienta", menu=herramienta)
menu1.add_cascade(label="Inventario", menu=inventario)
menu1.add_cascade(label="Total", menu=total)



raiz.mainloop()