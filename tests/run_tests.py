#! /usr/bin/env python

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

if __name__ == "__main__":
    import unittest
    from profile.profile_test import ProfileTestCase

    from about.about_test import AboutTestCase

    # from admin.admin_tests import AdminTestCase
    from anon.anon_test import AnonTestCase
    from auth.auth_test import AuthTestCase
    from comments.comments_test import CommentsTestCase
    from iofiles.iofiles_test import IOFilesTestCase
    from meta.meta_test import MetaTestCase
    from notifications.notifications_test import NotificationsTestCase
    from registration.registration_test import RegistrationTestCase
    from statistic.statistic_test import StatisticTestCase
    from tickets.tickets_test import TicketsTestCase

    all_tests = unittest.TestSuite(
        [
            # unittest.TestLoader().loadTestsFromTestCase(RegistrationTestCase),
            unittest.TestLoader().loadTestsFromTestCase(AuthTestCase),
            unittest.TestLoader().loadTestsFromTestCase(ProfileTestCase),
            unittest.TestLoader().loadTestsFromTestCase(TicketsTestCase),
            unittest.TestLoader().loadTestsFromTestCase(AboutTestCase),
            # unittest.TestLoader().loadTestsFromTestCase(AdminTestCase),
            unittest.TestLoader().loadTestsFromTestCase(AnonTestCase),
            unittest.TestLoader().loadTestsFromTestCase(MetaTestCase),
            unittest.TestLoader().loadTestsFromTestCase(IOFilesTestCase),
            unittest.TestLoader().loadTestsFromTestCase(CommentsTestCase),
            unittest.TestLoader().loadTestsFromTestCase(NotificationsTestCase),
            #            unittest.TestLoader().loadTestsFromTestCase(StatisticTestCase)
        ]
    )

    unittest.TextTestRunner(verbosity=1).run(all_tests)
