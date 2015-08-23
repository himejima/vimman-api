# -*- coding: utf-8 -*-
import json
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
import app
from models.model import *  # NOQA


class ApiTweetsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        conn = engine.connect()
        trans = conn.begin()
        conn.execute('DELETE FROM tweets')
        trans.commit()

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

    # get parameterのq で検索がヒットする + 検索がヒットしない
    # TODO: testを分割する
    def test_index_filter_by_q(self):
        content_body = {
            'type': 'response',
            'tweet_id': '1',
            'content': 'filter-test by q',
            'post_url': 'http://www.yahoo.co.jp/'
        }
        raw_response = self.app.post(
            '/tweets/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201

        raw_response = self.app.get(
            '/tweets/?q=filter-test'
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

    # idで検索ができるテスト
    def test_index_filter_by_id(self):
        content_body = {
            'type': 'response',
            'tweet_id': '1',
            'content': 'tweet content id',
            'post_url': 'http://www.yahoo.co.jp/'
        }
        raw_response = self.app.post(
            '/tweets/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)

        raw_response = self.app.get(
            '/tweets/?id=%d' % created['result']['id']
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 1

    # cursorに数字以外の文字を入れる
    def test_invalid_index_filter_by_cursor(self):
        raw_response = self.app.get(
            '/tweets/?cursor=なにぬ'
        )

        assert raw_response.status_code == 404

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    # cursorで指定したときに、次のページが取得できる
    def test_index_filter_by_plus_cursor(self):
        # データ準備
        for i in range(25):
            content_body = {
                'type': 'response',
                'tweet_id': '1',
                'content': 'content-cursor-%d' % (i + 1),
                'post_url': 'http://www.yahoo.co.jp/'
            }
            raw_response = self.app.post(
                '/tweets/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/tweets/?q=cursor&cursor=1'
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 21

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    # cursorの値がプラスで、次のページがない
    def test_index_filter_by_plus_cursor2(self):
        for i in range(15):
            content_body = {
                'type': 'response',
                'tweet_id': '1',
                'content': 'content-plus-cursor2-%d' % (i + 1),
                'post_url': 'http://www.yahoo.co.jp/'
            }
            raw_response = self.app.post(
                '/tweets/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

            if i == 12:
                created = json.loads(raw_response.data)

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/tweets/?q=plus-cursor2&cursor=%s' % created['result']['id']
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) < 20
        assert response['cursor']['prev'] != 0

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    # cursorの値がマイナスで、次のページがない
    def test_index_filter_by_minus_cursor(self):
        # データ準備
        for i in range(10):
            content_body = {
                'type': 'response',
                'tweet_id': '1',
                'content': 'content-minus-cursor-%d' % (i + 1),
                'post_url': 'http://www.yahoo.co.jp/'
            }
            raw_response = self.app.post(
                '/tweets/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/tweets/?q=minus-cursor&cursor=-100000'
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) < 20
        assert response['cursor']['next'] != 0
        # print response['cursor']['next']


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiTweetsTestCase))
    return suite
