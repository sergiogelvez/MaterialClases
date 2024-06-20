path = "./Archivos"
nArchivo = "base.txt"

opcion = 1
while opcion != 0 :
    print("\n\nMenu de la aplicación")
    print("1. Crear archivo de datos desde cero" )
    print("2. Visualizar datos" )
    print("3. Agregar datos al archivo" )
    print("4. Borrar datos del archivo" )
    print("5. Editar datos del archivo" )
    print("6. Insertar datos al archivo en una posicion" )
    print("0. Salir." )
    opcion = int(input(": "))
    match opcion:
        case 0 :
            print("Muchas gracias, hasta pronto \n") 
        case 1 : # opcion de crear archivo principal desde 0
            print("\n**************")
            print("Advertencia: Si el archivo existe se borrarán todos los datos")
            print("**************\n")
            cont = input("Desea continuar? (s)i o (n)o : ")
            if cont == "S" or cont == "s" :
                archivo = open(path + "/" + nArchivo, "w+t")
                print("Por favor ingrese un dato y presione enter.  Para terminar ingrese 0 :")
                linea = ""
                while linea != "0" :
                    linea = input("> ")
                    if linea != "0" :
                        # Se puede arreglar para que no deje saltos de linea de mas
                        archivo.write(f"{linea}\n")
                archivo.close()
            elif cont == "N" or cont == "n" :
                print("\nProceso abortado por el usuario\n")
            else :
                print("\nEntrada incorrecta. Proceso abortado por defecto\n")
        case 2 : # visualizar datos, leer del archivo y mostrar en pantalla
            try :
                archivo = open(path + "/" + nArchivo, "rt")
                lineas = archivo.readlines()
                nlineas = 0
                print("\n\nContenido del archivo: \n")
                for linea in lineas :
                    # recordar que va el fin de linea en la variable linea
                    print(f"{linea}", end="")
                    nlineas += 1
                print(f"Se leyeron {nlineas} registros.")
                archivo.close()
            except FileNotFoundError :
                print("Error, el archivo principal no existe. \n\n")
        case 3 : # agregar datos al archivo 
            archivo = open(path + "/" + nArchivo, "at")
            print("Por favor ingrese un dato y presione enter.  Para terminar ingrese 0 :")
            linea = ""
            while linea != "0" :
                linea = input("> ")
                if linea != "0" :
                    # Se puede arreglar para que no deje saltos de linea de mas
                    archivo.write(f"{linea}\n")
            archivo.close()
        case 4 : # Borrar un dato del archivo
            try :
                archivo = open(path + "/" + nArchivo, "rt")
                lineas = archivo.readlines()
                nlineas = 0
                print("\n\nContenido del archivo: \n")
                for linea in lineas :
                    # recordar que va el fin de linea en la variable linea
                    print(f"{nlineas}: {linea}", end="")
                    nlineas += 1
                print(f"Se leyeron {nlineas} registros.")
                archivo.close()
                maxlineas = nlineas
                borrar = -1
                while borrar >= maxlineas or borrar < 0:
                    borrar = int(input("Numero de linea a borrar: "))
                    if borrar < maxlineas :
                        lineas.pop(borrar)
                        archivo = open(path + "/" + nArchivo, "w+t")
                        for linea in lineas :
                            archivo.write(linea)
                        archivo.close()
                    else :
                        print("Numero de linea incorrecto.  Ingrese otro número de linea por favor")
            except FileNotFoundError :
                print("Error, el archivo principal no existe. \n\n")
        case 5 :
            try :
                archivo = open(path + "/" + nArchivo, "rt")
                lineas = archivo.readlines()
                nlineas = 0
                print("\n\nContenido del archivo: \n")
                for linea in lineas :
                    # recordar que va el fin de linea en la variable linea
                    print(f"{nlineas}: {linea}", end="")
                    nlineas += 1
                print(f"Se leyeron {nlineas} registros.")
                archivo.close()
                maxlineas = nlineas
                leditar = -1
                while leditar >= maxlineas or leditar < 0:
                    leditar = int(input("Numero de linea a editar: "))
                    if leditar < maxlineas :
                        lineas[leditar] = input("> ") + "\n"
                        archivo = open(path + "/" + nArchivo, "w+t")
                        for linea in lineas :
                            archivo.write(linea)
                        archivo.close()
                    else :
                        print("Numero de linea incorrecto.  Ingrese otro número de linea por favor")
            except FileNotFoundError :
                print("Error, el archivo principal no existe. \n\n")
        case 6 : # insertar un dato
            try :
                archivo = open(path + "/" + nArchivo, "rt")
                lineas = archivo.readlines()
                nlineas = 0
                print("\n\nContenido del archivo: \n")
                for linea in lineas :
                    # recordar que va el fin de linea en la variable linea
                    print(f"{nlineas}: {linea}", end="")
                    nlineas += 1
                print(f"Se leyeron {nlineas} registros.")
                archivo.close()
                maxlineas = nlineas
                borrar = -1
                while borrar >= maxlineas or borrar < 0:
                    borrar = int(input("Numero de linea de insercion (queda antes del punto): "))
                    if borrar < maxlineas :
                        datoNuevo = input("> ") + "\n"
                        lineas.insert(borrar, datoNuevo)
                        archivo = open(path + "/" + nArchivo, "w+t")
                        for linea in lineas :
                            archivo.write(linea)
                        archivo.close()
                    else :
                        print("Numero de linea incorrecto.  Ingrese otro número de linea por favor")
            except FileNotFoundError :
                print("Error, el archivo principal no existe. \n\n")
