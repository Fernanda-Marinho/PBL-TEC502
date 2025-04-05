import socket
import json
import logging
import sys
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger("root")

# Função principal
def main():
    id_posto = os.environ.get("ID_POSTO", "posto_padrao")
    latitude = float(os.environ.get("LATITUDE", -12.97))
    longitude = float(os.environ.get("LONGITUDE", -38.48))
    servidor_central = os.environ.get("SERVIDOR_CENTRAL", "servidor_central")
    porta = int(os.environ.get("PORTA_SERVIDOR", 9000))

    logger.info(f"Inicializando Posto {id_posto} (ID: {id_posto})")
    logger.info(f"Localização: Lat={latitude}, Long={longitude}")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((servidor_central, porta))

            mensagem = {
                "tipo": "posto",
                "id_posto": id_posto,
                "latitude": latitude,
                "longitude": longitude
            }

            sock.sendall(json.dumps(mensagem).encode('utf-8'))

            resposta = sock.recv(4096).decode('utf-8')
            try:
                resposta_json = json.loads(resposta)
                logger.info(f"Resposta do servidor: {resposta_json.get('mensagem', 'ok')}")
            except json.JSONDecodeError:
                logger.info(f"Resposta do servidor: {resposta}")

    except Exception as e:
        logger.error(f"[POSTO {id_posto}] Erro ao se comunicar com o servidor: {e}")

    logger.info(f" Posto de recarga rodando em 0.0.0.0:8000")

if __name__ == "__main__":
    main()
