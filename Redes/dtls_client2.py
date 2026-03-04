import ssl
import socket
import time
from dtls import do_patch

# Aplicar parche: después de esto, ssl.wrap_socket detecta
# automáticamente si el socket es UDP y usa DTLS
do_patch()

SERVIDOR = '127.0.0.1'
PORT = 9002

def main():
    # Crear socket UDP y conectar al servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((SERVIDOR, PORT))

    # Envolver en DTLS (el parche hace que wrap_socket use DTLS
    # cuando detecta un socket SOCK_DGRAM)
    conn_dtls = ssl.wrap_socket(
        sock,
        ca_certs='certificado.pem',
        cert_reqs=ssl.CERT_REQUIRED,
        do_handshake_on_connect=True
    )

    print('Handshake DTLS completado')

    try:
        mensajes = [
            'Hola, este es el primer mensaje seguro por UDP',
            'Este datagrama viaja encriptado',
            'Cada paquete se encripta de forma independiente',
            'Ultimo mensaje, adios'
        ]

        for msg in mensajes:
            conn_dtls.write(msg.encode('utf-8'))
            respuesta = conn_dtls.read(1024).decode('utf-8')
            print(f'Enviado: {msg}')
            print(f'Respuesta: {respuesta}')
            time.sleep(1)

    except ssl.SSLError as e:
        print(f'Error DTLS: {e}')
    finally:
        try:
            conn_dtls.shutdown()
        except:
            pass
        sock.close()

    print('Sesión DTLS cerrada')

if __name__ == '__main__':
    main()