import time
import logging
import pandas as pd
from pprint import pprint
from datetime import datetime
from aloha.aloha_logging import *
from aloha.network import Network
from alive_progress import alive_bar, alive_it
from aloha.head_node import HeadNode
from aloha.member_node import MemberNode
from aloha.aloha_logging import Status, log_line


class Aloha:
    def __init__(
        self,
        subnets: int,
        nodes_per_subnet: int,
        max_loop: int,
        generate_interval: int,
        head_node_generate: bool,
        head_node_coin: bool,
    ):
        self.generate_interval = generate_interval
        self.nodes_per_subnet = nodes_per_subnet
        self.subnets = subnets
        self.loops = max_loop
        self.head_node_generate = head_node_generate
        self.head_node_coin = head_node_coin

    def generate_packets(self):
        for subnet in self.subnet_list:
            if self.head_node_generate:
                subnet.head_node.generate()
            for node_index in range(self.nodes_per_subnet):
                subnet.members[node_index].generate()
        log_line()

    def create(self):
        """
        Create network structure
        """
        init_log()
        self.main_network = Network("BASE_STATION")
        self.subnet_list = []

        for i in range(self.subnets):
            subnet = Network(f"SUBNET_{i}")

            head_node = HeadNode(self.main_network, subnet, self.head_node_coin)

            subnet.head_node = head_node

            for node_index in range(self.nodes_per_subnet):
                subnet.members.append(MemberNode(subnet, node_index))

            self.subnet_list.append(subnet)
            self.main_network.members.append(head_node)

        if self.generate_interval < 0:
            self.generate_packets()
        return self

    def start(self):
        """
        Run aloha simulation
        """
        loop_index = 0

        packets_per_subnet = self.nodes_per_subnet
        if self.head_node_generate:
            packets_per_subnet += 1

        total_packts = self.subnets * packets_per_subnet
        with alive_bar() as bar:
            while True:
                time.sleep(1)
                bar()
                network_status = self.main_network.get_status()
                # All packets was received
                if len(network_status["memory"]) == total_packts:
                    return self

                # Generate packets
                if (
                    self.generate_interval > 0
                    and loop_index % self.generate_interval == 0
                ):
                    self.generate_packets()
                    loop_index += 1
                    continue

                for subnet in self.subnet_list:
                    for node in subnet.members:
                        node.submit()

                    subnet.head_node.submit()
                    status = subnet.get_submission_status()
                    subnet.notify(status)

                # Analyse main network collision
                status = self.main_network.get_submission_status()
                self.main_network.notify(status)

                loop_index += 1
                if self.loops > 0 and loop_index == self.loops:
                    return self

                log_line()

    def analyse(self):
        columns = ["timestamp", "network", "node", "type", "message"]
        log_df = pd.read_csv("aloha.log", header=None)
        log_df.columns = columns
        log_df["type"] = log_df["type"].str.strip()

        has_debug = log_df["timestamp"].str.contains("DEBUG:root")
        log_df = log_df[has_debug].copy()

        log_df["timestamp"] = log_df["timestamp"].apply(
            lambda t: t.split("DEBUG:root:").pop()
        )
        log_df["timestamp"] = pd.to_datetime(log_df["timestamp"])

        print("Estatísticas gerais")
        df = (
            log_df.groupby(["network", "type"], as_index=False)
            .agg({"timestamp": "count"})
            .pivot(index="network", columns="type", values="timestamp")
            .fillna(0)
        )

        if "IDLE" not in df.columns:
            df["IDLE"] = 0

        if "SUCCESS" not in df.columns:
            df["SUCCESS"] = 0

        if "PARTIAL_NODE_COLISION" not in df.columns:
            df["PARTIAL_NODE_COLISION"] = 0

        if "NODE_COLLISION" not in df.columns:
            df["NODE_COLLISION"] = 0

        if "COLLISION" not in df.columns:
            df["COLLISION"] = df["PARTIAL_NODE_COLISION"] + df["NODE_COLLISION"]

        df["BUSY"] = df["COLLISION"] + df["SUCCESS"]
        df["THROUGHPUT"] = df["SUCCESS"] / (df["IDLE"] + df["BUSY"])

        print(df)
        df.to_csv("metrics.csv")
