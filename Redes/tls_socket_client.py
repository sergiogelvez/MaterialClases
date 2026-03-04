import socket
import ssl
import time

SERVIDOR = '127.0.0.1'  # cambiar por la IP del servidor si es otra máquina
PORT = 9001

def main():
    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # Cargar el certificado del servidor como confiable
    # (en un entorno real, el sistema tiene CAs preinstaladas)
    contexto.load_verify_locations('certificado.pem')
    # El nombre del servidor debe coincidir con el CN del certificado
    contexto.check_hostname = True

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with contexto.wrap_socket(s, server_hostname='localhost') as s_seguro:
            s_seguro.connect((SERVIDOR, PORT))
            print(f'Conectado con TLS')
            print(f'  Versión: {s_seguro.version()}')
            print(f'  Cipher:  {s_seguro.cipher()}')

            mensajes = [
                'Hola, este es el primer mensaje seguro',
                'Este mensaje viaja encriptado',
                'Ni Wireshark puede leer esto',
                'Ultimo mensaje, adios'
            ]

            for msg in mensajes:
                s_seguro.sendall(msg.encode('utf-8'))
                respuesta = s_seguro.recv(1024).decode('utf-8')
                print(f'Enviado: {msg}')
                print(f'Respuesta: {respuesta}')
                time.sleep(1)  # separar mensajes en la traza

    print('Conexión cerrada')

if __name__ == '__main__':
    main()