# -*- coding: utf-8 -*-
import json
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
import app
from models.model import *  # NOQA TODO: 呼び出し方を変更したい


class ApiInformationsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # テスト実行前に1回のみ実行する
        conn = engine.connect()
        trans = conn.begin()
        # conn.execute('TRUNCATE TABLE informations')
        conn.execute('DELETE FROM informations')
        trans.commit()

    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

    def test_create(self):
        content_body = {
            'content': 'content-1',
            'state': '2'
        }
        raw_response = self.app.post(
            '/informations/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result']['id'] != ''
        assert response['result']['state'] == 2
        assert response['result']['content'] == 'content-1'

    def test_invalid_create(self):
        content_body = {
            'state': '2'
        }
        raw_response = self.app.post(
            '/informations/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_invalid_content_type_create(self):
        content_body = {
            'state': '2'
        }
        raw_response = self.app.post(
            '/informations/',
            content_type='text/html',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_index(self):
        raw_response = self.app.get(
            '/informations/'
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
            'state': '1'
        }
        raw_response = self.app.post(
            '/informations/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        raw_response = self.app.get(
            '/informations/%d' % created['result']['id']
        )
        assert raw_response.status_code == 200
        response = json.loads(raw_response.data)
        assert response['result']['id'] == created['result']['id']
        assert response['result']['state'] == created['result']['state']
        assert response['result']['content'] == created['result']['content']

    def test_unknown_read(self):
        raw_response = self.app.get(
            '/informations/%d' % 1000000
        )
        assert raw_response.status_code == 404

    def test_update(self):
        content_body = {
            'content': 'content-3',
            'state': '2'
        }
        raw_response = self.app.post(
            '/informations/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        content_body = {
            'content': u'content-33',
            'state': '3'
        }
        raw_response = self.app.put(
            '/informations/%d' % created['result']['id'],
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result']['id'] == created['result']['id']
        assert response['result']['state'] == 3
        assert response['result']['content'] == 'content-33'

    def test_invalid_content_type_update(self):
        content_body = {
            'content': 'content-34',
            'state': '2'
        }
        raw_response = self.app.post(
            '/informations/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        content_body = {
            'content': 'content-44',
            'state': '3'
        }
        raw_response = self.app.put(
            '/informations/%d' % created['result']['id'],
            content_type='text/html',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    def test_unknown_update(self):
        content_body = {
            'content': 'anything',
            'state': '3'
        }
        raw_response = self.app.put(
            '/informations/%d' % 1000000,
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 404

    def test_delete(self):
        content_body = {
            'content': 'content-4',
            'state': '3'
        }
        raw_response = self.app.post(
            '/informations/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        raw_response = self.app.delete(
            '/informations/%d' % created['result']['id']
        )
        assert raw_response.status_code == 204

    def test_unknown_delete(self):
        raw_response = self.app.delete(
            '/informations/%d' % 100000
        )
        assert raw_response.status_code == 404

    def test_index_filter_by_q(self):
        content_body = {
            'content': 'content-あいうえお',
            'state': '1'
        }
        raw_response = self.app.post(
            '/informations/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201

        raw_response = self.app.get(
            '/informations/?q=あいう'
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) > 0

        raw_response = self.app.get(
            '/informations/?q=xxxxxxxx'
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 0

    def test_index_filter_by_id(self):
        content_body = {
            'content': 'content-index-id',
            'state': '3'
        }
        raw_response = self.app.post(
            '/informations/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)

        raw_response = self.app.get(
            '/informations/?id=%d' % created['result']['id']
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 1

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    def test_index_filter_by_plus_cursor(self):
        # データ準備
        for i in range(25):
            content_body = {
                'content': 'content-cursor-%d' % (i + 1),
                'state': '1'
            }
            raw_response = self.app.post(
                '/informations/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/informations/?q=cursor&cursor=1'
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 21

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    def test_index_filter_by_plus_cursor2(self):
        for i in range(15):
            content_body = {
                'content': 'content-plus-cursor2-%d' % (i + 1),
                'state': '1'
            }
            raw_response = self.app.post(
                '/informations/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

            if i == 12:
                created = json.loads(raw_response.data)

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/informations/?q=plus-cursor2&cursor=%s' % created['result']['id']
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) < 20
        assert response['cursor']['prev'] != 0

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    def test_index_filter_by_minus_cursor(self):
        # データ準備
        for i in range(10):
            content_body = {
                'content': 'content-minus-cursor-%d' % (i + 1),
                'state': '1'
            }
            raw_response = self.app.post(
                '/informations/',
                content_type='application/json',
                data=json.dumps(content_body)
            )
        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/informations/?q=minus-cursor&cursor=-100000'
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) < 20
        assert response['cursor']['next'] != 0
        # print response['cursor']['next']


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiInformationsTestCase))
    return suite
