import socket
import json
import threading

# Dicionário para armazenar dados dos postos registrados
postos_registrados = {}

# Porta em que o servidor central vai escutar
HOST = "0.0.0.0"
PORT = 9000

def handle_posto(conn, addr):
    try:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            return
        
        posto = json.loads(data)
        posto_id = posto["id"]
        postos_registrados[posto_id] = {
            "ip": posto["ip"],
            "port": posto["port"],
            "location": posto["location"]
        }

        print(f"[INFO] Conexão recebida de {addr}")
        print(f"[REGISTRO] Posto {posto_id} registrado de {addr}")
        print(f"          -> Localização: {posto['location']}")
        print(f"          -> IP: {posto['ip']} Porta: {posto['port']}")
    
    except Exception as e:
        print(f"[ERRO] Erro ao registrar posto: {e}")
    
    finally:
        conn.close()

def start_server():
    print(f"[INFO] Servidor Central escutando em {HOST}:{PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_posto, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
