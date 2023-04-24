#!/usr/bin/env python3

from aloha.aloha import Aloha

if __name__ == "__main__":

    aloha_config = {
        "subnets": 2,
        "nodes_per_subnet": 3,
        "generate_interval": -1,
        "head_node_generate": True,
    }
    (Aloha(**aloha_config).create().start().analyse())
