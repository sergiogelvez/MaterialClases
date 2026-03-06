import socket
from OpenSSL import SSL, crypto

HOST = '0.0.0.0'
PORT = 9002

def crear_contexto_dtls():
    contexto = SSL.Context(SSL.DTLS_SERVER_METHOD)
    contexto.set_verify(SSL.VERIFY_NONE, lambda *args: True)
    contexto.use_certificate_file('certificado.pem')
    contexto.use_privatekey_file('clave.pem')
    return contexto

def main():
    contexto = crear_contexto_dtls()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))

    print(f'Servidor DTLS escuchando en el puerto {PORT}')

    while True:
        # Esperar datos iniciales del cliente
        datos, addr_cliente = sock.recvfrom(4096)
        print(f'Datagrama recibido de {addr_cliente}, iniciando handshake DTLS...')

        # Crear un socket UDP dedicado para este cliente
        conn_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conn_sock.bind((HOST, PORT))
        conn_sock.connect(addr_cliente)
        conn_sock.settimeout(5)

        # Envolver el socket en una conexión DTLS
        conn_dtls = SSL.Connection(contexto, conn_sock)
        conn_dtls.set_accept_state()

        try:
            # Completar el handshake DTLS
            # El handshake puede requerir varios intentos (WantReadError)
            handshake_completo = False
            for _ in range(10):
                try:
                    conn_dtls.do_handshake()
                    handshake_completo = True
                    break
                except SSL.WantReadError:
                    continue

            if not handshake_completo:
                print('Error: no se pudo completar el handshake')
                conn_sock.close()
                continue

            print(f'Sesión DTLS establecida con {addr_cliente}')

            # Recibir y responder mensajes
            while True:
                try:
                    datos = conn_dtls.read(1024)
                    if not datos:
                        break
                    mensaje = datos.decode('utf-8')
                    print(f'Recibido: {mensaje}')
                    respuesta = f'Servidor recibio: {mensaje}'
                    conn_dtls.write(respuesta.encode('utf-8'))
                except SSL.ZeroReturnError:
                    break
                except SSL.SysCallError:
                    break
                except SSL.Error as e:
                    print(f'Error SSL: {e}')
                    break

        except SSL.Error as e:
            print(f'Error en handshake DTLS: {e}')
        finally:
            try:
                conn_dtls.shutdown()
            except:
                pass
            conn_sock.close()

        print('Sesión DTLS cerrada\n')

if __name__ == '__main__':
    main()