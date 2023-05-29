# import everything from tkinter module
from tkinter import *

def test():
    mensaje = texto1.get()
    print(mensaje)

# create a tkinter window
root = Tk()

root.title("Gato con botas")

# Open window having dimension 100x100
root.geometry('640x480')

# Create a Button
#btn = Button(root, text = 'Click me !', bd = '5', command = root.destroy)
btn = Button(root, text = 'Click me !', bd = '1', command = test)

# Set the position of button on the top of window.
btn.pack(side = 'bottom')


# Label is what output will be
# show on the window
label1 = Label(root, text ="Miau !")
label1.pack()

label2 = Label(root, text ="Valor de algo:")
label2.place(x=200, y=100)

texto1 = Entry(root, width=20)
texto1.place(x=300, y=100)
# calling mainloop method which is used
# when your application is ready to run
# and it tells the code to keep displaying
root.mainloop()