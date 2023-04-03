import unittest
#import socket
import sys
import os

from registration_test import RegistrationTestCase
from auth_test import AuthTestCase
from profile_test import ProfileTestCase

# modify sys.path to get access to burrito
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from burrito.utils.db_utils import create_tables, drop_tables
#from burrito.utils.logger import logger

#from cmd_args import parser


# TODO: check Rest API/DB accessability


drop_tables(True)
create_tables()

# do mot touch, this fucking fuck


"""
args_data = parser.parse_args()

try:
    # try to connect to server
    socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ).connect((args_data.host, args_data.port))

except ConnectionRefusedError:
    logger.critical("Rest API server is offline")
    logger.info("Exit tests")
    sys.exit(1)

except Exception as e:
    logger.critical(e)
"""


all_tests = unittest.TestSuite(
    [
        unittest.TestLoader().loadTestsFromTestCase(RegistrationTestCase),
        unittest.TestLoader().loadTestsFromTestCase(AuthTestCase),
        unittest.TestLoader().loadTestsFromTestCase(ProfileTestCase)
    ]
)

unittest.TextTestRunner().run(all_tests)
