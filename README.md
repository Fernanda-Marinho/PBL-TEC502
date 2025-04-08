# 🔌 Sistema Distribuído de Recarga de Veículos Elétricos

## 💡 Descrição do Problema

Este projeto simula um sistema distribuído para recarga de veículos elétricos, composto por um **servidor central**, **postos de recarga** e **carros**, todos implementados como contêineres Docker. O objetivo é gerenciar múltiplos carros tentando acessar postos simultaneamente, simulando concorrência, controle de fila, e decisão inteligente do veículo com base em localização e espera.

## 🎯 Objetivos

- Criar um sistema escalável com múltiplos postos e carros em contêineres isolados.
- Utilizar TCP para comunicação entre os componentes.
- Implementar controle de concorrência com filas e tempo de carregamento nos postos.
- Adicionar inteligência na escolha de postos pelos veículos.
- Simular e testar localmente e em rede real.
- Exibir informações do sistema em tempo real em um dashboard.

## 🛠️ Tecnologias Utilizadas

- Python 3
- Sockets TCP
- `threading` e `queue` para concorrência
- Docker e Docker Compose
- JSON para troca de dados
- (Em desenvolvimento) Frontend para dashboard

## 📁 Estrutura do Projeto

```
PBL-TEC502-main/
├── servidor/
│   └── servidor.py
├── postos/
│   ├── posto.py
│   └── Dockerfile
├── carros/
│   ├── carro.py
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```


## 🔧 Funcionamento

- **Servidor Central** (`servidor/servidor.py`)
  - Mantém registro dos postos de recarga e suas localizações.
  - Responde a requisições de carros com a lista de postos disponíveis.
  - Recebe atualizações periódicas dos postos.

- **Posto de Recarga** (`postos/posto.py`)
  - Lê as configurações via variáveis de ambiente (porta, localização, tempo de carga).
  - Registra-se no servidor central a cada 10 segundos.
  - Gerencia uma fila de carros conectados e simula o processo de carregamento com `sleep`.

- **Carro** (`carros/carro.py`)
  - Solicita a lista de postos ao servidor.
  - Seleciona um posto com base na menor distância e na menor fila.
  - Conecta ao posto e espera na fila para carregar.
 
🔌 Comunicação entre Processos
A arquitetura segue o modelo cliente-servidor, com comunicação entre processos feita via sockets TCP. As mensagens são trafegadas no formato JSON, que permite estrutura flexível, leitura fácil e compatibilidade com múltiplas linguagens.
📡 Protocolo Utilizado: TCP
O protocolo TCP (Transmission Control Protocol) foi escolhido por garantir:
  - Entrega confiável das mensagens.
  - Ordem correta dos pacotes.
  - Controle de congestionamento e retransmissão automática em caso de falha.
  - Facilidade de uso com bibliotecas padrão em Python (socket).
  - Como o sistema lida com fila de espera e controle de tempo, a confiabilidade do TCP é essencial para manter a integridade dos dados e da sincronização entre os componentes.

🔄 Fluxo da Comunicação

Posto de recarga → Servidor Central
 Iniciador: Posto
 Descrição: A cada 10 segundos, o posto envia uma mensagem com seu status (disponível/ocupado), tamanho da fila e tempo estimado de recarga.


Carro → Servidor Central
 Iniciador: Carro
 Descrição: Ao iniciar, o carro envia uma solicitação para obter a lista de postos disponíveis.


Servidor Central → Carro
 Resposta: Envia uma lista de postos com IP, porta e status (tamanho da fila, tempo estimado).


Carro → Posto de recarga
 Iniciador: Carro
 Descrição: O carro seleciona o melhor posto (com menor fila ou mais próximo) e envia uma solicitação de reserva.


Posto de recarga → Carro
 Resposta: O posto responde com a confirmação da reserva e a posição do carro na fila.



📤 Mensagens JSON e seus Tipos
Todas as mensagens são objetos JSON. Abaixo estão os principais tipos:
➤ Posto → Servidor Central
{
  "tipo": "registro_posto",
  "id": "posto01",
  "ip": "172.18.0.2",
  "porta": 9001,
  "status": "disponível",
  "fila": 2,
  "tempo_estimado": 30
}


➤ Carro → Servidor Central
{
  "tipo": "solicita_postos",
  "placa": "ABC-1234"
}


➤ Servidor Central → Carro
{
  "tipo": "resposta_postos",
  "postos": [
    {
      "id": "posto01",
      "ip": "172.18.0.2",
      "porta": 9001,
      "fila": 1
    }
  ]
}


➤ Carro → Posto
{
  "tipo": "reserva",
  "placa": "ABC-1234"
}


➤ Posto → Carro
{
  "tipo": "resposta_reserva",
  "status": "em_espera",
  "posicao_na_fila": 2
}

⚙️ Execução do Projeto

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/(https://github.com/Fernanda-Marinho/PBL-TEC502/tree/main)/PBL-TEC502-main.git
   cd PBL-TEC502-main
   ```

2. **Executar com Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Exemplo de logs**:
   ```bash
   docker logs -f servidor-central
   docker logs -f posto1
   docker logs -f carro1
   ```
💡 Interface Remota
Não foi utilizada uma API remota tradicional (como REST/HTTP).
Em vez disso, a comunicação entre os serviços foi implementada via
sockets TCP, trocando mensagens no formato de strings (JSON ou texto simples).
Formato das mensagens
As mensagens entre os agentes seguem um padrão bem direto, usando strings com campos separados por ; , como:
Carro * Servidor:


LATITUDE;LONGITUDE

Exemplo real:


-12.9711;-38.5108

Servidor * Carro (resposta):


id_posto;latitude;longitude

Servidor * Posto:
Apenas conecta, e o posto responde com:


id;latitude;longitude;disponivel

Exemplo de fluxo de mensagens


⦁	Carro envia sua localização * Servidor
⦁	Servidor se conecta aos postos → coleta dados
⦁	Postos respondem com localização e disponibilidade
⦁	Servidor escolhe o melhor posto
⦁	Servidor responde ao carro com os dados do posto


Diagrama de sequência (texto simples)



Carro	Servidor		Posto 1	Posto 2
|	|	|	|	
|-- localização ⟶	|	|
|	|-- conecta ⟶		|
|	|* dados ---	|	
|	|-- conecta	*|
|	|* dados	|
|* resposta com posto mais próximo --|


🧪 Simulação

O sistema pode ser testado de duas formas:

- Modo Local (Simulação):
  - Todos os serviços são executados em contêineres na mesma máquina.
- Modo Distribuído (Rede Local):
  - Contêineres podem rodar em dispositivos diferentes conectados à mesma rede.
  - Para isso, ajuste o `docker-compose.yml` ou as variáveis `HOST` nos scripts.



