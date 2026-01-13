"""Small helper that sends an IAX INFO packet to a local server.

Used during development to exercise the server's INFO handling and
response generation. The script crafts a minimal INFO frame and prints
the parsed response when one is received.
"""

import socket
from struct import pack
from iax2.subclass import frameTypes
from iax2.subclass.info import info
from secrets import randbits

__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


def main():
    # Build a random destination id and constant source id for testing
    dest = randbits(14)
    source = 1 << 15

    # Build initial INFO data class and IAX header
    dataClass = info(initial=True)
    header = pack("!HHLBBB", source, dest, 10, 0, 0, frameTypes.IAX.value)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)

    # send to localhost IAX port
    s.sendto(header + dataClass.get_response(), ('127.0.0.1', 4569))

    try:
        rec_data, addr = s.recvfrom(2048)
    except socket.timeout:
        # no response received
        pass
    else:
        # parse and print the INFO response payload
        parsedData = info(rec_data[0x0C:])
        print(parsedData.parsedData)


if __name__ == "__main__":
    main()
