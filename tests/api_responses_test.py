# -*- coding: utf-8 -*-
import json
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
import app
from models.model import *  # NOQA


class ApiResponsesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        conn = engine.connect()
        trans = conn.begin()
        conn.execute('DELETE FROM responses')
        trans.commit()

    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

    def test_create(self):
        content_body = {
            'type': 'ok',
            'content': 'responses content',
            'state': '1'
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result']['id'] != ''
        assert response['result']['type'] == 'ok'
        assert response['result']['content'] == 'responses content'
        assert response['result']['state'] == 1

    def test_invalid_create(self):
        content_body = {
            'type': 'ng',
            'content': 'responses content ng',
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_invalid_content_type_create(self):
        content_body = {
            'type': 'ng',
            'content': 'responses content ng',
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='text/html',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_index(self):
        raw_response = self.app.get(
            '/responses/'
        )
        assert raw_response.status_code == 200
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result'][0]['id'] is not None
        assert response['result'][0]['type'] is not None
        assert response['result'][0]['content'] is not None
        assert response['result'][0]['state'] is not None

    def test_read(self):
        content_body = {
            'type': 'ng',
            'content': 'response',
            'state': '1'
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        raw_response = self.app.get(
            '/responses/%d' % created['result']['id']
        )
        assert raw_response.status_code == 200
        response = json.loads(raw_response.data)
        assert response['result']['id'] == created['result']['id']
        assert response['result']['type'] == created['result']['type']
        assert response['result']['content'] == created['result']['content']
        assert response['result']['state'] == created['result']['state']

    def test_unknown_read(self):
        raw_response = self.app.get(
            '/tweets/%d' % 1000000
        )
        assert raw_response.status_code == 404

    def test_update(self):
        content_body = {
            'type': 'ng',
            'content': 'response-3',
            'state': '1'
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        content_body = {
            'type': 'ng',
            'content': 'response-33',
            'state': '2'
        }
        raw_response = self.app.put(
            '/responses/%d' % created['result']['id'],
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result']['id'] == created['result']['id']
        assert response['result']['content'] == 'response-33'
        assert response['result']['state'] == 2

    def test_unknown_update(self):
        content_body = {
            'type': 'ng',
            'state': '2'
        }
        raw_response = self.app.put(
            '/responses/%d' % 1000000,
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 404

    def test_invalid_content_type_update(self):
        content_body = {
            'type': 'ng',
            'content': 'response-33',
            'state': '1'
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        content_body = {
            'type': 'ng',
            'content': 'response-34',
            'state': '2'
        }
        raw_response = self.app.put(
            '/responses/%d' % created['result']['id'],
            content_type='text/html',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_delete(self):
        content_body = {
            'type': 'ng',
            'content': 'response-4',
            'state': '1'
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        raw_response = self.app.delete(
            '/responses/%d' % created['result']['id']
        )
        assert raw_response.status_code == 204

    def test_unknown_delete(self):
        raw_response = self.app.delete(
            '/responses/%d' % 100000
        )
        assert raw_response.status_code == 404

    # get parameterのq で検索がヒットする + 検索がヒットしない
    def test_index_filter_by_q(self):
        content_body = {
            'type': 'ok',
            'content': u'content-あいうえお',
            'state': '1'
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201

        raw_response = self.app.get(
            '/responses/?q=あいう'
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) > 0

        raw_response = self.app.get(
            '/responses/?q=xxxxxxxx'
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 0

    # idで検索ができるテスト
    def test_index_filter_by_id(self):
        content_body = {
            'type': 'ok',
            'content': u'content-by-id',
            'state': '1'
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)

        raw_response = self.app.get(
            '/responses/?id=%d' % created['result']['id']
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 1

    # cursorに数字以外の文字を入れる
    def test_invalid_index_filter_by_cursor(self):
        raw_response = self.app.get(
            '/responses/?cursor=なにぬ'
        )

        assert raw_response.status_code == 404

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    # cursorで指定したときに、次のページが取得できる
    def test_index_filter_by_plus_cursor(self):
        # データ準備
        for i in range(25):
            content_body = {
                'type': 'ok',
                'content': u'content-cursor-%d' % (i + 1),
                'state': '1'
            }
            raw_response = self.app.post(
                '/responses/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/responses/?q=cursor&cursor=1'
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 21

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    # cursorの値がプラスで、次のページがない
    def test_index_filter_by_plus_cursor2(self):
        for i in range(15):
            content_body = {
                'type': 'ok',
                'content': 'content-plus-cursor2-%d' % (i + 1),
                'state': '1'
            }
            raw_response = self.app.post(
                '/responses/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

            if i == 12:
                created = json.loads(raw_response.data)

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/responses/?q=plus-cursor2&cursor=%s' % created['result']['id']
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
                'type': 'ok',
                'content': 'content-minus-cursor-%d' % (i + 1),
                'state': '1'
            }
            raw_response = self.app.post(
                '/responses/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/responses/?q=minus-cursor&cursor=-100000'
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) < 20
        assert response['cursor']['next'] != 0


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiResponsesTestCase))
    return suite
