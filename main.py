#!/usr/bin/env python3

from aloha.aloha import Aloha
import fire
import os


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
        "subnets": int(os.getenv("SUBNETS")),
        "nodes_per_subnet": int(os.getenv("NODES_PER_SUBNET")),
        "generate_interval": int(os.getenv("GENERATE_INTERVAL")),
        "head_node_generate": os.getenv("HEAD_NODE_GENERATE", "False") == "True",
        "head_node_coin": os.getenv("HEAD_NODE_COIN", "False") == "True",
        "max_loop": int(os.getenv("MAX_LOOP")),
    }

    final = {**hs_aloha, **kwargs}

    (Aloha(**final).create().start().analyse())


if __name__ == "__main__":
    fire.Fire(main)
