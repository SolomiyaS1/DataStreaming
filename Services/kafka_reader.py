import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from kafka import KafkaConsumer
import msgpack
from utils import load_config


class MessageReader:
    def __init__(self, topic):
        config = load_config()
        bootstrap_servers = config["bootstrap_servers"]
        self.topic = topic
        self._kafka_consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest', value_deserializer=msgpack.unpackb)

    def get_twits(self):
        self._kafka_consumer.subscribe(topics=self.topic)
        for message in self._kafka_consumer:
            yield message.topic, message.value
