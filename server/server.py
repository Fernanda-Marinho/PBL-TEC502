import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 8000

lock = threading.Lock()  # Criando um bloqueio para processar um cliente por vez

def handle_client(client_socket, client_address):
    """Lida com um cliente conectado."""
    print(f"Cliente {client_address} conectado ao server.")

    try:
        while True:
            with lock:  # Trava o acesso até liberar a resposta do cliente
                request = client_socket.recv(1024)
                if not request:
                    break  # Cliente fechou a conexão

                request = request.decode("utf-8").strip()
                print(f"Cliente {client_address} enviou: {request}%")

                if request.lower() == "close":
                    client_socket.send("closed".encode("utf-8"))
                    break

                try:
                    battery = int(request)
                    if battery <= 15:
                        response = "Need recharge"
                    else:
                        response = "Do not need recharge"
                except ValueError:
                    response = "ERROR: convert type"

                time.sleep(3)  # ⏳ Espera 3 segundos antes de responder
                print(f"Servidor enviando resposta para {client_address}: {response}")
                client_socket.send(response.encode("utf-8"))

    except Exception as e:
        print(f"Erro com {client_address}: {e}")

    finally:
        print(f"Conexão com {client_address} encerrada")
        client_socket.close()

def run_server():
    """Inicia o servidor e aceita múltiplos clientes sequencialmente."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor ouvindo em {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

run_server()
