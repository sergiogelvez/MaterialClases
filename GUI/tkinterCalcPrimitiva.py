import tkinter as tk

def sumar():
    operando1 = texto1.get()
    operando2 = texto2.get()
    resultado = float(operando1) + float(operando2)
    print(resultado)
    textof.configure(state=tk.NORMAL)
    textof.delete(0, tk.END)
    textof.insert(0, resultado)
    textof.configure(state=tk.DISABLED)

def restar():
    operando1 = texto1.get()
    operando2 = texto2.get()
    resultado = float(operando1) - float(operando2)
    print(resultado)
    textof.configure(state=tk.NORMAL)
    textof.delete(0, tk.END)
    textof.insert(0, resultado)
    textof.configure(state=tk.DISABLED)

def multiplicar():
    operando1 = texto1.get()
    operando2 = texto2.get()
    resultado = float(operando1) * float(operando2)
    print(resultado)
    textof.configure(state=tk.NORMAL)
    textof.delete(0, tk.END)
    textof.insert(0, resultado)
    textof.configure(state=tk.DISABLED)

def dividir():
    operando1 = texto1.get()
    operando2 = texto2.get()
    resultado = float(operando1) / float(operando2)
    print(resultado)
    textof.configure(state=tk.NORMAL)
    textof.delete(0, tk.END)
    textof.insert(0, resultado)
    textof.configure(state=tk.DISABLED)

ventana = tk.Tk()

ventana.title("Kalculadora")
ventana.geometry('640x480')
ventana.resizable(False, False)

texto1 = tk.Entry( ventana, width=20)
texto2 = tk.Entry( ventana, width=20)
textof = tk.Entry( ventana, width=20, state="disabled")

etiqueta1 = tk.Label(ventana, text="Operando 1:")
etiqueta2 = tk.Label(ventana, text="Operando 2:")
etiquetaf = tk.Label(ventana, text="Resultado:")

boton_suma = tk.Button( ventana, text="+", bd = 3, command=sumar)
boton_resta = tk.Button( ventana, text="-", bd = 3, command=restar)
boton_producto = tk.Button( ventana, text="*", bd = 3, command=multiplicar)
boton_cociente = tk.Button( ventana, text="/", bd = 3, command=dividir)
boton_salir = tk.Button( ventana, text="salir", bd=2, command=ventana.destroy)

texto1.place(x=100, y=100)
texto2.place(x=100, y=200)
textof.place(x=100, y=300)

etiqueta1.place(x=200, y=100)
etiqueta2.place(x=200, y=200)
etiquetaf.place(x=200, y=300)

boton_suma.place(x=400, y=100)
boton_resta.place(x=450, y=100)
boton_producto.place(x=400, y=200)
boton_cociente.place(x=450, y=200)

boton_salir.pack(anchor="center", side="bottom")

ventana.mainloop()




