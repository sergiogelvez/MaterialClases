# tcp_server.py
'''
import socket

HOST = "127.0.0.1"
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Servidor TCP inseguro escuchando...")
    conn, addr = s.accept()
    with conn:
        print("Conectado por", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Recibido (texto plano):", data)
            conn.sendall(data)
'''

# tls_server.py
import socket, ssl

HOST = "127.0.0.1"
PORT = 12345

# ssl._create_default_https_context = ssl._create_unverified_context
# context = ssl.create_default_context()
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print("Servidor seguro escuchando...")
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        print("Conexión TLS desde", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Recibido (cifrado en tránsito, decifrado aquí):", data)
            conn.sendall(data)
