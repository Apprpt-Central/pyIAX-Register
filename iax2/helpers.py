from datetime import datetime, timezone
from ipaddress import ip_address, IPv4Address, IPv6Address
from struct import pack


class IEDateTime:
    """
       Per the RFC:
        The 5 least significant bits are seconds,
        the next 6 least significant bits are minutes,
        the next least significant 5 bits are hours,
        the next least significant 5 bits are the day of the month,
        the next least significant 4 bits are the month, 1-based index (i.e., January == 1, February == 2, etc.)
        the most significant 7 bits are the year. The year is offset from 2000
        The timezone of the clock MUST be UTC to avoid confusion between the peers
    """

    def __init__(self, TS=None):
        if TS is None:
            TS = datetime.now(timezone.utc)
        # TODO: Check what TS is, it needs to be a DateTime object
        result = (TS.second >> 1) & 0x1f
        result = result | (TS.minute & 0x3f) << 5
        result = result | (TS.hour & 0x1f) << 11
        result = result | (TS.day & 0x1f) << 16
        result = result | ((TS.month) & 0x0f) << 21
        result = result | ((TS.year - 2000) & 0x7f) << 25
        self.result = result


class IEApparentAddr:

    def __init__(self, address, port):
        ip = ip_address(address)
        if isinstance(ip, IPv4Address):
            self.result = pack("!HH4sxxxxxxxx", 0x0200, port, ip.packed)
        elif isinstance(ip, IPv6Address):
            # self.result = pack("!HH4s16s4s", 0x0A00, port, "FlowInfo", ip.packed, "ScopeID")
            raise
        else:
            raise
