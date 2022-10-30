#!/usr/bin/env python3

from aloha.aloha import Aloha
import time
import os

# Environment variables
# os.environ["SUBNETS"] = "2"
# os.environ["NODES_PER_NET"] = "2"
# os.environ["LOOPS"] = "1000"
# os.environ["GENERATE_INTERVAL"] = "100"

if __name__ == "__main__":
    subnets = int(os.environ.get("SUBNETS", "2"))
    nodes_per_net = int(os.environ.get("NODES_PER_NET", "2"))
    loops = int(os.environ.get("LOOPS", "1000"))
    generate_interval = int(os.environ.get("GENERATE_INTERVAL", "100"))

    aloha = Aloha(subnets, nodes_per_net, loops, generate_interval)
    aloha.create()
    aloha.start()
