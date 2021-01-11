from iax2.subclass import baseclass
from iax2.subclass.regauth import regauth
from iax2.subclass.regack import regack
from iax2.subclass.regrej import regrej
import time

__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


class regreq(baseclass):
    def __init__(self, data=None, **kwargs):
        super().__init__(data, **kwargs)

    def parse(self, data):
        # Use the baseClass parser then work with the data
        super().parse(data)
        if "ChallengeResponseMD5" in self.parsedData or "ChallengeResponseRSA" in self.parsedData:
            challengeSecret = self.call.get_entry('challengeSecret')
            if challengeSecret is None:
                return

            if 'ChallengeResponseMD5' in self.parsedData:
                challengeResponse = self.parsedData['ChallengeResponseMD5']
            elif 'ChallengeResponseRSA' in self.parsedData:
                challengeResponse = self.parsedData['ChallengeResponseRSA']

            # We have a ChallengeResponse, try and auth
            # user, challenge, secret, method, host, port
            host, port = self.call.get_entry('host')
            auth = self.register.verify(
                self.parsedData['UserName'],
                challengeSecret,
                challengeResponse,
                None, host, port
            )
            if auth:
                self.call.set_entry('RegRefresh', self.register.get_refresh())
                self.nodes[self.parsedData['UserName']] = time.time()
                self.response = regack
            else:
                self.call.set_entry('Cause',  self.register.Cause)
                self.call.set_entry('CauseCode',  self.register.CauseCode)
                self.response = regrej
        else:
            # Initital Reg Request
            self.call.set_entry('UserName', self.parsedData['UserName'])
            self.response = regauth
