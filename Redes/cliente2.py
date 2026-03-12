import socket
import time

HOST = '127.0.0.1' # <-- cambiar por la IP del servidor
PORT = 5051 # o otro puerto que se anuncie

mensajes = [
    'Hola, este es el primer mensaje',
    'Este es el segundo mensaje',
    'Este es el tercer mensaje',
    'Este es el cuarto mensaje',
    'Este es el quinto y ultimo mensaje',
]

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f'Conectado a {HOST}:{PORT}')
        for msg in mensajes:
            s.sendall(msg.encode('utf-8'))
            print(f'Enviado: {msg}')
            time.sleep(1) # pausa para separar paquetes en Wireshark
            resp = s.recv(1024)
            print(f'Recibido: {resp.decode("utf-8")}')
    print('Conexión cerrada')

if __name__ == '__main__':
    main()