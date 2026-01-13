"""Kafka notify backend to publish node updates as protobuf messages.

This module provides a `kafka` initializer that creates a
`confluent_kafka.Producer` and a `notifyHandler` which publishes a
serialized `update` protobuf message each time `notify()` is called.
"""

from notify import notify, baseNotify
from datetime import datetime
from dns_pb2 import update
from confluent_kafka import Producer

import logging
import verboselogs

__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2024, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


verboselogs.install()
logger = logging.getLogger(__name__)


class kafka(baseNotify):
    """Initializer that creates a confluent-kafka Producer instance."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = Producer({'bootstrap.servers': self.args.NOTIFY_BOOTSTRAP})

    def get_handler(self):
        return notifyHandler(producer=self.producer, topic=self.args.NOTIFY_TOPIC)


class notifyHandler(notify):
    """Publish a protobuf `update` message to the configured Kafka topic."""

    def __init__(self, producer, topic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = producer
        self.topic = topic

    def notify(self, user, host, port, *args, **kwargs):
        # Build protobuf update message from parameters
        Entry = update()
        Entry.timestamp.FromDatetime(datetime.now())
        Entry.node = int(user)
        Entry.ipaddress = host
        Entry.port = port
        Entry.ttl = 60
        Entry.server = "XXXXX"
        logger.debug(Entry)
        logger.success(f"Notification Success from {host}:{port} for user {user}")
        # Produce the serialized message to Kafka and flush
        self.producer.produce(self.topic, key=str(Entry.node).encode(), value=Entry.SerializeToString())
        self.producer.flush()


def help(parser):
    group = parser.add_argument_group('Dummy Notify Module')
    group.add_argument('--bootstrap', dest='NOTIFY_BOOTSTRAP', default='localhost:9092', help='Kafka bootstap server (Default: localhost:9092)')
    group.add_argument('--topic', dest='NOTIFY_TOPIC', default='test', help='Kafka topic')
