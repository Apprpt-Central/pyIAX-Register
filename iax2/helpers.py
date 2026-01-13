"""Helpers to build IAX Information Elements (IEs).

Provides `IEDateTime` and `IEApparentAddr` helpers that produce the
binary representation expected by the IAX protocol for timestamps and
the apparent client address IE.
"""

from datetime import datetime, timezone
from ipaddress import ip_address, IPv4Address, IPv6Address
from struct import pack


class IEDateTime:
    """Construct the packed IEDateTime value per IAX specification.

    The resulting integer is formed by packing fields (seconds, minutes,
    hours, day, month, year offset) into bitfields as defined by the
    protocol. The input `TS` should be a timezone-aware datetime in UTC
    (defaults to now UTC).
    """

    def __init__(self, TS=None):
        if TS is None:
            TS = datetime.now(timezone.utc)
        # TODO: Validate TS is a datetime
        result = (TS.second >> 1) & 0x1f
        result = result | (TS.minute & 0x3f) << 5
        result = result | (TS.hour & 0x1f) << 11
        result = result | (TS.day & 0x1f) << 16
        result = result | ((TS.month) & 0x0f) << 21
        result = result | ((TS.year - 2000) & 0x7f) << 25
        self.result = result


class IEApparentAddr:
    """Pack an apparent-address IE for IPv4 (IPv6 not implemented).

    The format includes a family/type field, port and the packed IP
    address. IPv6 support is not implemented in this helper.
    """

    def __init__(self, address, port):
        ip = ip_address(address)
        if isinstance(ip, IPv4Address):
            # pack family/type, port, 4-byte IPv4 address and padding
            self.result = pack("!HH4sxxxxxxxx", 0x0200, port, ip.packed)
        elif isinstance(ip, IPv6Address):
            # TODO Not implementet yet for IPv6
            # pack family/type, port, 16-byte IPv6 address
            # self.result = pack("!HH4s16s4s", 0x0A00, port, "FlowInfo", ip.packed, "ScopeID")
            raise
        else:
            raise
