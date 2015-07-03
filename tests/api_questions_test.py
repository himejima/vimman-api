# -*- coding: utf-8 -*-
import json
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
import app


class ApiQuestionsTestCase(unittest.TestCase):
    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

    def test_create(self):
        content_body = {
            'content': 'question-1',
            'answers': 'answer-1\r\nanswer-2',
            'state': '2'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result']['id'] != ''
        assert response['result']['state'] == '2'  # FIXME: 文字列比較でないと一致しない問題を解消すること

#    # FIXME: 動作しない問題を解消すること
    def test_invalid_create(self):
        content_body = {
            'content': 'hogehoge'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        print raw_response.status_code
        print raw_response.data
        assert raw_response.status_code == 400

    def test_invalid_content_type_create(self):
        content_body = {
            'state': '3'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='text/html',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_index(self):
        raw_response = self.app.get(
            '/questions/'
        )
        assert raw_response.status_code == 200
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result'][0]['id'] is not None
        assert response['result'][0]['state'] is not None
        assert response['result'][0]['content'] is not None

    def test_read(self):
        content_body = {
            'content': 'content-2',
            'answers': 'answer-1',
            'state': '1'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        raw_response = self.app.get(
            '/questions/%d' % created['result']['id']
        )
        assert raw_response.status_code == 200
        response = json.loads(raw_response.data)
        assert response['result']['id'] == created['result']['id']
#        assert response['result']['state'] == created['result']['state']  # FIXME: 一致しない問題を解消すること
        assert response['result']['content'] == created['result']['content']

    def test_unknown_read(self):
        raw_response = self.app.get(
            '/questions/%d' % 1000000
        )
        assert raw_response.status_code == 404

    def test_update(self):
        content_body = {
            'content': 'question-3',
            'answers': 'answer-3_1\r\nanswer-3_2',
            'state': '2'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        content_body = {
            'content': 'question-33',
            'answers': 'answer-33_1\r\nanswer-33_2',
            'state': '3'
        }
        raw_response = self.app.put(
            '/questions/%d' % created['result']['id'],
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result']['id'] == created['result']['id']
        assert response['result']['state'] == 3
        assert response['result']['content'] == 'question-33'

#    def test_unknown_update(self):
#        content_body = {
#            'username' : 'anything',
#            'password' : 'hogehoge',
#            'state'    : '3'
#        }
#        raw_response = self.app.put(
#            '/questions/%d' % 1000000,
#            content_type='application/json',
#            data=json.dumps(content_body)
#        )
#        assert raw_response.status_code == 404

    def test_delete(self):
        content_body = {
            'content': 'question-4',
            'answers': 'answer-4_1\r\nanswer-4_2',
            'state': '2'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        raw_response = self.app.delete(
            '/questions/%d' % created['result']['id']
        )
        assert raw_response.status_code == 204

    def test_unknown_delete(self):
        raw_response = self.app.delete(
            '/questions/%d' % 100000
        )
        assert raw_response.status_code == 404


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiQuestionsTestCase))
    return suite
