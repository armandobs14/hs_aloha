# hs_aloha
This repository is a proposal of implementation for the Hierarchical Slotted ALOHA using python language

![aloha - Time-sequence diagram](aloha.png "Time-sequence diagram")


## Simulation variables
The simulation variables can be changed in [.env](.env) file.

```bash
SUBNETS=2                           # * Quantidade de sub-redes.
NODES_PER_SUBNET=3                  # * Quantidade de nós por sub-rede
GENERATE_INTERVAL=2                 # * Intervalo de geração de pacotes. 
                                    #   -1 Implica que não haverá geração
                                    #   de pacotes durante a execução.
HEAD_NODE_GENERATE=False            # * Define se o HEAD_NODE pode gerar pacotes
HEAD_NODE_COIN=True                 # * Define se o HEAD_NODE tem sorteio com moeda
MAX_LOOP=10                         # * Define o número máximo de loops do experimento
ALOHA_LOG_FILE=/app/data/aloha.log  # * Define local onde será salvo os logs do experimento
```

## How to use
```bash
# run docker compose
docker compose run --rm aloha
```

When executed a file will be created containing the log interactions. This file will be created on the path setted by the ENV `ALOHA_LOG_FILE`
```bash
# info logs
INFO:root:2023-04-24T01:56:38.976460,SUBNET_0, HEAD_NODE, TRANSMITING, TRANSMITING
INFO:root:2023-04-24T01:56:38.976554,SUBNET_0, 1, IDLE, IDLE
INFO:root:2023-04-24T01:56:38.978009,BASE_STATION, None, IDLE, IDLE

# non collisons
DEBUG:root:2023-04-24T01:56:38.978592,SUBNET_0, None, SUCCESS, SUCCESS
DEBUG:root:2023-04-24T01:47:33.643989,BASE_STATION, None, SUCCESS, SUCCESS

# collisions
DEBUG:root:2023-04-24T01:47:33.594998,SUBNET_0, None, NODE_COLLISION, NODE COLLISION
DEBUG:root:2023-04-24T01:47:33.575478,SUBNET_0, None, HEAD_NODE_COLLISION, HEAD_NODE COLLISION
```

Also a resume called `metrics.csv` will be generated containing metrics like:
```
| type         | GENERATING_PACKAGES | HEAD_NODE_COLLISION | IDLE | NODE_COLLISION | SUCCESS | COLLISION | BUSY | THROUGHPUT |
|--------------|---------------------|---------------------|------|----------------|---------|-----------|------|------------|
| network      |                     |                     |      |                |         |           |      |            |
| BASE_STATION | 0.0                 | 0.0                 | 7.0  | 0.0            | 2.0     | 0.0       | 2.0  | 0.222222   |
| SUBNET_0     | 4.0                 | 5.0                 | 2.0  | 1.0            | 1.0     | 6.0       | 7.0  | 0.111111   |
| SUBNET_1     | 4.0                 | 0.0                 | 6.0  | 0.0            | 3.0     | 0.0       | 3.0  | 0.333333   |
```

## Running an experiment
```bash
# create a virtualenv
docker compose run --rm experiment
```

You can change the number of experiments setting the value of `EXPERIMENTS` varible in [compose.yml](compose.yml)
### References:
[T. Oku, T. Kimura and J. Cheng, "Performance Evaluation of Hierarchical Slotted ALOHA for IoT Applications," 2020 IEEE International Conference on Consumer Electronics - Taiwan (ICCE-Taiwan), 2020, pp. 1-2, doi: 10.1109/ICCE-Taiwan49838.2020.9258134.](paper.pdf)
