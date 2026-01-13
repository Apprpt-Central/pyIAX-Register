"""ASL-old registration backend using a SQLAlchemy connection.

This module implements a backend that authenticates users from a
legacy `user_Nodes` table. It exposes a `aslold` initializer that
creates a scoped SQLAlchemy session and a `registerHandler` class with a
`verify()` method used by the IAX2 parser.
"""

from hashlib import md5
from register import register, baseRegister
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from os import path
import logging
import verboselogs

__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2024, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


verboselogs.install()
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class Node(Base):
    """Minimal declarative model for the legacy `user_Nodes` table."""

    __tablename__ = "user_Nodes"

    Node_ID: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int]
    secret: Mapped[str]


# Initializer: create DB engine and scoped session factory
class aslold(baseRegister):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        engine = create_engine(self.args.SQLALCHEMY_DB_URL, echo=False, pool_recycle=60 * 5, pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        self.Session = scoped_session(session_factory)

    def get_handler(self):
        # return a handler that will be used per-request
        return registerHandler(self.Session)


# Per-request handler that uses the provided session factory
class registerHandler(register):
    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session

    def verify(self, user, challenge, secret, method, host, port):
        """Verify hashed challenge against stored secret.

        The stored password is combined with the provided `challenge` and
        hashed with MD5; the result is compared to the `secret` value
        supplied by the client.
        """
        self.host = host
        self.port = port
        data = self.session.query(Node).filter_by(name=user).all()
        self.session.remove()
        if len(data) > 0:
            password = data[0].secret
            if md5(challenge.encode('utf-8') + password.encode('ascii')).hexdigest().lower() == secret.lower():
                logger.success(f"Authentication Success from {host}:{port} for user {user}")
                return True

        logging.warning("Authentication Failed")
        self.CauseCode = 0x0d
        self.Cause = f"User/Password Incorrect from {host}:{port} for user {user}"
        return False


def help(parser):
    group = parser.add_argument_group('ASL Old DB Registration Module')
    group.add_argument('--db', dest="SQLALCHEMY_DB_URL", default='mysql+pymysql://allstar:change_me@localhost/allstar', help='The SQLAlchemy database connection URL.')
