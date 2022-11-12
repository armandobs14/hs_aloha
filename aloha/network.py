import gc
from typing import List
from aloha.head_node import HeadNode
from aloha.member_node import MemberNode


class Network:
    network_name: str
    head_node: HeadNode
    members: List[MemberNode]
    buffer: List

    def __init__(self, name):
        self.network_name = name
        self.members = list()
        self.buffer = []
        self.memory = []

    def has_collision(self):
        """
        Validate if more then one network node was sedded data
        """
        return len(self.buffer) > 1

    def notify_collision(self):
        """
        Notify all members when a collision occours
        """
        self.buffer = self.memory
        for node in self.members:
            node.error()

    def notify_success(self):
        """
        Notify all members when a transmission have success
        """

        for node in self.members:
            node.success()

        self.memory += self.buffer

    def receive(self, buffer: list):
        """
        Receive data from network node
        """
        self.buffer.append(buffer)

    def clear(self):
        """
        Clear network buffer
        """
        self.buffer = []
        self.memory = []
        gc.collect()
