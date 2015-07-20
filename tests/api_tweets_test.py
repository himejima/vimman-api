# -*- coding: utf-8 -*-
import json
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
import app


class ApiTweetsTestCase(unittest.TestCase):
    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

    def test_create(self):
        content_body = {
            'type': 'response',
            'tweet_id': '1',
            'content': 'tweet content',
            'post_url': 'http://www.yahoo.co.jp/'
        }
        raw_response = self.app.post(
            '/tweets/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result']['id'] != ''
        assert response['result']['type'] == 'response'
        assert response['result']['tweet_id'] == 1
        assert response['result']['content'] == 'tweet content'

    def test_invalid_create(self):
        content_body = {
            'type': 'question',
            'tweet_id': '2',
            'content': 'tweet content invalid',
        }
        raw_response = self.app.post(
            '/tweets/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_invalid_content_type_create(self):
        content_body = {
            'type': 'question',
            'tweet_id': '2',
            'content': 'tweet content invalid',
        }
        raw_response = self.app.post(
            '/tweets/',
            content_type='text/html',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_index(self):
        raw_response = self.app.get(
            '/tweets/'
        )
        assert raw_response.status_code == 200
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result'][0]['id'] is not None
        assert response['result'][0]['tweet_id'] is not None
        assert response['result'][0]['content'] is not None
        assert response['result'][0]['post_url'] is not None

    def test_read(self):
        content_body = {
            'type': 'response',
            'tweet_id': '3',
            'content': 'tweet content3',
            'post_url': 'http://www.yahoo.co.jp/'
        }
        raw_response = self.app.post(
            '/tweets/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        raw_response = self.app.get(
            '/tweets/%d' % created['result']['id']
        )
        assert raw_response.status_code == 200
        response = json.loads(raw_response.data)
        assert response['result']['id'] == created['result']['id']
        assert response['result']['tweet_id'] == created['result']['tweet_id']
        assert response['result']['content'] == created['result']['content']
        assert response['result']['post_url'] == created['result']['post_url']

    def test_unknown_read(self):
        raw_response = self.app.get(
            '/tweets/%d' % 1000000
        )
        assert raw_response.status_code == 404

    # TODO: データ依存のテストを追加
    def test_index_filter(self):
        content_body = {
            'type': 'response',
            'tweet_id': '3',
            'content': 'tweet contentあいうえお',
            'post_url': 'http://www.yahoo.co.jp/'
        }
        raw_response = self.app.post(
            '/tweets/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201

        raw_response = self.app.get(
            '/tweets/?q=あいう'
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) > 0

        raw_response = self.app.get(
            '/tweets/?q=xxxxxxxx'
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 0


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiTweetsTestCase))
    return suite
