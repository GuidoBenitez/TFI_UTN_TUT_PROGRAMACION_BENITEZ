import socket
import threading
import time
import random

def atender_instrumento(puerto, modelo):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", puerto))
    server.listen(1)
    print(f"[{modelo}] Instrumento virtual escuchando en 127.0.0.1:{puerto}")
    
    while True:
        try:
            conn, addr = server.accept()
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                comando = data.decode("ascii").strip()
                
                respuesta = procesar_comando(modelo, comando)
                if respuesta is not None:
                    conn.sendall((respuesta + "\n").encode("ascii"))
            conn.close()
        except Exception:
            break

def procesar_comando(modelo, cmd):
    cmd_upper = cmd.upper()
    if "*IDN?" in cmd_upper:
        if modelo == "ADS3202":
            return "OWON, ADS3202,25470803,V1.2.0"
        else:
            return "OWON, XDM1041,25470803,V4.4.0,3"
            
    if "MEASUREMENT" in cmd_upper or "FREQ" in cmd_upper or "PKPK" in cmd_upper or "CYCRMS" in cmd_upper:
        # Simula el "temblor" de las mediciones reales con leve variación aleatoria
        if "FREQ" in cmd_upper:
            val = 1000.0 + random.uniform(-2.0, 2.0) if "CH1" in cmd_upper else 2500.0 + random.uniform(-3.0, 3.0)
            return f"{val:12.6E}"
        elif "PKPK" in cmd_upper:
            val = 2.0 + random.uniform(-0.01, 0.01) if "CH1" in cmd_upper else 0.8 + random.uniform(-0.005, 0.005)
            return f"{val:12.6E}"
        elif "CYCRMS" in cmd_upper:
            val = 0.7071 + random.uniform(-0.001, 0.001) if "CH1" in cmd_upper else 0.2828 + random.uniform(-0.001, 0.001)
            return f"{val:12.6E}"
            
    return "ERROR: comando desconocido"

if __name__ == "__main__":
    t1 = threading.Thread(target=atender_instrumento, args=(5555, "ADS3202"), daemon=True)
    t2 = threading.Thread(target=atender_instrumento, args=(5556, "XDM1041"), daemon=True)
    
    t1.start()
    t2.start()
    
    print("Instrumentos virtuales activos. Para apagar presione Ctrl+C.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nInstrumentos apagados.")
