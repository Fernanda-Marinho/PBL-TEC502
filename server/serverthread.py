import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    while True:
        try:
            request = client_socket.recv(1024).decode("utf-8") 
            if not request:
                break 

            print(f"Received from {client_address}: {request}")

            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break

            response = "accepted".encode("utf-8")
            client_socket.send(response)  
        except:
            break

    client_socket.close()
    print(f"Connection to {client_address} closed")

def run_server():
    server_ip = "127.0.0.1"
    port1 = 8000
    port2 = 8001

    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server1.bind((server_ip, port1))
    server2.bind((server_ip, port2))

    server1.listen(5)
    server2.listen(5)

    print(f"Listening on {server_ip}:{port1} and {server_ip}:{port2}")

    while True:
        client_socket1, client_address1 = server1.accept()
        client_socket2, client_address2 = server2.accept()

        threading.Thread(target=handle_client, args=(client_socket1, client_address1)).start()
        threading.Thread(target=handle_client, args=(client_socket2, client_address2)).start()

run_server()
