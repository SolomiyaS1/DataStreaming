import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from kafka import KafkaProducer
from utils import load_config, create_logger
import msgpack

logger = create_logger(__name__)


class MessagePublisher(object):

    def __init__(self, topic):
        config = load_config()
        bootstrap_servers = config["bootstrap_servers"]
        self.topic = topic
        self._kafka_producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=msgpack.dumps
        )

    def publish_results(self, message):
        if len(message) != 0:
            self._kafka_producer.send(self.topic, str(message))
            logger.info("Published results: " + str(message))
            self._kafka_producer.flush()
            return 1
        else:
            return 0
