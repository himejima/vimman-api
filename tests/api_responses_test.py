import sys, os, json, unittest, urllib
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../src/api/')
import app

class ApiResponsesTestCase(unittest.TestCase):
    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

    def test_create(self):
        content_body = {
            'type' : 'ok',
            'content' : 'responses content',
            'state'    : '1'
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
            'type' : 'ng',
            'content' : 'responses content ng',
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
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
            'type' : 'ng',
            'content' : 'response',
            'state'    : '1'
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
            'type' : 'ng',
            'content' : 'response-3',
            'state'    : '1'
        }
        raw_response = self.app.post(
            '/responses/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        created = json.loads(raw_response.data)
        content_body = {
            'type' : 'ng',
            'content' : 'response-33',
            'state'    : '2'
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
            'type' : 'ng',
            'state'    : '2'
        }
        raw_response = self.app.put(
            '/responses/%d' % 1000000,
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 404

    def test_delete(self):
        content_body = {
            'type' : 'ng',
            'content' : 'response-4',
            'state'    : '1'
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

if __name__ == '__main__':
    unittest.main()
