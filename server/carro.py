import socket
import json
import time
import logging
import os
import random

SALDO_MINIMO = 50
SALDO_MAXIMO = 300

CONSUMO_MINIMO = 20
CONSUMO_MAXIMO = 50

TEMPO_RECARGA_MINIMO = 2
TEMPO_RECARGA_MAXIMO = 5

VALOR_RECARGA = 50

NIVEL_CRITICO = 30

logging.basicConfig(level=logging.INFO, format='%(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger('root')

def carro_main():
    HOST = 'servidor_central'
    PORT = 9000

    id_carro = os.getenv('PLACA', 'carro_padrao')
    latitude = float(os.getenv('LOCALIZACAO_LAT', '-12.97'))
    longitude = float(os.getenv('LOCALIZACAO_LON', '-38.48'))

    nivel_bateria = 100  
    saldo = random.randint(SALDO_MINIMO, SALDO_MAXIMO) 

    logger.info(f"Iniciando carro {id_carro} na localização inicial (Lat={latitude}, Lon={longitude})")

    time.sleep(5)  #aguarda o servidor subir

    while True:
        # localizacao = {
        #     "tipo": "carro",
        #     "id_carro": id_carro,
        #     "latitude": latitude,
        #     "longitude": longitude
        # }

        consumo = random.randint(CONSUMO_MINIMO, CONSUMO_MAXIMO)
        nivel_bateria -= consumo
        nivel_bateria = max(nivel_bateria, 0)

        logger.info(f"[CARRO {id_carro}] Bateria: {nivel_bateria}% | Saldo: R${saldo}")

        if nivel_bateria <= NIVEL_CRITICO:
            if saldo < VALOR_RECARGA:
                logger.warning(f"[CARRO {id_carro}] Saldo insuficiente para recarregar. Parando requisições.")
                break  

            logger.info(f"[CARRO {id_carro}] Bateria baixa e saldo suficiente. Procurando ponto de recarga...")

            mensagem = {
                "tipo": "carro",
                "id_carro": id_carro,
                "latitude": latitude,
                "longitude": longitude,
                "bateria": nivel_bateria,
                "saldo": saldo
            }

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(json.dumps(mensagem).encode())
                    #s.sendall(json.dumps(localizacao).encode())

                    data = s.recv(4096).decode()
                    resposta = json.loads(data)

                    logger.info(f"[CARRO {id_carro}] Resposta recebida do servidor: {resposta}")
                    time.sleep(1)

                    if 'posto' in resposta and resposta['posto']:
                        posto = resposta['posto']
                        logger.info(f"[CARRO {id_carro}] Posto mais próximo: {posto['id_posto']} em ({posto['latitude']}, {posto['longitude']})")
                        #time.sleep(5)
                        tempo_recarga = random.randint(TEMPO_RECARGA_MINIMO, TEMPO_RECARGA_MAXIMO)
                        logger.info(f"[CARRO {id_carro}] Recarregando por {tempo_recarga} segundos...")
                        time.sleep(tempo_recarga)
                        nivel_bateria = 100
                        saldo -= VALOR_RECARGA 
                        logger.info(f"[CARRO {id_carro}] Recarga concluída. Bateria cheia! Saldo restante: R${saldo}")
                    else:
                        logger.info(f"[CARRO {id_carro}] Nenhum posto disponível")
                        time.sleep(5)
            except Exception as e:
                logger.error(f"[CARRO {id_carro}] Erro ao se conectar ao servidor: {e}")
        else:
            logger.info(f"[CARRO {id_carro}] Bateria suficiente. Nenhuma requisição enviada.")

        #simula movimento aleatório
        latitude += random.uniform(-0.0005, 0.0005)
        longitude += random.uniform(-0.0005, 0.0005)

        time.sleep(5)  #aguarda antes de enviar nova localização

if __name__ == '__main__':
    carro_main()
