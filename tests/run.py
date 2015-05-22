import sys, os, json, unittest, urllib
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

if __name__ == '__main__':
    unittest.main()
