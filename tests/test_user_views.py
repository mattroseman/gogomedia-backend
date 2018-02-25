import json
from base_test_case import GoGoMediaBaseTestCase

from database import db

from models.user import User


class GoGoMediaUserViewsTestCase(GoGoMediaBaseTestCase):
    def test_register(self):
        response = self.client.post('/register',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 201)
        self.assertTrue(body['success'])
        self.assertIsInstance(body['auth_token'], str)

        user = User.query.filter(User.username == 'testname').first()

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testname')

    def test_register_missing_request_body_params(self):
        response = self.client.post('/register',
                                    data=json.dumps({'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Request body is missing the parameter \'username\'')

        response = self.client.post('/register',
                                    data=json.dumps({'username': 'testname'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Request body is missing the parameter \'password\'')

    def test_register_existing_user(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/register',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'This username is already taken. Please choose another.')

    def test_login(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertIsInstance(body['auth_token'], str)

    def test_login_missing_request_body_params(self):
        response = self.client.post('/login',
                                    data=json.dumps({'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Request body is missing the parameter \'username\'')

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Request body is missing the parameter \'password\'')

    def test_invalid_login(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'pass123'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(body['success'])
        self.assertNotIn('auth_token', body)

    def test_login_with_unexisting_user(self):
        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'User doesn\'t exist. Please register user.')

    def test_logout(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))
        auth_token = body['auth_token']

        response = self.client.get('/logout')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        # TODO test that the auth_token is blacklisted
