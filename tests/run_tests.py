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


drop_tables(True)
create_tables()


all_tests = unittest.TestSuite(
    [
        unittest.TestLoader().loadTestsFromTestCase(RegistrationTestCase),
        unittest.TestLoader().loadTestsFromTestCase(AuthTestCase),
        unittest.TestLoader().loadTestsFromTestCase(ProfileTestCase)
    ]
)

unittest.TextTestRunner(verbosity=2).run(all_tests)
