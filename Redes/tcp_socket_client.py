# tcp_client.py
'''
import socket

HOST = "127.0.0.1"
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for msg in ["hola", "sistemas", "distribuidos"]:
        s.sendall(msg.encode())
        data = s.recv(1024)
        print("Eco recibido:", data)

'''
# tls_client.py
import socket, ssl

HOST = "127.0.0.1"
PORT = 12345

context = ssl.create_default_context()
# ssl._create_default_https_context = ssl._create_unverified_context
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        for msg in ["hola", "comunicacion", "segura"]:
            ssock.sendall(msg.encode())
            data = ssock.recv(1024)
            print("Eco recibido:", data)

