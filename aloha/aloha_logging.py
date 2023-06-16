import os
import logging
from enum import Enum
from datetime import datetime

config = {"filename": "aloha.log", "level": logging.DEBUG}
logging.basicConfig(**config)


class Status(Enum):
    IDLE = "IDLE"
    SUCCESS = "SUCCESS"
    TRANSMITING = "TRANSMITING"
    GENERATING_PACKAGES = "GENERATING PACKAGES"
    PARTIAL_NODE_COLISION = "PARTIAL NODE COLISION + HEAD NODE SUCESS"
    HEAD_NODE_COLLISION = "HEAD_NODE COLLISION"
    NODE_COLLISION = "NODE COLLISION"


def init_log():
    try:
        os.truncate(config["filename"], 0)
    except:
        pass


def log_line():
    message_log = "___________________________________"
    logging.info(message_log)


def log_info(network, node_index, status):
    log(network, node_index, status, logging.INFO)


def log(network, node_index, status, level=logging.DEBUG):
    message_log = "{timestamp},{network}, {node_index}, {event_type}, {message}".format(
        timestamp=datetime.now().replace(microsecond=0).isoformat(),
        network=network.network_name,
        node_index=node_index,
        event_type=status.name,
        message=status.value,
    )
    logging.log(level, message_log)


def custom_log(message_log, level=logging.INFO):
    logging.log(level, message_log)
