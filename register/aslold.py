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
    __tablename__ = "user_Nodes"

    Node_ID: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int]
    secret: Mapped[str]


# Initializer, add any connections you need here as they initialize at startup
class aslold(baseRegister):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        engine = create_engine(self.args.SQLALCHEMY_DB_URL, echo=False)
        session_factory = sessionmaker(bind=engine)
        self.Session = scoped_session(session_factory)

    def get_handler(self):
        return registerHandler(self.Session)


# Handlers are initialized at time of use,
class registerHandler(register):
    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session

    # hashed === md5(challenge+plaintext) -> success
    def verify(self, user, challenge, secret, method, host, port):
        self.host = host
        self.port = port
        data = self.session.query(Node).filter_by(name = user).all()
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
