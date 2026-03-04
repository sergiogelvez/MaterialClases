from OpenSSL import crypto

# Generar clave privada RSA de 2048 bits
clave = crypto.PKey()
clave.generate_key(crypto.TYPE_RSA, 2048)

# Crear certificado autofirmado
cert = crypto.X509()
cert.get_subject().C = "CO"
cert.get_subject().ST = "Santander"
cert.get_subject().L = "Bucaramanga"
cert.get_subject().O = "Universidad"
cert.get_subject().CN = "localhost"
cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # válido por 1 año
cert.set_issuer(cert.get_subject())  # autofirmado
cert.set_pubkey(clave)
cert.sign(clave, 'sha256')

# Guardar archivos
with open('certificado.pem', 'wb') as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

with open('clave.pem', 'wb') as f:
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, clave))

print('Archivos generados:')
print('  certificado.pem — certificado público (se comparte con los clientes)')
print('  clave.pem       — clave privada (nunca se comparte)')