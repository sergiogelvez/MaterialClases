import socket
import ssl

HOST = '0.0.0.0'
PORT = 9001  # puerto diferente al taller anterior para poder comparar

def crear_contexto_tls():
    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contexto.load_cert_chain('certificado.pem', 'clave.pem')
    # Mostrar qué versión de TLS y cipher se negociaron
    return contexto

def manejar_cliente(conn_segura, addr):
    print(f'Conexión TLS desde {addr}')
    print(f'  Versión: {conn_segura.version()}')
    print(f'  Cipher:  {conn_segura.cipher()}')
    with conn_segura:
        while True:
            datos = conn_segura.recv(1024)
            if not datos:
                break
            mensaje = datos.decode('utf-8')
            print(f'Recibido: {mensaje}')
            respuesta = f'Servidor recibio: {mensaje}'
            conn_segura.sendall(respuesta.encode('utf-8'))
    print('Conexión cerrada')

def main():
    contexto = crear_contexto_tls()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f'Servidor TLS escuchando en el puerto {PORT}')
        with contexto.wrap_socket(s, server_side=True) as s_seguro:
            while True:
                conn_segura, addr = s_seguro.accept()
                manejar_cliente(conn_segura, addr)

if __name__ == '__main__':
    main()
