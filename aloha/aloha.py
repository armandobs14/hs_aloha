import time
import logging
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from aloha.network import Network
from aloha.head_node import HeadNode
from aloha.network_node import Status
from aloha.member_node import MemberNode

logging.basicConfig(filename="aloha.log", level=logging.DEBUG)


class Aloha:
    def __init__(
        self,
        subnets: int = 2,
        nodes_per_subnet: int = 2,
        loops: int = 1000,
        generate_interval: int = 100,
    ):
        self.generate_interval = generate_interval
        self.nodes_per_subnet = nodes_per_subnet
        self.subnets = subnets
        self.loops = loops
        self.head_node_probability = 1.0 / self.subnets
        self.node_probability = 1.0 / self.nodes_per_subnet

    def create(self):
        """
        Create network structure
        """
        self.main_network = Network("BASE_STATION")
        self.subnet_list = []

        for i in range(self.subnets):
            subnet = Network(f"SUBNET_{i}")

            head_node = HeadNode(self.main_network, subnet, self.head_node_probability)

            subnet.head_node = head_node
            for _ in range(self.nodes_per_subnet):
                subnet.members.append(MemberNode(subnet, self.node_probability))

            self.subnet_list.append(subnet)
            self.main_network.members.append(head_node)

    def start(self):
        """
        Run aloha simulation
        """
        for loop_index in tqdm(range(self.loops)):
            time.sleep(1.0 / 30)
            self.main_network.clear()

            for subnet in self.subnet_list:
                # generation new packages according to predefined interval
                if (loop_index % self.generate_interval) == 0:
                    message_log = "{timestamp}, {loop}, {network}, {event_type}, {message}".format(
                        timestamp=datetime.now().isoformat(),
                        loop=loop_index,
                        network=subnet.network_name,
                        event_type="GENERATING_PACKAGES",
                        message="GENERATING PACKAGES",
                    )
                    logging.debug(message_log)

                    subnet.head_node.generate()
                    for member in subnet.members:
                        member.generate()
                    # continue

                # sessing data from head_node and member_nodes
                subnet.head_node.transmit()
                for member in subnet.members:
                    member.transmit()

                if len(subnet.buffer) == 0:
                    message_log = "{timestamp}, {loop}, {network}, {event_type}, {message}".format(
                        timestamp=datetime.now().isoformat(),
                        loop=loop_index,
                        network=subnet.network_name,
                        event_type="IDLE",
                        message="MEMBER IDLE",
                    )
                    logging.debug(message_log)
                    subnet.notify_collision()

                # validate member collision
                if subnet.has_collision():
                    message_log = "{timestamp}, {loop}, {network}, {event_type}, {message}".format(
                        timestamp=datetime.now().isoformat(),
                        loop=loop_index,
                        network=subnet.network_name,
                        event_type="COLLISION",
                        message="MEMBER COLLISION",
                    )
                    logging.debug(message_log)
                    subnet.notify_collision()

                # validate head_member collision
                if (
                    len(subnet.buffer) > 0
                    and subnet.head_node.Status == Status.TRANSMITING
                ):
                    message_log = "{timestamp}, {loop}, {network}, {event_type}, {message}".format(
                        timestamp=datetime.now().isoformat(),
                        loop=loop_index,
                        network=subnet.network_name,
                        event_type="COLLISION",
                        message="HEAD_MEMBER COLLISION",
                    )
                    logging.debug(message_log)
                    subnet.notify_collision()
                    subnet.head_node.error()
                elif len(subnet.buffer) > 0 and subnet.head_node.Status == Status.IDLE:
                    message_log = "{timestamp}, {loop}, {network}, {event_type}, {message}".format(
                        timestamp=datetime.now().isoformat(),
                        loop=loop_index,
                        network=subnet.network_name,
                        event_type="SUCCESS",
                        message="MEMBER -> HEAD_NODE",
                    )
                    logging.debug(message_log)
                    subnet.head_node.receive(subnet.buffer)
                    subnet.notify_success()
                    subnet.clear()

            if len(self.main_network.buffer) == 0:
                message_log = (
                    "{timestamp}, {loop}, {network}, {event_type}, {message}".format(
                        timestamp=datetime.now().isoformat(),
                        loop=loop_index,
                        network=self.main_network.network_name,
                        event_type="IDLE",
                        message="HEAD_NODE IDLE",
                    )
                )
                logging.debug(message_log)

            # validate head_node collision
            if self.main_network.has_collision():
                message_log = (
                    "{timestamp}, {loop}, {network}, {event_type}, {message}".format(
                        timestamp=datetime.now().isoformat(),
                        loop=loop_index,
                        network=self.main_network.network_name,
                        event_type="COLLISION",
                        message="HEAD_NODE COLLISION",
                    )
                )
                logging.debug(message_log)
                self.main_network.notify_collision()
            elif len(self.main_network.buffer) > 0:
                message_log = (
                    "{timestamp}, {loop}, {network}, {event_type}, {message}".format(
                        timestamp=datetime.now().isoformat(),
                        loop=loop_index,
                        network=self.main_network.network_name,
                        event_type="SUCCESS",
                        message="HEAD_NODE -> BASE_STATION",
                    )
                )
                logging.debug(message_log)
                self.main_network.notify_success()

    def analyse(self):
        columns = ["timestamp", "loop", "network", "type", "message"]
        log_df = pd.read_csv("aloha.log", header=None)
        log_df.columns = columns
        log_df["type"] = log_df["type"].str.strip()

        log_df["timestamp"] = log_df["timestamp"].str.replace("DEBUG:root:", "")
        log_df["timestamp"] = pd.to_datetime(log_df["timestamp"])

        print("Estatísticas gerais")
        df = (
            log_df.groupby(["network", "type"], as_index=False)
            .agg({"loop": "count"})
            .pivot(index="network", columns="type", values="loop")
            .fillna(0)
        )

        df["performance"] = df["SUCCESS"] / df["GENERATING_PACKAGES"]

        print(df)
        df.to_csv("metrics.csv")
