from tkinter import*

raiz=Tk()

raiz.iconbitmap("satur.ico.ico")

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
codigo.place(x=60 , y=60)

raiz.mainloop()