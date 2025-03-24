import socket
import time
import random 
import json

# pegar o range de distancias 
def range_distance(start, stop, step):
    while start < stop:
        yield round(start, 10)  
        start += step

# escolhe um valor float aleatorio entre 1 e 500 (pulando de 0,3 em 0,3)
def set_distance():
    list_distance = []
    for i in range_distance(1,500,0.3): #mudar aq se necessario 
        list_distance.append(i)
    return random.choice(list_distance)

client_id = 0 
def create_client(id):
    return {'id': id, 
            'battery': random.randint(1,100),
            'localization': set_distance()  
    }

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_ip = "server"  
    server_port = 8000  
    
    client.connect((server_ip, server_port))

    car = create_client(1)

    while True:
        car['battery'] = random.randint(1, 100)
        msg = json.dumps(car)
        #battery = random.randint(1,100)
        #msg = str(battery)
        print(f"Enviado: {msg}")
        
        client.send(msg.encode("utf-8")[:1024])

        response = client.recv(1024)
        response = response.decode("utf-8")

        if response.lower() == "closed":
            break
        
        print(f"Resposta: {response}")
        time.sleep(5)

    client.close()
    print("Connection to server closed")

run_client()

