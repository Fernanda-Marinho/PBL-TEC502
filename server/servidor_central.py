import socket
import json
import threading
import logging

#config login
logging.basicConfig(level=logging.DEBUG, format='%(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger("servidor_central")

#lista para armazenar os postos
postos_de_recarga = []

#funcao para calcular a distncia entre dois pontos
def calcular_distancia(lat1, lon1, lat2, lon2):
    return ((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5

#funcao para lidar com posto ou carro
def lidar_com_cliente(conexao, endereco):
    try:
        dados = conexao.recv(4096).decode('utf-8')
        if not dados:
            return

        try:
            mensagem = json.loads(dados)
        except json.JSONDecodeError:
            logger.warning(f"[ERRO] Mensagem inválida de {endereco}: {dados}")
            conexao.sendall("Mensagem inválida".encode('utf-8'))
            return

        tipo = mensagem.get("tipo")
        
        if tipo == "posto":
            id_posto = mensagem.get("id_posto")
            latitude = mensagem.get("latitude")
            longitude = mensagem.get("longitude")
            postos_de_recarga.append({
                "id_posto": id_posto,
                "latitude": latitude,
                "longitude": longitude
            })
            logger.info(f"[POSTO] Registrado: {id_posto} em ({latitude}, {longitude})")
            conexao.sendall(json.dumps({"mensagem": "Posto registrado com sucesso"}).encode('utf-8'))

        elif tipo == "carro":
            id_carro = mensagem.get("id_carro")
            latitude = mensagem.get("latitude")
            longitude = mensagem.get("longitude")
            logger.info(f"[CARRO] Requisição de {id_carro} em ({latitude}, {longitude})")

            if not postos_de_recarga:
                resposta = {"mensagem": "Nenhum posto disponível no momento."}
            else:
                # Encontrar o posto mais próximo
                posto_mais_proximo = min(
                    postos_de_recarga,
                    key=lambda posto: calcular_distancia(latitude, longitude, posto["latitude"], posto["longitude"])
                )
                resposta = {
                    "mensagem": "Posto mais próximo encontrado",
                    "posto": posto_mais_proximo
                }

            conexao.sendall(json.dumps(resposta).encode('utf-8'))

        else:
            logger.warning(f"[AVISO] Mensagem desconhecida de {endereco}: {mensagem}")
            conexao.sendall(json.dumps({"mensagem": "Formato de mensagem nao reconhecido."}).encode('utf-8'))

    except Exception as e:
        logger.error(f"[ERRO] Falha ao lidar com cliente {endereco}: {e}")
    finally:
        conexao.close()

# Função principal do servidor
def main():
    host = '0.0.0.0'
    porta = 9000
    logger.debug("Servidor iniciado - versão atual")
    logger.info(f"Servidor Central escutando em {host}:{porta}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((host, porta))
        servidor.listen()

        while True:
            conexao, endereco = servidor.accept()
            threading.Thread(target=lidar_com_cliente, args=(conexao, endereco), daemon=True).start()

if __name__ == "__main__":
    main()
