from struct import unpack_from, pack
from iax2.subclass import SUBCLASS
from iax2.call import call
from cachetools import TTLCache
from secrets import randbits

import logging
import verboselogs
import time

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


# Source: https://stackoverflow.com/a/5998359
def current_milli_time():
    return int(round(time.time() * 1000))


class iax2():
    calls = TTLCache(512, 120)
    nodes = TTLCache(10000, 120)

    def __init__(self, register, notify):
        logger.info("Init IAX2")
        self.register = register
        self.notify = notify

    def parse_packet(self, data, host):
        logger.debug(f"received {data} from {host}")
        packet = iax2Packet(data, host, self)
        if packet.responseClass:
            # Since we have a responseClass, sending which ever response we're going to send
            return packet.build_response()


class iax2Packet():
    def __init__(self, data, host, parent):
        start_time = current_milli_time()
        self.parent = parent

        # F, Source Call Number -- 1, 15 Bits (16 Bits)
        # R, Destination Call Number -- 1, 15 Bits (16 Bits)
        # Time stamp - 32 Bit
        # OSeqno - 8 Bit
        # ISeqno - 8 Bit
        # Frame Type - 8 Bit
        # C, Subclass - 8 Bit
        # Data - Variable
        fsource, rdest, self.time, self.oseq, self.iseq, self.frame, csub = unpack_from("!HHLBBBB", data, 0)

        fFlag = fsource >> 15
        self.source = fsource & 0x7FFF

        rFlag = rdest >> 15
        self.dest = rdest & 0x7FFF

        cFlag = csub >> 15

        if fFlag == 1:
            length = 0x0C
        else:
            logger.debug("Mini-Frame - Not Supported")
            return

        if cFlag == 0:
            sub = csub & 0x7FFF
        else:
            logger.debug("Unsupported cFlag")
            return

        logger.debug(f"Source: {self.source}, rFlag: {rFlag}, Dest: {self.dest}, Time: {self.time}")
        logger.debug(f"OutSeq: {self.oseq}, InSeq: {self.iseq}, Frame: {self.frame}, SubClass: {sub}")

        self.call = self.get_call(self.source)
        if not self.call.get_entry("start_time"):
            self.call.set_entry("host", host)
            self.call.set_entry("start_time", start_time)

        # Find and load the correct packet parser
        if self.frame == 0x06:  # IAX Frame Type
            # TODO: Probably wrap this in a Try for any packet types we don't support
            module = __import__(f"iax2.subclass.{SUBCLASS[sub]}", fromlist=[''])
            parserResponse = getattr(module, SUBCLASS[sub])(data[length:], parent=self.parent, calls=self.call)

            # Get what ever response the parser has set, this is a reference to the class of the response
            self.responseClass = parserResponse.get_response()
        return None

    def build_response(self):
        response = self.responseClass(calls=self.call, nodes=self.parent.nodes)
        if self.dest == 0:
            self.dest = randbits(14)
        fsource = response.fType << 15 | self.dest
        frameType = response.frameType
        time = current_milli_time() - self.call.get_entry("start_time")
        logger.info(f"TIME: {time}")
        header = pack("!HHLBBB", fsource, self.source, self.time + time, self.iseq, self.oseq + 1, frameType.value)
        return header + response.get_response()

    def get_call(self, sourceCall):
        # We're probably a new call, so create a new call object
        if sourceCall not in self.parent.calls:
            self.parent.calls[sourceCall] = call(sourceCall)
        return self.parent.calls[sourceCall]
