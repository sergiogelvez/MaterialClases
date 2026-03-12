import socket
HOST = '127.0.0.1' # escuchar en todas las interfaces
PORT = 5051 # o otro puerto que se anuncie

def manejar_cliente(conn, addr):
    print(f'Conexión desde {addr}')
    with conn:
        while True:
            datos = conn.recv(1024)
            if not datos:
                break
            mensaje = datos.decode('utf-8')
            print(f'Recibido: {mensaje}')
            respuesta = f'Servidor recibio: {mensaje}'
            conn.sendall(respuesta.encode('utf-8'))
            print('Conexión cerrada')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f'Servidor TCP escuchando en el puerto {PORT}')
        while True:
            conn, addr = s.accept()
            manejar_cliente(conn, addr)

if __name__ == '__main__':
    main()