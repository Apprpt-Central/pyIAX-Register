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


# Initializer, add any connections you need here as they initialize at startup
class kafka(baseNotify):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = Producer({'bootstrap.servers': self.args.NOTIFY_BOOTSTRAP})

    def get_handler(self):
        return notifyHandler(producer=self.producer, topic=self.args.NOTIFY_TOPIC)


# Handlers are initialized at time of use,
class notifyHandler(notify):
    def __init__(self, producer, topic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = producer
        self.topic = topic

    def notify(self, user, host, port, *args, **kwargs):
        Entry = update()
        Entry.timestamp.FromDatetime(datetime.now())
        Entry.node = int(user)
        Entry.ipaddress = host
        Entry.port = port
        Entry.ttl = 60
        Entry.server = "XXXXX"
        logger.success(Entry)
        logger.success(f"Authentication Success from {host}:{port} for user {user}")
        self.producer.produce(self.topic, key=str(Entry.node).encode(), value=Entry.SerializeToString())
        self.producer.flush()


def help(parser):
    group = parser.add_argument_group('Dummy Notify Module')
    group.add_argument('--bootstrap', dest='NOTIFY_BOOTSTRAP', default='localhost:9092', help='Kafka bootstap server (Default: localhost:9092)')
    group.add_argument('--topic', dest='NOTIFY_TOPIC', default='test', help='Kafka topic')
