import socket

class Instrumento:
    """Clase para comunicarse con el instrumento virtual mediante sockets TCP[cite: 10]."""
    def __init__(self, direccion="127.0.0.1", puerto=5555):
        self.direccion = direccion
        self.puerto = puerto
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.direccion, self.puerto))
        
    def enviar(self, comando):
        """Manda una orden y no espera respuesta (ENVIAR)[cite: 10]."""
        mensaje = comando.strip() + "\n"
        self.socket.sendall(mensaje.encode("ascii"))
        
    def preguntar(self, comando):
        """Manda una consulta y devuelve la respuesta del instrumento (QUERY)[cite: 10]."""
        mensaje = comando.strip() + "\n"
        self.socket.sendall(mensaje.encode("ascii"))
        
        buffer = bytearray()
        while True:
            chunk = self.socket.recv(1)
            if not chunk or chunk == b"\n":
                break
            buffer.extend(chunk)
        return buffer.decode("ascii").strip()
        
    def cerrar(self):
        """Cierra la conexión con el instrumento[cite: 10]."""
        self.socket.close()

if __name__ == "__main__":
    print("Para probar el cliente, asegúrese de tener corriendo 'python3 instrumento_virtual.py'[cite: 4, 10].")
    assert hasattr(Instrumento, "enviar")
    assert hasattr(Instrumento, "preguntar")
    assert hasattr(Instrumento, "cerrar")
    print("pruebas 05_cliente estructura OK")
