import uuid
import logging
from abc import ABC
from enum import Enum
from typing import List
from abc import abstractmethod


class Status(Enum):
    IDLE = "IDLE"
    TRANSMITING = "TRANSMITING"


class NetWorkNode(ABC):
    @abstractmethod
    def transmit():
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def generate():
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def clear():
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def success():
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def error():
        raise NotImplementedError("Method not implemented")
