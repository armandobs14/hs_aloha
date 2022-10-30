import time
import logging
from tqdm import tqdm
from aloha.network import Network
from aloha.head_node import HeadNode
from aloha.network_node import Status
from aloha.member_node import MemberNode

logging.basicConfig(filename="aloha.log", level=logging.DEBUG)

class Aloha():
    def __init__(self, subnets: int = 2, nodes_per_subnet: int = 2, loops:int = 1000, generate_interval:int = 100):
        self.generate_interval = generate_interval
        self.nodes_per_subnet = nodes_per_subnet
        self.subnets = subnets
        self.loops = loops
    
    def create(self):
        """
        Create network structure
        """
        self.main_network = Network("BASE_STATION")
        self.subnet_list = []
        
        for i in range(self.subnets):
            subnet = Network(f"SUBNET_{i}")
            head_node = HeadNode(self.main_network, subnet)

            subnet.head_node = head_node
            for _ in range(self.nodes_per_subnet):
                subnet.members.append(MemberNode(subnet))
            
            self.subnet_list.append(subnet)
            self.main_network.members.append(head_node)

    
    def start(self):
        """
        Run aloha simulation
        """
        for loop_index in tqdm(range(self.loops)):
            time.sleep(1.0/30)
            self.main_network.clear()

            for subnet in self.subnet_list:
                # generation new packages according to predefined interval
                if (loop_index % self.generate_interval) == 0:
                    logging.debug(f"{subnet.network_name}:GENERATING PACKAGES")
                    subnet.head_node.generate()
                    for member in subnet.members:
                        member.generate()
                    continue
                
                # sessing data from head_node and member_nodes
                subnet.head_node.transmit()
                for member in subnet.members:
                    member.transmit()
                
                # validate member collision
                if subnet.has_collision():
                    logging.debug(f"{subnet.network_name}:MEMBER COLLISION")
                    subnet.notify_collision()
                
                # validate head_member collision
                if len(subnet.buffer) > 0 and subnet.head_node.Status == Status.TRANSMITING:
                    logging.debug(f"{subnet.network_name}:HEAD_MEMBER COLLISION")
                    subnet.notify_collision()
                    subnet.head_node.error()
                elif len(subnet.buffer) > 0 and subnet.head_node.Status == Status.IDLE:
                    logging.debug(f"{subnet.network_name}:MEMBER -> HEAD_NODE")
                    subnet.head_node.receive(subnet.buffer)
                    subnet.notify_success()
                    subnet.clear()

            # validate head_node collision
            if self.main_network.has_collision():
                logging.debug(f"{self.main_network.network_name}:HEAD_NODE COLLISION")
                self.main_network.notify_collision()
            elif len(self.main_network.buffer) > 0:
                logging.debug(f"{self.main_network.network_name}:HEAD_NODE -> BASE_STATION")
                self.main_network.notify_success()