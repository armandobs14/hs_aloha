from aloha.network_node import NetWorkNode
from aloha.aloha_logging import Status
from aloha.aloha_logging import *
from random import choice
import uuid
import os
import gc


class HeadNode(NetWorkNode):
    def __init__(self, main_network, subnet, coin):
        self.Status = Status.IDLE
        self.coin = coin
        self.main_network = main_network
        self.subnet = subnet
        self.buffer = []

    def generate(self):
        """
        Generate a new package
        """
        log(self.subnet, "HEAD_NODE", Status.GENERATING_PACKAGES)
        self.buffer.append(uuid.uuid4())

    def clear(self):
        self.buffer = []
        gc.collect()

    def submit(self):
        """
        Transmit data to main_network
        """

        if self.coin:
            submit_condition = (
                len(self.buffer) > 0
                and choice([Status.TRANSMITING, Status.IDLE]) == Status.TRANSMITING
            )

        else:
            submit_condition = len(self.buffer) > 0

        if submit_condition:
            log_info(self.subnet, "HEAD_NODE", Status.TRANSMITING)
            self.Status = Status.TRANSMITING
        else:
            log_info(self.subnet, "HEAD_NODE", Status.IDLE)
            self.Status = Status.IDLE

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

    def log_status(self):
        """
        Log Current Status
        """
        custom_log(f"HEAD_NODE: {self.Status} {self.buffer}")
