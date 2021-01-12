#!/usr/bin/env python3

from iax2.packet import iax2
from register.flatfile import flatfile as register
# from register.dummy import dummy as register
from verboselogs import VerboseLogger as getLogger
import logging
import socketserver
import threading
import time
import configargparse


__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


logger = getLogger('pyIAX-Regserver')


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
    parser = configargparse.ArgParser(default_config_files=['/etc/pyiax-reg/*.conf', 'pyiax-reg.conf'], description='IAX2 Registration Server')
    parser.add_argument('--listen_ip', dest='HOST', metavar='IP', help='The IP to listen on - default: 0.0.0.0', default='0.0.0.0')
    parser.add_argument('--port', dest='PORT', metavar='PORT', type=int, help='The UDP Port to listen on - default: 4569', default=4569)
    parser.add_argument('-v', dest='VERBOSE', action='count', help='Verbose Logs (More is more verbose)', default=0)
    parser.add_argument('-c', dest='COLOR', action='store_true', help='Display Colored logs - default False')

    args = parser.parse_args()

    # Configure logger for requested verbosity.
    if args.VERBOSE >= 3:
        logging_level = "DEBUG"
    elif args.VERBOSE >= 2:
        logging_level = "VERBOSE"
    elif args.VERBOSE >= 1:
        logging_level = "NOTICE"
    elif args.VERBOSE <= 0:
        logging_level = "WARNING"

    if args.COLOR:
        import coloredlogs
        coloredlogs.install(level=logging_level)
    else:
        logging.basicConfig(level=logging_level)

    server = ThreadedUDPServer((args.HOST, args.PORT), pyIAX)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        logger.success("Server started at {} port {}".format(args.HOST, args.PORT))
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()
