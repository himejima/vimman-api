# -*- coding: utf-8 -*-
import json
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
import app
from models.model import *  # NOQA


class ApiQuestionsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        conn = engine.connect()
        trans = conn.begin()
        conn.execute('DELETE FROM questions')
        trans.commit()

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

    def test_invalid_create(self):
        content_body = {
            'content': 'hogehoge'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
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

    def test_unknown_update(self):
        content_body = {
            'content': 'unknown-question-1',
            'answers': 'unknown-answer-1',
            'state': '2'
        }
        raw_response = self.app.put(
            '/questions/%d' % 1000000,
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

    # 不正なcontent type
    def test_invalid_content_type_update(self):
        content_body = {
            'content': 'unknown-question-1',
            'answers': 'unknown-answer-1',
            'state': '2'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)

        content_body = {
            'content': 'unknown-question-update-1',
            'answers': 'unknown-answer-update-1',
            'state': '2'
        }
        raw_response = self.app.put(
            '/questions/%d' % created['result']['id'],
            content_type='text/html',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 400

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

    # TODO: データ依存のテストを追加
    def test_index_filter_by_q(self):
        content_body = {
            'content': u'question-5かきくけこ',
            'answers': u'answer-5_1\r\nanswer-5_2\r\nあいう',
            'state': '2'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201

        raw_response = self.app.get(
            u'/questions/?q=かき'
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) > 0

        raw_response = self.app.get(
            '/questions/?q=xxxxxxxx'
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 0

    # idで検索ができるテスト
    def test_index_filter_by_id(self):
        content_body = {
            'content': u'question-5かきくけこ',
            'answers': u'answer-5_1\r\nanswer-5_2\r\nあいう',
            'state': '2'
        }
        raw_response = self.app.post(
            '/questions/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)

        raw_response = self.app.get(
            '/questions/?id=%d' % created['result']['id']
        )
        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 1

    # cursorに数字以外の文字を入れる
    def test_invalid_index_filter_by_cursor(self):
        raw_response = self.app.get(
            '/questions/?cursor=なにぬ'
        )

        assert raw_response.status_code == 404

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    # cursorで指定したときに、次のページが取得できる
    def test_index_filter_by_plus_cursor(self):
        # データ準備
        for i in range(25):
            content_body = {
                'content': u'content-cursor-%d' % (i + 1),
                'answers': u'answer-5_1\r\nanswer-5_2\r\nあいう',
                'state': '2'
            }
            raw_response = self.app.post(
                '/questions/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/questions/?q=cursor&cursor=1'
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) == 21

    # TODO: 別のテストで作成されたデータに依存しているので分離する
    # cursorの値がプラスで、次のページがない
    def test_index_filter_by_plus_cursor2(self):
        for i in range(15):
            content_body = {
                'content': 'content-plus-cursor2-%d' % (i + 1),
                'answers': u'answer-5_1\r\nanswer-5_2\r\nあいう',
                'state': '2'
            }
            raw_response = self.app.post(
                '/questions/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

            if i == 12:
                created = json.loads(raw_response.data)

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/questions/?q=plus-cursor2&cursor=%s' % created['result']['id']
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
                'content': 'content-minus-cursor-%d' % (i + 1),
                'answers': u'answer-5_1\r\nanswer-5_2\r\nあいう',
                'state': '2'
            }
            raw_response = self.app.post(
                '/questions/',
                content_type='application/json',
                data=json.dumps(content_body)
            )

        # TODO: q= を追い出す
        raw_response = self.app.get(
            '/questions/?q=minus-cursor&cursor=-100000'
        )

        response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert len(response['result']) < 20
        assert response['cursor']['next'] != 0
        # print response['cursor']['next']


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiQuestionsTestCase))
    return suite
