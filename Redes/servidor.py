import socket

# Crear un socket TCP (IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociar el socket a una dirección y puerto
server_socket.bind(("127.0.0.1", 65432))

# Ponerlo en modo escucha
server_socket.listen()

print("Servidor esperando conexión en 127.0.0.1:65432...")

# Aceptar una conexión
conn, addr = server_socket.accept()
print(f"Conectado con {addr}")

# Recibir datos
data = conn.recv(1024)
print("Servidor recibió:", data.decode())

# Responder
conn.sendall(b"Hola desde el servidor")

# Cerrar
conn.close()
server_socket.close()
