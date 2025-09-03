import socket

# Crear un socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al servidor
client_socket.connect(("127.0.0.1", 65432))

# Enviar un mensaje
client_socket.sendall(b"Hola desde el cliente")

# Recibir la respuesta
data = client_socket.recv(1024)
print("Cliente recibió:", data.decode())

# Cerrar
client_socket.close()
