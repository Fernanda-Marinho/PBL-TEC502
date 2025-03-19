import socket
import time
import json
import random
import os

def load_clients():
    """Carrega os clientes do arquivo JSON ou cria um novo se não existir."""
    file_path = "clients.json"

    # Se o arquivo não existir, cria um novo com dados padrão
    if not os.path.exists(file_path):
        default_clients = [
            {"id": 1, "name": "Alice", "battery": 50},
            {"id": 2, "name": "Bob", "battery": 10},
            {"id": 3, "name": "Charlie", "battery": 80},
            {"id": 4, "name": "David", "battery": 30},
            {"id": 5, "name": "Eve", "battery": 5}
        ]
        with open(file_path, "w") as file:
            json.dump(default_clients, file, indent=4)

    # Agora, lê o arquivo
    with open(file_path, "r") as file:
        return json.load(file)

def run_client(client_data):
    """Simula um cliente enviando a porcentagem de bateria ao servidor."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_ip = "server"
    server_port = 8000

    try:
        client.connect((server_ip, server_port))
        print(f"Cliente {client_data['id']} ({client_data['name']}) conectado ao server.")

        while True:
            # Usa o valor do JSON ou um novo aleatório
            battery = client_data.get("battery", random.randint(1, 100))

            print(f"Cliente {client_data['id']} ({client_data['name']}) enviando: {battery}%")
            client.send(str(battery).encode("utf-8")[:1024])

            response = client.recv(1024).decode("utf-8")
            print(f"Cliente {client_data['id']} ({client_data['name']}) recebeu: {response}")

            # Atualiza a bateria no JSON (simulação)
            client_data["battery"] = random.randint(1, 100)  # Simula variação da bateria

            time.sleep(5)  # Aguarda antes de enviar outra requisição

    except Exception as e:
        print(f"Erro no cliente {client_data['id']} ({client_data['name']}): {e}")

    finally:
        client.close()
        print(f"Cliente {client_data['id']} ({client_data['name']}) conexão fechada")

if __name__ == "__main__":
    clients = load_clients()  # Carrega a lista de clientes do JSON

    for client_data in clients:
        run_client(client_data)  # Executa cada cliente
