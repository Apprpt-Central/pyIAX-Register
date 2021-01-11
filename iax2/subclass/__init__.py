from struct import unpack_from, pack, calcsize
from enum import Enum
import logging
import verboselogs


__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


verboselogs.install()
logger = logging.getLogger(__name__)


VERSION = "pyIAX 0.0.1"


SUBCLASS = {
    0x02: "ping",
    0x03: "pong",
    0x04: "ack",
    0x0b: "lagrq",
    0x0c: "lagrp",
    0x0d: "regreq",
    0x0e: "regauth",
    0x0f: "regack",
    0x10: "regrej",
    0x42: "info",
}


INFO_ELEMENT = {
    0x02: ("CallingNumber", "c"),
    0x04: ("CallingName", "c"),
    0x06: ("UserName", "c"),
    0x0e: ("AuthMethod", "H"),
    0x0f: ("Challenge", "c"),
    0x10: ("ChallengeResponseMD5", "c"),
    0x11: ("ChallengeResponseRSA", "c"),
    0x12: ("ApparentAddress", "c"),
    0x13: ("Refresh", "H"),
    0x16: ("Cause", "c"),
    0x18: ("MessageCount", "BB"),
    0x1f: ("DateTime", "L"),
    0x2a: ("CauseCode", "B"),
    0x36: ("CallToken", "c"),
    0x42: ("Version", "c"),
    0x43: ("NumClients", "B"),
}


class frameTypes(Enum):
    IAX = 0x06


class baseclass():
    response = None
    call = None

    def __init__(self, data=None, **kwargs):
        if 'nodes' in kwargs:
            self.nodes = kwargs['nodes']

        if 'calls' in kwargs:
            self.call = kwargs['calls']

        if 'register' in kwargs:
            self.register = kwargs['register']

        if data is None:
            self.generate()
        else:
            self.parse(data)

    def parse(self, data):
        self.parsedData = {}
        offset = 0
        while offset < len(data):
            subclass, length = unpack_from("!BB", data, offset)
            dataFormat = INFO_ELEMENT[subclass]
            if dataFormat[1] == 'c':
                subData = b"".join(unpack_from(f"!{length}c", data, offset + 2)).decode('utf-8')
            else:
                subData = unpack_from(f"!{dataFormat[1]}", data, offset + 2)[0]
            offset += length + 2
            self.parsedData[dataFormat[0]] = subData
            logger.debug(f"Subclass: {subclass}, Name: {dataFormat[0]}, Data: {subData}")

    def generate(self, inputData):
        result = []
        result.append(pack("B", self.subClass))
        for format in self.format:
            # Format is: Type, Required, Default
            # Check to see if Type is in the inputData
            dataFormat = INFO_ELEMENT[format[0]]
            if format[0] in inputData:
                data = inputData[format[0]]
            # It's required, add the default value
            elif format[1]:
                data = format[2]
            else:
                data = None

            # If we have data to add, add it
            if data is not None:
                if dataFormat[1] == 'c':
                    result.append(pack(f"!BB{len(data)}c", format[0], len(data), *[data[i].encode('utf-8') for i in range(0, len(data))]))
                else:
                    result.append(pack(f"!BB{dataFormat[1]}", format[0], calcsize(dataFormat[1]), data))
        self.response = b"".join(result)

    def get_response(self):
        return self.response
