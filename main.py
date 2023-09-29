#!/usr/bin/env python3

from aloha.aloha import Aloha
import fire

def main(*args, **kwargs):
    # s_aloha = {
    #     "subnets": 1,
    #     "nodes_per_subnet": 3,
    #     "generate_interval": -1,
    #     "head_node_generate": False,
    #     "head_node_coin": False,
    #     "max_loop": -1,
    # }

    # Hierarchical Slotted Aloha
    hs_aloha = {
        "subnets": 2,
        "nodes_per_subnet": 3,
        "generate_interval": 2,
        "head_node_generate": False,
        "head_node_coin": True,
        "max_loop": 100,
    }
    
    final = {
        **hs_aloha,
        **kwargs
    }

    (Aloha(**final).create().start().analyse())

if __name__ == "__main__":
    fire.Fire(main)
