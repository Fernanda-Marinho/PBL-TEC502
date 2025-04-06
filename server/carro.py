import socket
import json
import time
import logging
import os
import random

logging.basicConfig(level=logging.INFO, format='%(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger('root')

def carro_main():
    HOST = 'servidor_central'
    PORT = 9000

    id_carro = os.getenv('PLACA', 'carro_padrao')
    latitude = float(os.getenv('LOCALIZACAO_LAT', '-12.97'))
    longitude = float(os.getenv('LOCALIZACAO_LON', '-38.48'))

    logger.info(f"Iniciando carro {id_carro} na localização inicial (Lat={latitude}, Lon={longitude})")

    time.sleep(5)  #aguarda o servidor subir

    while True:
        localizacao = {
            "tipo": "carro",
            "id_carro": id_carro,
            "latitude": latitude,
            "longitude": longitude
        }

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(json.dumps(localizacao).encode())

                data = s.recv(4096).decode()
                resposta = json.loads(data)

                logger.info(f"[CARRO {id_carro}] Resposta recebida do servidor: {resposta}")
                time.sleep(1)

                if 'posto' in resposta and resposta['posto']:
                    posto = resposta['posto']
                    logger.info(f"[CARRO {id_carro}] Posto mais próximo: {posto['id_posto']} em ({posto['latitude']}, {posto['longitude']})")
                    time.sleep(5)
                else:
                    logger.info(f"[CARRO {id_carro}] Nenhum posto disponível")
                    time.sleep(5)
        except Exception as e:
            logger.error(f"[CARRO {id_carro}] Erro ao se conectar ao servidor: {e}")

        #simula movimento aleatório
        latitude += random.uniform(-0.0005, 0.0005)
        longitude += random.uniform(-0.0005, 0.0005)

        time.sleep(5)  #aguarda antes de enviar nova localização

if __name__ == '__main__':
    carro_main()
