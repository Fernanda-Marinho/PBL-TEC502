import socket
import threading
import json
import time

HOST = "0.0.0.0"
PORT = 8000

lock = threading.Lock()  # Criando um bloqueio para processar um cliente por vez

def handle_client(client_socket, client_address):
    """Lida com um cliente conectado."""
    print(f"🚗 Cliente {client_address} conectado ao server.")

    try:
        while True:
            with lock:  # Trava o acesso até liberar a resposta do cliente
                request = client_socket.recv(1024)
                if not request:
                    break  # Cliente fechou a conexão

                request = request.decode("utf-8").strip()
                
                # 🚨 Tenta decodificar o JSON recebido
                try:
                    data = json.loads(request)
                    bateria = int(data.get("bateria", -1))  # Obtém a bateria e converte para int
                except (json.JSONDecodeError, ValueError, TypeError):
                    response = "ERROR: convert type"
                    client_socket.send(response.encode("utf-8"))
                    continue  # Volta para a próxima iteração sem processar mais

                print(f"📩 Cliente {data.get('placa', 'Desconhecido')} enviou {bateria}% de bateria")

                # Verifica a bateria e define a resposta
                if bateria <= 15:
                    response = f"bateria em {bateria}%, Precisa carregar"
                else:
                    response = f"bateria em {bateria}%, Nao precisa carregar"

                time.sleep(1)  # Simula processamento antes de enviar resposta
                print(f"📤 Servidor enviando resposta para {data.get('placa', 'Desconhecido')}: {response}")
                client_socket.send(response.encode("utf-8"))

    except Exception as e:
        print(f"❌ Erro com {client_address}: {e}")

    finally:
        print(f"🔌 Conexão com {client_address} encerrada")
        client_socket.close()

def run_server():
    """Inicia o servidor e aceita múltiplos clientes sequencialmente."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"🖥️ Servidor ouvindo em {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

run_server()
