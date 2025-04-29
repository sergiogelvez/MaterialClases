import tkinter as tk
import pandas as pd

dict = { 
         'nombre': ["Gato con botas"],
         'estatura': [1.80], 
         'color de ojos': ["Avellana"]
        } 

df = pd.DataFrame(dict)
print(df)

def salvar():
    df.to_csv("gato.csv")

def agregar(df):
    df3 = df
    estatura = float(text_estatura.get())
    nombre = text_nombre.get()
    ojos = text_ojos.get()
    dict2 = { 
         'nombre': [nombre],
         'estatura': [estatura], 
         'color de ojos': [ojos]
         }
    df2 = pd.DataFrame(dict2)
    df = pd.concat(df3, df2)
    print(df)

#Agregar cosas al dataframe
# 




ventana = tk.Tk()

ventana.title("Formulario")
ventana.geometry('640x480')
ventana.resizable(False, False)

lbl_nombre = tk.Label(ventana, text="Nombre:")
lbl_estatura = tk.Label(ventana, text="Estatura:")
lbl_ojos = tk.Label(ventana, text="ojos:")

text_nombre = tk.Entry( ventana, width=20)
text_estatura = tk.Entry( ventana, width=20)
text_ojos = tk.Entry( ventana, width=20)

lbl_nombre.pack()
text_nombre.pack()

lbl_estatura.pack()
text_estatura.pack()

lbl_ojos.pack()
text_ojos.pack()

btn_agregar = tk.Button(ventana, text="Agregar", command= lambda : agregar(df) )
btn_salvar = tk.Button(ventana, text="Salvar", command=salvar)
btn_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)

btn_agregar.pack()
btn_salvar.pack()
btn_salir.pack()



# el código del funcionamiento de la ventana debe ir antes del main loop
ventana.mainloop()
