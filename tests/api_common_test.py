# -*- coding: utf-8 -*-
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
import app
from models.model import *  # NOQA


class ApiCommonTestCase(unittest.TestCase):
    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

    # 存在しない url にアクセス
    def test_not_found(self):
        raw_response = self.app.get(
            '/notfoundxxxxx/'
        )
        assert raw_response.status_code == 404


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiCommonTestCase))
    return suite
