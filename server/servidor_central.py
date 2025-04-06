import socket
import json
import threading
import logging
import time
from queue import Queue

#configuracao login
logging.basicConfig(level=logging.DEBUG, format='%(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger("servidor_central")

postos_de_recarga = []
filas_por_posto = {}  #fila real
carros_em_fila_por_posto = {}  #controle para evitar que o msm carro va para a fila duas vezes


#funcao para calcular distância
def calcular_distancia(lat1, lon1, lat2, lon2):
    return ((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5


#exibe a fila de um posto específico
def exibir_fila_posto(id_posto):
    fila = filas_por_posto.get(id_posto)
    if fila:
        conteudo = list(fila.queue)
        logger.info(f"📋 Fila do posto {id_posto}: {conteudo}")
        time.sleep(5)
    else:
        logger.info(f"[INFO] Nenhuma fila encontrada para o posto {id_posto}")
        time.sleep(5)


#exibe todas as filas de todos os postos
def exibir_todas_filas():
    logger.info("📊 Todas as filas de postos:")
    for id_posto, fila in filas_por_posto.items():
        conteudo = list(fila.queue)
        logger.info(f"  Posto {id_posto}: {conteudo}")
        time.sleep(5)
    logger.info("-" * 40)


#lidar com conexao (carro ou posto)
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

            if id_posto not in [p["id_posto"] for p in postos_de_recarga]:
                postos_de_recarga.append({
                    "id_posto": id_posto,
                    "latitude": latitude,
                    "longitude": longitude
                })
                filas_por_posto[id_posto] = Queue()
                carros_em_fila_por_posto[id_posto] = set()
                logger.info(f"[POSTO] Registrado: {id_posto} em ({latitude}, {longitude})")
                time.sleep(5)

            conexao.sendall(json.dumps({"mensagem": "Posto registrado com sucesso"}).encode('utf-8'))

        elif tipo == "carro":
            id_carro = mensagem.get("id_carro")
            latitude = mensagem.get("latitude")
            longitude = mensagem.get("longitude")
            logger.info(f"[CARRO] Requisição de {id_carro} em ({latitude}, {longitude})")
            time.sleep(5)

            if not postos_de_recarga:
                resposta = {"mensagem": "Nenhum posto disponível no momento."}
            else:
                posto_mais_proximo = min(
                    postos_de_recarga,
                    key=lambda posto: calcular_distancia(latitude, longitude, posto["latitude"], posto["longitude"])
                )
                id_posto = posto_mais_proximo["id_posto"]

                fila = filas_por_posto.get(id_posto)
                carros_em_fila = carros_em_fila_por_posto.get(id_posto)

                if id_carro in carros_em_fila:
                    logger.info(f"[FILA] Carro {id_carro} já está na fila do posto {id_posto}, ignorando novo pedido.")
                    time.sleep(5)
                    resposta = {
                        "mensagem": "Você já está na fila deste posto.",
                        "posto": posto_mais_proximo
                    }
                else:
                    fila.put(id_carro)
                    carros_em_fila.add(id_carro)
                    posicao_na_fila = fila.qsize()
                    logger.info(f"[FILA] Carro {id_carro} adicionado à fila do posto {id_posto} (posição {posicao_na_fila})")
                    time.sleep(5)

                    exibir_fila_posto(id_posto)
                    time.sleep(5)

                    exibir_todas_filas()

                    resposta = {
                        "mensagem": "Você foi adicionado à fila.",
                        "posto": posto_mais_proximo,
                        "posicao_na_fila": posicao_na_fila
                    }

            conexao.sendall(json.dumps(resposta).encode('utf-8'))

        else:
            logger.warning(f"[AVISO] Mensagem desconhecida de {endereco}: {mensagem}")
            conexao.sendall(json.dumps({"mensagem": "Formato de mensagem não reconhecido."}).encode('utf-8'))

    except Exception as e:
        logger.error(f"[ERRO] Falha ao lidar com cliente {endereco}: {e}")
    finally:
        conexao.close()

def main():
    host = '0.0.0.0'
    porta = 9000
    logger.debug("Servidor iniciado - com verificação de duplicatas")
    logger.info(f"Servidor Central escutando em {host}:{porta}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((host, porta))
        servidor.listen()

        while True:
            conexao, endereco = servidor.accept()
            threading.Thread(target=lidar_com_cliente, args=(conexao, endereco), daemon=True).start()
            time.sleep(5) #para que os logs aparecam de forma mais lenta


if __name__ == "__main__":
    main()
