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

dest = randbits(14)
source = 1 << 15

dataClass = info()

header = pack("!HHLBBB", source, dest, 10, 0, 0, frameTypes.IAX.value)
data = dataClass.generate(True)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(1)

s.sendto(header+dataClass.get_response(), ('127.0.0.1', 4569))

try:
    rec_data, addr = s.recvfrom(2048)
except socket.timeout:
    pass
else:
    parsedData = info(rec_data[0x0C:])
    print(parsedData.parsedData)
