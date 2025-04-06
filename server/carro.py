import socket
import json
import time
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger('root')

def carro_main():
    HOST = 'servidor_central'
    PORT = 9000

    # informacoes do carro
    id_carro = os.getenv('PLACA', 'carro_padrao')
    latitude = float(os.getenv('LOCALIZACAO_LAT', '-12.97'))
    longitude = float(os.getenv('LOCALIZACAO_LON', '-38.48'))

    localizacao = {
        "tipo": "carro",
        "id_carro": id_carro,
        "latitude": latitude,
        "longitude": longitude
    }

    logger.info(f"Iniciando carro {id_carro} na localização (Lat={latitude}, Lon={longitude})")

    #tempo para garantir conexao
    time.sleep(5)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(localizacao).encode())

        data = s.recv(4096).decode()
        resposta = json.loads(data)

        logger.info(f"[CARRO {id_carro}] Resposta recebida do servidor: {resposta}")
        
        if 'posto' in resposta and resposta['posto']:
            posto = resposta['posto']
            logger.info(f"[CARRO {id_carro}] Posto mais próximo: {posto['id_posto']} em ({posto['latitude']}, {posto['longitude']})")

        else:
            logger.info(f"[CARRO {id_carro}] Nenhum posto disponível")

if __name__ == '__main__':
    carro_main()
