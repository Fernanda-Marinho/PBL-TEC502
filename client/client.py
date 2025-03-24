import socket
import json
import random
import time
from haversine import calcular_distancia

def carregar_cars():
    with open("cars.json", "r") as file:
        return json.load(file)

def carregar_postos():
    with open("postos.json", "r") as file:
        return json.load(file)

def encontrar_posto_proximo(car_lat, car_lon, postos):
    menor_distancia = float("inf")
    posto_mais_proximo = None

    for posto in postos:
        distancia = calcular_distancia(car_lat, car_lon, posto["latitude"], posto["longitude"])
        if distancia < menor_distancia:
            menor_distancia = distancia
            posto_mais_proximo = posto

    return posto_mais_proximo, menor_distancia

def run_client(car):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "server"
    server_port = 8000  # Porta fixa para os postos
    client.connect((server_ip, server_port))

    print(f"{car['placa']} conectado ao server.")

    while True:
        car['bateria'] = max(0, car["bateria"]- random.randint(1, 10))
        msg = json.dumps({
            "id": car["id"],
            "placa": car["placa"],
            "bateria": car["bateria"],
            "localizacao": car["localizacao"]
        })

        print(f"Cliente {car['placa']} enviando: {msg}")
        client.send(msg.encode("utf-8"))

        # Recebe resposta do servidor
        response = client.recv(1024).decode("utf-8")
        print(f"Cliente {car['placa']} recebeu: {response}")

        print(encontrar_posto_proximo(carro["localizacao"]["latitude"], carro["localizacao"]["longitude"], postos))

        # Aguarda antes de enviar a próxima atualização
        time.sleep(5)

    client.close()

# Carrega a lista de carros e inicia cada cliente em uma thread separada
carros = carregar_cars()
postos = carregar_postos()
for carro in carros:
    run_client(carro)