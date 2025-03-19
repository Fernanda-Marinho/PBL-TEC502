import socket
import time
import random 
import threading

server_ip = "server"  
server_port = 8000

def run_client(client_id):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, server_port))
        print(f"Cliente {client_id} conectado ao server.")

        while True:            
            battery = random.randint(1,100)
            msg = str(battery)

            print(f"Client {client_id} bateria: {msg}%")
        
            client.send(msg.encode("utf-8")) # nao precisa do 1024, o encode ja mantem o formato

            response = client.recv(1024).decode("utf-8")

            if response.lower() == "closed":
                print(f"Cliente {client_id} encerrado pelo servidor.")
                break
        
            print(f"Cliente {client_id} recebeu: {response}")
            time.sleep(5)

        client.close()
    except Exception as e:
        print(f"Erro no Cliente {client_id}: {e}")

def start_clients(n):
    threads = []
    for i in range(n):
        thread = threading.Thread(target=run_client, args=(i+1,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    num_clients = 5  # Número de clientes a serem simulados
    start_clients(num_clients)

