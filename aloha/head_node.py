from aloha.network_node import NetWorkNode
from aloha.network_node import Status
from random import randint
import uuid

class HeadNode(NetWorkNode):
    def __init__(self, main_network, subnet):
        self.Status = Status.IDLE
        self.main_network = main_network
        self.subnet = subnet
        self.buffer = []
    
    def generate(self):
        """
        Generate a new package
        """
        self.buffer.append(uuid.uuid4())
    
    def clear(self):
        self.buffer = []

    def transmit(self):
        """
        Transmit data to main_network
        """
        if randint(1, 2) == 1 and len(self.buffer) > 0:
            self.main_network.receive(self.buffer)
            self.Status = Status.TRANSMITING

    def receive(self, data):
        """
        Receive data from the network
        """
        self.buffer += data
    
    def success(self):
        """
        Handle data when the transmission was
        success
        """
        if self.Status == Status.TRANSMITING:
            self.Status = Status.IDLE
            self.clear()
    
    def error(self):
        """
        Handle data when the transmission was
        collision
        """
        if self.Status == Status.TRANSMITING:
            self.Status = Status.IDLE