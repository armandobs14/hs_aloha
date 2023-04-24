import gc
import uuid
from random import choice
from aloha.aloha_logging import *
from aloha.aloha_logging import Status
from aloha.network_node import NetWorkNode


class MemberNode(NetWorkNode):
    def __init__(self, main_network, probabilty, node_index):
        self.Status = Status.IDLE
        self.probability = probabilty
        self.main_network = main_network
        self.buffer = []
        self.node_index = node_index

    def generate(self):
        """
        Generate a new package
        """
        log(self.main_network, self.node_index, Status.GENERATING_PACKAGES)
        self.buffer.append(uuid.uuid4())

    def clear(self):
        self.buffer = []
        gc.collect()

    def submit(self):
        """
        Send data to the network
        """
        if (
            len(self.buffer) > 0
            and choice([Status.TRANSMITING, Status.IDLE]) == Status.TRANSMITING
        ):
            log_info(self.main_network, self.node_index, Status.TRANSMITING)
            self.Status = Status.TRANSMITING

        else:
            log_info(self.main_network, self.node_index, Status.IDLE)

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
