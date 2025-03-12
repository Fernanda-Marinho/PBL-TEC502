import socket
import time


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_ip = "server"  
    server_port = 8000  
    
    client.connect((server_ip, server_port))

    while True:
        #msg = input("Message: ")
        msg = "hello!"
        client.send(msg.encode("utf-8")[:1024])

        response = client.recv(1024)
        response = response.decode("utf-8")

        if response.lower() == "closed":
            break
        
        print(f"Received: {response}")
        time.sleep(5)

    client.close()
    print("Connection to server closed")

run_client()

