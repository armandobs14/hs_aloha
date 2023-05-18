import gc
from typing import List
from aloha.head_node import HeadNode
from aloha.aloha_utils import flatten
from aloha.aloha_logging import Status
from aloha.member_node import MemberNode
from aloha.aloha_logging import Status, log_info, log


class Network:
    network_name: str
    head_node: HeadNode
    members: List[MemberNode]

    def __init__(self, name):
        self.network_name = name
        self.members = list()
        self.memory = []

    def get_status(self):
        return {
            "network_name": self.network_name,
            "buffer": self.buffer,
            "memory": self.memory,
        }

    def get_transmitting_nodes(self):
        return [node for node in self.members if node.Status == Status.TRANSMITING]

    @property
    def buffer(self):
        buffers = [node.buffer for node in self.get_transmitting_nodes()]
        return flatten(buffers)

    def get_submission_status(self):
        """
        Validate if more then one network node was sedded data
        """
        transmitting_nodes = self.get_transmitting_nodes()

        if hasattr(self, "head_node"):
            # Member and head collision
            if (
                len(transmitting_nodes) >= 1
                and self.head_node.Status == Status.TRANSMITING
            ):
                log_info(self, None, Status.PARTIAL_NODE_COLISION)
                return Status.PARTIAL_NODE_COLISION

        # Member collision
        if len(transmitting_nodes) > 1:
            log_info(self, None, Status.NODE_COLLISION)
            return Status.NODE_COLLISION

        if len(transmitting_nodes) == 0:
            log_info(self, None, Status.IDLE)
            return Status.IDLE

        if len(transmitting_nodes) == 1:
            log_info(self, None, Status.SUCCESS)
            return Status.SUCCESS

    def notify_collision(self, collision_type):
        """
        Notify all members when a collision occours
        """
        transmitting_nodes = self.get_transmitting_nodes()

        if collision_type == Status.PARTIAL_NODE_COLISION:
            self.head_node.success()

        for node in transmitting_nodes:
            node.error()

    def notify(self, status):
        log(self, None, status)
        if status in [
            Status.NODE_COLLISION,
            Status.PARTIAL_NODE_COLISION,
        ]:
            self.notify_collision(status)
        elif status == Status.SUCCESS:
            self.notify_success()

    def notify_success(self):
        """
        Notify all members when a transmission have success
        """
        if hasattr(self, "head_node"):
            self.head_node.receive(self.buffer)

        self.memory += flatten([self.buffer])

        for node in self.members:
            node.success()

    def clear(self):
        """
        Clear network buffer
        """
        self.memory = []
        gc.collect()
