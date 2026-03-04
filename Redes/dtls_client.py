import socket
import time
from OpenSSL import SSL

SERVIDOR = '127.0.0.1'  # cambiar si es otra máquina
PORT = 9002

def main():
    contexto = SSL.Context(SSL.TLSv1_2_METHOD)
    # Cargar certificado del servidor como confiable
    contexto.load_verify_locations('certificado.pem')
    # Para laboratorio, no verificamos el hostname
    contexto.set_verify(SSL.VERIFY_NONE, lambda *args: True)

    # Crear socket UDP y conectar
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((SERVIDOR, PORT))
    sock.settimeout(5)

    # Envolver en DTLS
    conn_dtls = SSL.Connection(contexto, sock)
    conn_dtls.set_connect_state()

    try:
        conn_dtls.do_handshake()
        print('Handshake DTLS completado')

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
            time.sleep(1)  # separar mensajes en la traza

        conn_dtls.shutdown()
        print('Sesión DTLS cerrada')

    except SSL.Error as e:
        print(f'Error DTLS: {e}')
    finally:
        sock.close()

if __name__ == '__main__':
    main()