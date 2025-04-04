# Dockerfile do Posto de Recarga

FROM python:3.10-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia o script do posto para o container
COPY posto.py .

# Expõe a porta usada pelo posto
EXPOSE 8000

# Comando padrão para rodar o script
CMD ["python", "posto.py"]
