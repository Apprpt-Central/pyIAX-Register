from struct import unpack_from, pack
from iax2.subclass import SUBCLASS
from iax2.call import call
from iax2.cache import timed_lru_cache
from secrets import randbits

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


class iax2():
    calls = {}

    def __init__(self, register):
        logger.info("Init IAX2")
        self.register = register

    @timed_lru_cache(120)
    def get_call(self, sourceCall):
        # We're probably a new call, so create a new call object
        if sourceCall not in self.calls:
            self.calls[sourceCall] = call(sourceCall)
        return self.calls[sourceCall]

    def parse_packet(self, data, host):
        logger.debug(f"received {data} from {host}")
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

        call = self.get_call(self.source)

        # Find and load the correct packet parser
        if self.frame == 0x06:  # IAX Frame Type
            # TODO: Probably wrap this in a Try for any packet types we don't support
            module = __import__(f"iax2.subclass.{SUBCLASS[sub]}", fromlist=[''])
            parserResponse = getattr(module, SUBCLASS[sub])(data[length:], register=self.register.get_handler(), calls=call)

            # Get what ever response the parser has set, this is a reference to the class of the response
            responseClass = parserResponse.get_response()
            if responseClass:
                # Since we have a responseClass, sending which ever response we're going to send
                return self.build_response(responseClass, call)
        return None

    def build_response(self, responseClass, call):
        response = responseClass(calls=call)
        if self.dest == 0:
            self.dest = randbits(14)
        fsource = response.fType << 15 | self.dest
        frameType = response.frameType
        header = pack("!HHLBBB", fsource, self.source, self.time + 10, self.iseq, self.oseq + 1, frameType.value)
        return header + response.get_response()
