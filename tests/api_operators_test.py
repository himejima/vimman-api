# -*- coding: utf-8 -*-
import json
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
import app


class ApiOperatorsTestCase(unittest.TestCase):
    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

    def test_create(self):
        content_body = {
            'username': 'tester-1',
            'password': 'hogehoge',
            'state': '2'
        }
        raw_response = self.app.post(
            '/operators/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result']['id'] != ''
        assert response['result']['state'] == 2
        assert response['result']['username'] == 'tester-1'

    def test_invalid_create(self):
        content_body = {
            'password': 'hogehoge',
            'state': '2'
        }
        raw_response = self.app.post(
            '/operators/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_invalid_content_type_create(self):
        content_body = {
            'password': 'hogehoge',
            'state': '2'
        }
        raw_response = self.app.post(
            '/operators/',
            content_type='text/html',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_index(self):
        raw_response = self.app.get(
            '/operators/'
        )
        assert raw_response.status_code == 200
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result'][0]['id'] is not None
        assert response['result'][0]['state'] is not None
        assert response['result'][0]['username'] is not None

    def test_read(self):
        content_body = {
            'username': 'tester-2',
            'password': 'hogehoge',
            'state': '1'
        }
        raw_response = self.app.post(
            '/operators/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        raw_response = self.app.get(
            '/operators/%d' % created['result']['id']
        )
        assert raw_response.status_code == 200
        response = json.loads(raw_response.data)
        assert response['result']['id'] == created['result']['id']
        assert response['result']['state'] == created['result']['state']
        assert response['result']['username'] == created['result']['username']

    def test_unknown_read(self):
        raw_response = self.app.get(
            '/operators/%d' % 1000000
        )
        assert raw_response.status_code == 404

    def test_update(self):
        content_body = {
            'username': 'tester-3',
            'password': 'hogehoge',
            'state': '2'
        }
        raw_response = self.app.post(
            '/operators/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        content_body = {
            'username': 'tester-33',
            'password': 'hogehoge',
            'state': '3'
        }
        raw_response = self.app.put(
            '/operators/%d' % created['result']['id'],
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result']['id'] == created['result']['id']
        assert response['result']['state'] == 3
        assert response['result']['username'] == 'tester-33'

    def test_unknown_update(self):
        content_body = {
            'username': 'anything',
            'password': 'hogehoge',
            'state': '3'
        }
        raw_response = self.app.put(
            '/operators/%d' % 1000000,
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 404

    def test_invalid_content_type_update(self):
        content_body = {
            'username': 'tester-33',
            'password': 'hogehoge',
            'state': '3'
        }
        raw_response = self.app.post(
            '/operators/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        content_body = {
            'username': 'tester-34',
            'password': 'hogehoge',
            'state': '4'
        }
        raw_response = self.app.put(
            '/operators/%d' % created['result']['id'],
            content_type='text/html',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_delete(self):
        content_body = {
            'username': 'tester-4',
            'password': 'hogehoge',
            'state': '3'
        }
        raw_response = self.app.post(
            '/operators/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        raw_response = self.app.delete(
            '/operators/%d' % created['result']['id']
        )
        assert raw_response.status_code == 204

    def test_unknown_delete(self):
        raw_response = self.app.delete(
            '/operators/%d' % 100000
        )
        assert raw_response.status_code == 404


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiOperatorsTestCase))
    return suite
