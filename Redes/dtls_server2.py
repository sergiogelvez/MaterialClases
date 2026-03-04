import ssl
import socket
from dtls import do_patch
from dtls.sslconnection import SSLConnection

# Aplicar parche que habilita DTLS en el módulo ssl
do_patch()

HOST = '127.0.0.1'
PORT = 9002

def main():
    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))

    print(f'Servidor DTLS escuchando en {HOST}:{PORT}')

    # Envolver en conexión DTLS (modo servidor)
    conn_dtls = SSLConnection(
        sock,
        keyfile='clave.pem',
        certfile='certificado.pem',
        server_side=True,
        ca_certs='certificado.pem',
        do_handshake_on_connect=False
    )

    while True:
        print('Esperando conexión DTLS...')
        # listen() espera un ClientHello entrante
        conn_dtls.listen()

        # accept() completa el handshake y devuelve la conexión
        peer, addr = conn_dtls.accept()
        print(f'Conexión DTLS establecida con {addr}')

        try:
            while True:
                datos = peer.read(1024)
                if not datos:
                    break
                mensaje = datos.decode('utf-8')
                print(f'Recibido: {mensaje}')
                respuesta = f'Servidor recibio: {mensaje}'
                peer.write(respuesta.encode('utf-8'))
        except ssl.SSLError as e:
            print(f'Sesión terminada: {e}')
        except Exception as e:
            print(f'Error: {e}')
        finally:
            try:
                peer.shutdown()
            except:
                pass

        print('Sesión DTLS cerrada')

if __name__ == '__main__':
    main()