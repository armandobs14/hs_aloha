#!/usr/bin/env python3

from aloha.aloha import Aloha

if __name__ == "__main__":
    s_aloha = {
        "subnets": 2,
        "nodes_per_subnet": 3,
        "generate_interval": -1,
        "head_node_generate": False,
        "head_node_coin": False,
        "max_loop": -1,
    }

    # Hierarchical Slotted Aloha
    hs_aloha = {
        "subnets": 2,
        "nodes_per_subnet": 3,
        "generate_interval": 10,
        "head_node_generate": True,
        "head_node_coin": True,
        "max_loop": -1,
    }

    (Aloha(**s_aloha).create().start().analyse())
