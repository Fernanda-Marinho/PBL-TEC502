import socket
import json
import random
import time
import math

def carregar_cars():
    with open("cars.json", "r") as file:
        return json.load(file)

def carregar_postos():
    with open("postos.json", "r") as file:
        return json.load(file)

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371 # Raio da Terra em metros
    return R * c  # Retorna distância em metros

def encontrar_posto_proximo(lat_carro, lon_carro, postos):
    menor_distancia = float('inf')
    posto_proximo = None

    for posto in postos:
        lat_posto = posto["latitude"]
        lon_posto = posto["longitude"]
        distancia = haversine(lat_carro, lon_carro, lat_posto, lon_posto)

        if distancia < menor_distancia:
            menor_distancia = distancia
            posto_proximo = posto

    return posto_proximo["nome"], round(menor_distancia, 2) if posto_proximo else ("Nenhum posto", 0)

def mover_carro(carro):
    """ Simula um movimento aleatório do carro. """
    carro["localizacao"]["latitude"] += random.uniform(-0.0005, 0.0005)
    carro["localizacao"]["longitude"] += random.uniform(-0.0005, 0.0005)

def run_client(carros):
    server_ip = "server"
    server_port = 8000  

    while True:
        for carro in carros:
            mover_carro(carro)  # Atualiza a posição do carro
            carro["bateria"] = max(0, carro["bateria"] - random.randint(1, 10))  # Reduz bateria

            msg = json.dumps({
                "id": carro["id"],
                "placa": carro["placa"],
                "bateria": carro["bateria"],
                "localizacao": carro["localizacao"]
            })

            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((server_ip, server_port))
                print(f"🚗 Cliente {carro['placa']} enviando: {msg}")
                client.send(msg.encode("utf-8"))

                # Recebe resposta do servidor
                response = client.recv(1024).decode("utf-8")
                print(f"📩 Cliente {carro['placa']} recebeu: {response}")

                # Descobre o posto mais próximo
                posto_proximo = encontrar_posto_proximo(
                    carro["localizacao"]["latitude"],
                    carro["localizacao"]["longitude"],
                    postos
                )

                print(f"⛽ Posto mais próximo de {carro['placa']}: {posto_proximo[0]}, {posto_proximo[1]} KMs")

            except Exception as e:
                print(f"Erro no cliente {carro['placa']}: {e}")
            finally:
                client.close()

        time.sleep(5)  # Aguarda antes de repetir o loop para todos os carros

# Carrega carros e postos
carros = carregar_cars()
postos = carregar_postos()
run_client(carros)
