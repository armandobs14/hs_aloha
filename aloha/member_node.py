import gc
import uuid
from random import random
from aloha.network_node import Status
from aloha.network_node import NetWorkNode


class MemberNode(NetWorkNode):
    def __init__(self, main_network, probabilty):
        self.Status = Status.IDLE
        self.probability = probabilty
        self.main_network = main_network
        self.buffer = []

    def generate(self):
        """
        Generate a new package
        """
        self.buffer.append(uuid.uuid4())

    def clear(self):
        self.buffer = []
        gc.collect()

    def transmit(self):
        """
        Send data to the network
        """
        if random() <= self.probability and len(self.buffer) > 0:
            self.main_network.receive(self.buffer)
            self.Status = Status.TRANSMITING
            self.clear()

    def receive(self, data):
        """Receive data from the network"""
        pass

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
