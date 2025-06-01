from abc import ABC
from abc import abstractmethod


class NetWorkNode(ABC):
    @abstractmethod
    def submit():
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

    @abstractmethod
    def log_status(self):
        raise NotImplementedError("Method not implemented")
