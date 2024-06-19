path = "."
nombre_archivo = "base.txt"

opcion = 1
while opcion != 0 :
    print("Escoja una opcion:")
    print("1. Crear archivo nuevo")
    print("2. Leer archivo y mostrar datos")
    print("3. Agregar datos al archivo")
    print("4. Borrar datos del archivo")
    print("0. Salir")
    opcion = int(input(": "))
    match opcion:
        case 0 :
            print("Gracias, hasta pronto")
        case 1 :
            print("\n\n****************")
            print("Advertencia: si hay un archivo este se borrara!!")
            print("****************\n\n ")
            print("Desea continuar, (s)i o (n)o?")
            cont = input("_ ")
            if cont == "n" or cont == "N" :
                continue
            elif cont == "s" or cont == "S" :
                archivo = open(path + "/" + nombre_archivo, "+wt")
                linea = ""
                while linea != "0" :
                    linea = input(">")
                    if linea != "0" :
                        archivo.write(linea + "\n")
                archivo.close()
            else :
                print("Opcion no valida, abortado")
        case 2 :
            print("Intentando acceder al archivo de datos")
            try :
                archivo = open(path + "/" + nombre_archivo, "rt")
                lineas = archivo.readlines()
                for linea in lineas :
                    print(linea, end="")
                archivo.close()
            except :
                print("No existe el archivo de datos \n")
        case 3 :
            print("Si no hay un archivo este se creará")
            archivo = open(path + "/" + nombre_archivo, "at")
            linea = ""
            while linea != "0" :
                linea = input(">")
                if linea != "0" :
                    archivo.write(linea + "\n")
            archivo.close()
        case 4 :
            print("Intentando acceder al archivo de datos")
            try :
                archivo = open(path + "/" + nombre_archivo, "rt")
                lineas = archivo.readlines()
                nlinea = 0
                for linea in lineas :
                    print(str(nlinea) + ": " + linea, end="")
                    nlinea += 1
                maxlineas = nlinea
                print(f"Que linea desea borrar? (maximo {maxlineas}) : ")
                borrar = int(input(""))
                if borrar < nlinea :
                    lineas.pop(borrar)
                # se muestra la lista de lineas como viene
                archivo.close()
                archivo = open(path + "/" + nombre_archivo, "+wt")
                # se escribe el nuevo archivo
                for linea in lineas :
                    print(linea, end="")
                    archivo.write(linea)

                    
                
                archivo.close()
            except :
                
                print("No existe el archivo de datos \n")
        case _:
            print("Opcion invalida")



