#!/usr/bin/env python3
"""UDP-based IAX2 registration server entrypoint.

This script sets up a threaded UDP server that parses IAX2 packets and
delegates registration and notification handling to pluggable modules
in the `register` and `notify` packages.
"""

from iax2.packet import iax2
from verboselogs import VerboseLogger as getLogger
import importlib
import logging
import socketserver
import threading
import time
import configargparse
import register
import notify

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
    """Request handler that passes raw UDP data to the IAX2 parser.

    The `self.request` attribute for UDP handlers is a (data, socket)
    tuple; `self.client_address` is the (host, port) tuple of the sender.
    """

    def handle(self):
        data = self.request[0]
        host = self.client_address
        # Parse incoming packet and optionally get a response to send
        response = self.server.iax2.parse_packet(data, host)
        logger.debug(f"Response: {response}")
        if response:
            # reply using the socket object in the request tuple
            self.request[1].sendto(response, host)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    """UDP server that holds references to register/notify handlers.

    The server stores the `iax2` parser instance on itself so request
    handlers can call `self.server.iax2`.
    """

    def __init__(self, *args, **kwargs):

        # Pop pluggable components from kwargs and keep them on the server
        self.register = kwargs.pop('register')
        self.notify = kwargs.pop('notify')
        self.args = kwargs.pop('args')

        # IAX2 parser requires register/notify handler objects
        self.iax2 = iax2(self.register, self.notify)
        socketserver.UDPServer.__init__(self, *args, **kwargs)


def main():
    parser = configargparse.ArgParser(
        default_config_files=['/etc/pyiax-reg/*.conf', './pyiax-reg.conf'],
        description='IAX2 Registration Server',
        add_help=False
    )
    parser.add_argument('-h', dest='HELP', action='store_true', help='show this help message and exit')
    parser.add_argument('--listen_ip', dest='HOST', metavar='IP', help='The IP to listen on - default: 0.0.0.0', default='0.0.0.0')
    parser.add_argument('--port', dest='PORT', metavar='PORT', type=int, help='The UDP Port to listen on - default: 4569', default=4569)
    parser.add_argument('-v', dest='VERBOSE', action='count', help='Verbose Logs (More is more verbose)', default=0)
    parser.add_argument('-c', dest='COLOR', action='store_true', help='Display Colored logs - default False')
    parser.add_argument('--register', dest="REGISTER", choices=register.__all__, help='Select the registration module to use')
    parser.add_argument('--notify', dest="NOTIFY", choices=notify.__all__, help='Select the noitification module to use')

    args, argv = parser.parse_known_args()

    if args.HELP:
        # If help requested, query modules for extra help and show it
        for moduleName in register.__all__:
            module = importlib.import_module(f"register.{moduleName}")
            if "help" in dir(module):
                module.help(parser)
        for moduleName in notify.__all__:
            try:
                module = importlib.import_module(f"notify.{moduleName}")
                if "help" in dir(module):
                    module.help(parser)
            except Exception:
                pass

        parser.parse_known_args()
        parser.print_help()
        return

    if args.REGISTER is None:
        print("Register Argument is not optional")
        return

    # Configure logger for requested verbosity.
    if args.VERBOSE >= 3:
        logging_level = "DEBUG"
    elif args.VERBOSE >= 2:
        logging_level = "VERBOSE"
    elif args.VERBOSE >= 1:
        logging_level = "NOTICE"
    else:
        logging_level = "WARNING"

    if args.COLOR:
        import coloredlogs
        coloredlogs.install(level=logging_level)
    else:
        logging.basicConfig(level=logging_level)

    # Initialize the chosen register backend
    registerMod = importlib.import_module(f"register.{args.REGISTER}")
    if "help" in dir(registerMod):
        registerMod.help(parser)
        args, argv = parser.parse_known_args()
    registerHandler = getattr(registerMod, args.REGISTER)(args=args)

    # Optionally initialize notify backend
    if args.NOTIFY:
        notifyMod = importlib.import_module(f"notify.{args.NOTIFY}")
        if "help" in dir(notifyMod):
            notifyMod.help(parser)
            args, argv = parser.parse_known_args()
        notifyHandler = getattr(notifyMod, args.NOTIFY)(args=args)
    else:
        notifyHandler = None

    server = ThreadedUDPServer((args.HOST, args.PORT), pyIAX, register=registerHandler, notify=notifyHandler, args=args)

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


if __name__ == "__main__":
    main()
