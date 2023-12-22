import unittest

from ..models import ThreadedDB, Request, Response

from FelsonSports.DB import NBADB



class RequestTestCase(unittest.TestCase):

    def setUp(self):
        self.request = Request()


    def creates_request(self):
        self.assertIsInstance(self.request, Request)


class ThreadedDBTestCase(unittest.TestCase):

    pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(RequestTestCase('creates_request'))
    return suite
