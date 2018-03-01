import json
from base_test_case import GoGoMediaBaseTestCase

from database import db

from models.user import User
from models.media import Media


class GoGoMediaMediaViewsTestCase(GoGoMediaBaseTestCase):
    def test_nonexistent_user_media_endpoint(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'user doesn\'t exist')

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
        self.assertEqual(body['data'], {
            'name': 'testmedianame',
            'consumed': False,
            'medium': 'other'
        })

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'other')

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
        self.assertEqual(body['message'], 'missing parameter \'name\'')

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
        self.assertEqual(body['data'], {
            'name': 'testmedianame',
            'consumed': True,
            'medium': 'other'
        })

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertTrue(media.consumed)
        self.assertEqual(media.medium, 'other')

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
        self.assertEqual(body['data'], {
            'name': 'testmedianame',
            'consumed': False,
            'medium': 'other'
        })

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'other')

    def test_add_media_with_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'medium': 'film'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'name': 'testmedianame',
            'consumed': False,
            'medium': 'film'
        })

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'film')

    def test_add_consumed_media_with_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': True, 'medium': 'audio'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'name': 'testmedianame',
            'consumed': True,
            'medium': 'audio'
        })

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertTrue(media.consumed)
        self.assertEqual(media.medium, 'audio')

    def test_update_media_consumed(self):
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
        self.assertEqual(body['data'], {
            'name': 'testmedianame',
            'consumed': True,
            'medium': 'other'
        })

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
        self.assertEqual(body['data'], {
            'name': 'testmedianame',
            'consumed': False,
            'medium': 'other'
        })

        media_list = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertFalse(media_list[0].consumed)

    def test_update_media_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='film')
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'medium': 'literature'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'name': 'testmedianame',
            'consumed': False,
            'medium': 'literature'
        })

        media_list = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].medium, 'literature')

    def test_update_media_consumed_and_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({
                                       'name': 'testmedianame',
                                       'consumed': True,
                                       'medium': 'audio'
                                   }),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'name': 'testmedianame',
            'consumed': True,
            'medium': 'audio'
        })

        media_list = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertTrue(media_list[0].consumed)
        self.assertEqual(media_list[0].medium, 'audio')

    def test_get_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed=True, medium='film')
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        response = self.client.get('/user/testname/media')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertListEqual(sorted(body['data'], key=lambda media: media['name']),
                             [{'name': 'testmedianame1', 'consumed': True, 'medium': 'film'},
                              {'name': 'testmedianame2', 'consumed': False, 'medium': 'other'}])

    def test_get_consumed_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed=True, medium='film')
        media2 = Media('testmedianame2', user.id, consumed=True)
        media3 = Media('testmedianame3', user.id, consumed=False, medium='other')
        media4 = Media('testmedianame4', user.id, consumed=False)
        media5 = Media('testmedianame5', user.id, consumed=True, medium='audio')
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
                         [{'name': 'testmedianame1', 'consumed': True, 'medium': 'film'},
                          {'name': 'testmedianame2', 'consumed': True, 'medium': 'other'},
                          {'name': 'testmedianame5', 'consumed': True, 'medium': 'audio'}])

    def test_get_unconsumed_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed=True, medium='film')
        media2 = Media('testmedianame2', user.id, consumed=True)
        media3 = Media('testmedianame3', user.id, consumed=False, medium='other')
        media4 = Media('testmedianame4', user.id, consumed=False)
        media5 = Media('testmedianame5', user.id, consumed=True, medium='audio')
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
                         [{'name': 'testmedianame3', 'consumed': False, 'medium': 'other'},
                          {'name': 'testmedianame4', 'consumed': False, 'medium': 'other'}])

    def test_get_media_with_specific_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed=True, medium='film')
        media2 = Media('testmedianame2', user.id, medium='other')
        media3 = Media('testmedianame3', user.id, consumed=False, medium='film')
        media4 = Media('testmedianame4', user.id, medium='film')
        media5 = Media('testmedianame5', user.id, consumed=True)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        response = self.client.get('/user/testname/media?medium=film')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [{'name': 'testmedianame1', 'consumed': True, 'medium': 'film'},
                          {'name': 'testmedianame3', 'consumed': False, 'medium': 'film'},
                          {'name': 'testmedianame4', 'consumed': False, 'medium': 'film'}])

    def test_get_consumed_media_with_specific_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed=True, medium='film')
        media2 = Media('testmedianame2', user.id, medium='other')
        media3 = Media('testmedianame3', user.id, consumed=False, medium='film')
        media4 = Media('testmedianame4', user.id, medium='film')
        media5 = Media('testmedianame5', user.id, consumed=True)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed=no&medium=film')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [{'name': 'testmedianame3', 'consumed': False, 'medium': 'film'},
                          {'name': 'testmedianame4', 'consumed': False, 'medium': 'film'}])

    def test_get_media_with_malformed_consumed_url_parameter(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed=true')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'consumed url parameter must be \'yes\' or \'no\'')

    def test_get_media_with_malformed_medium_url_parameter(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.get('/user/testname/media?medium=asdf')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'medium url parameter must be \'film\', \'audio\', \'literature\', or \'other\'')

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
        self.assertEqual(body['message'], 'missing parameter \'name\'')

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
