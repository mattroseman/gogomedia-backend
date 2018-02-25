import datetime
import json
import jwt
from base_test_case import GoGoMediaBaseTestCase
from flask import current_app

from database import db

from models.user import User
from models.media import Media

from logic.media import get_media


class GoGoMediaMediaViewsTestCase(GoGoMediaBaseTestCase):
    def test_add_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'],
                         {'name': 'testmedianame', 'consumed': False})

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)

    def test_add_media_missing_request_body_params(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Request body is missing the parameter \'name\'.')

    def test_login_required_media_endpoint(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        # temporarily enable login for this test
        current_app.config['LOGIN_DISABLED'] = False

        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        # havn't logged in yet
        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'No Authorization header found. Please add auth_token in Authorization header.')
        self.assertEqual(user.media, [])

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))
        auth_token = body['auth_token']

        # have logged in
        response = self.client.put('/user/testname/media',
                                   headers={'Authorization': 'JWT ' + auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'],
                         {'name': 'testmedianame', 'consumed': False})
        media_list = get_media('testname')
        self.assertEqual(media_list, [{'name': 'testmedianame', 'consumed': False}])

    def test_login_required_media_endpoint_different_user(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        # temporarily enable login for this test
        current_app.config['LOGIN_DISABLED'] = False

        user1 = User('testname1', 'P@ssw0rd')
        user2 = User('testname2', 'pass123')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname1', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))
        auth_token = body['auth_token']

        self.assertIn('auth_token', body)

        response = self.client.put('/user/testname2/media',
                                   headers={'Authorization': 'JWT ' + auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'You are not logged in as this user. Please log in.')

        media_list = get_media('testname2')
        self.assertEqual(media_list, [])

    def test_login_invalid_auth_token(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        current_app.config['LOGIN_DISABLED'] = False

        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))
        auth_token = body['auth_token']
        # cut off the first character of the auth_token, making it invalid
        auth_token = auth_token[1:]

        response = self.client.put('/user/testname/media',
                                   headers={'Authorization': 'JWT ' + auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Invalid token. Please log in again.')

    def test_login_expired_auth_token(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        current_app.config['LOGIN_DISABLED'] = False

        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        # Manually create an auth_token for user that is expired
        payload = {
            'exp': datetime.datetime.utcnow() - datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id
        }
        auth_token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

        response = self.client.put('/user/testname/media',
                                   headers={'Authorization': 'JWT ' + auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Signature expired. Please log in again.')

    def test_nonexistent_user_media_endpoint(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'User doesn\'t exist. Please register user.')

    def test_add_media_consumed(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': True}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'],
                         {'name': 'testmedianame', 'consumed': True})

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertTrue(media.consumed)

    def test_add_media_unconsumed(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': False}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {'name': 'testmedianame', 'consumed': False})

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)

    def test_update_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed=False)
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': True}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'],
                         {'name': 'testmedianame', 'consumed': True})

        media_list = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertTrue(media_list[0].consumed)

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': False}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'],
                         {'name': 'testmedianame', 'consumed': False})

        media_list = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertFalse(media_list[0].consumed)

    def test_get_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        response = self.client.get('/user/testname/media')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [{'name': 'testmedianame1', 'consumed': False},
                          {'name': 'testmedianame2', 'consumed': False}])

    def test_get_consumed_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed=True)
        media2 = Media('testmedianame2', user.id, consumed=True)
        media3 = Media('testmedianame3', user.id, consumed=False)
        media4 = Media('testmedianame4', user.id, consumed=False)
        media5 = Media('testmedianame5', user.id, consumed=True)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed=yes')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [{'name': 'testmedianame1', 'consumed': True},
                          {'name': 'testmedianame2', 'consumed': True},
                          {'name': 'testmedianame5', 'consumed': True}])

    def test_get_unconsumed_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed=True)
        media2 = Media('testmedianame2', user.id, consumed=True)
        media3 = Media('testmedianame3', user.id, consumed=False)
        media4 = Media('testmedianame4', user.id, consumed=False)
        media5 = Media('testmedianame5', user.id, consumed=True)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed=no')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [{'name': 'testmedianame3', 'consumed': False},
                          {'name': 'testmedianame4', 'consumed': False}])

    def test_delete_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'name': 'testmedianame'}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])

        media_list = Media.query.filter(Media.user == user.id).all()

        self.assertEqual(media_list, [])

    def test_delete_media_missing_request_body_params(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Request body is missing the parameter \'name\'.')

    def test_delete_unexisting_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'name': 'testmedianame'}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
