import sys
import os

import unittest

#from registration_test import RegistrationTestCase
from auth_test import AuthTestCase
from profile_test import ProfileTestCase
from tickets_test import TicketsTestCase
from about_test import AboutTestCase
from admin_tests import AdminTestCase
from anon_test import AnonTestCase

# modify sys.path to get access to burrito
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from burrito.utils.db_utils import create_tables, drop_tables


#drop_tables(True)
#create_tables()


all_tests = unittest.TestSuite(
    [
##        unittest.TestLoader().loadTestsFromTestCase(RegistrationTestCase),
        unittest.TestLoader().loadTestsFromTestCase(AuthTestCase),
        unittest.TestLoader().loadTestsFromTestCase(ProfileTestCase),
        unittest.TestLoader().loadTestsFromTestCase(TicketsTestCase),
        unittest.TestLoader().loadTestsFromTestCase(AboutTestCase),
#        unittest.TestLoader().loadTestsFromTestCase(AdminTestCase),
        unittest.TestLoader().loadTestsFromTestCase(AnonTestCase)
    ]
)

#unittest.TestLoader.sortTestMethodsUsing = None
unittest.TextTestRunner().run(all_tests)
