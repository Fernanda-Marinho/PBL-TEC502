import socket
import json
import threading
import os
import time

# Configurações do posto (via variáveis de ambiente no Docker)
POSTO_ID = os.environ.get("POSTO_ID")
NOME = os.environ.get("NOME")
LATITUDE = os.environ.get("LATITUDE")
LONGITUDE = os.environ.get("LONGITUDE")
PORTA_LOCAL = 8000

print(f"[INFO] Inicializando {NOME} (ID: {POSTO_ID})")
print(f"[INFO] Localização: Lat={LATITUDE}, Long={LONGITUDE}")

# Configuração do servidor central
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = 9000

# Fila de espera dos carros
fila_de_espera = []

# -------------------------
# Função de registro no servidor central
# -------------------------
def registrar_no_servidor_central():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_HOST, SERVER_PORT))
                dados_registro = {
                    "id": POSTO_ID,
                    "ip": socket.gethostbyname(socket.gethostname()),
                    "port": PORTA_LOCAL,
                    "location": {"lat": LATITUDE, "lon": LONGITUDE}
                }
                s.send(json.dumps(dados_registro).encode("utf-8"))
                print("[INFO] Posto registrado com sucesso no servidor central")
        except Exception as e:
            print(f"[ERRO] Falha ao registrar no servidor central: {e}")
        time.sleep(10)  # Envia a cada 10 segundos

# -------------------------
# Função para processar conexões de carros
# -------------------------
def handle_client(conn, addr):
    global fila_de_espera
    try:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            return

        carro = json.loads(data)
        print(f"Carro {carro['placa']} conectado ao posto!")

        fila_de_espera.append(carro["placa"])

        resposta = {
            "mensagem": "Reserva recebida",
            "posicao_fila": len(fila_de_espera)
        }
        conn.send(json.dumps(resposta).encode("utf-8"))

    except Exception as e:
        print(f"[ERRO] Erro ao processar conexão: {e}")
    finally:
        conn.close()

# -------------------------
# Servidor TCP do posto
# -------------------------
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORTA_LOCAL))
    server.listen(5)
    print(f" Posto de recarga rodando em 0.0.0.0:{PORTA_LOCAL}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# -------------------------
# Execução principal
# -------------------------
if __name__ == "__main__":
    threading.Thread(target=registrar_no_servidor_central, daemon=True).start()
    start_server()
