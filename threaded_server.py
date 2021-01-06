#!/usr/bin/env python3

from iax2.packet import iax2
from register.dummy import dummy as register
from verboselogs import VerboseLogger as getLogger
import socketserver
import threading
import time
import coloredlogs


__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


logger = getLogger('pyIAX-Regserver')
coloredlogs.install(level='DEBUG')


class pyIAX(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        host = self.client_address
        response = self.server.iax2.parse_packet(data, host)
        logger.debug(f"Response: {response}")
        if response:
            self.request[1].sendto(response, host)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, *args, **kwargs):
        socketserver.UDPServer.__init__(self, *args, **kwargs)
        self.register = register()
        self.iax2 = iax2(self.register)


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 4569

    server = ThreadedUDPServer((HOST, PORT), pyIAX)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, PORT))
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()
