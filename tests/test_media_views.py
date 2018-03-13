import json
import unittest
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
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'not started'
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')

    def test_add_media_missing_request_name_and_id_params(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'missing parameter \'name\' or parameter \'id\'')

    def test_add_media_mistyped_request_id_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': '12'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'id parameter must be type integer')

    def test_add_media_mistyped_request_name_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 23}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'name parameter must be type string')

    def test_add_media_mistyped_request_consumed_state_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': True}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'consumed_state parameter must be \'not started\', \'started\', or \'finished\'')

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': 'finised'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'consumed_state parameter must be \'not started\', \'started\', or \'finished\'')

    def test_add_media_mistyped_request_medium_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'medium': 'aduio'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'medium parameter must be \'film\', \'audio\', \'literature\', or \'other\'')

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'medium': 12}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'medium parameter must be \'film\', \'audio\', \'literature\', or \'other\'')

    def test_add_media_not_started(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': 'not started'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'not started'
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')

    def test_add_media_started(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': 'started'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'started'
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'started')

    def test_add_media_finished(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': 'finished'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'finished'
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'finished')

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
            'id': 1,
            'name': 'testmedianame',
            'medium': 'film',
            'consumed_state': 'not started'
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'film')
        self.assertEqual(media.consumed_state, 'not started')

    def test_add_media_with_medium_and_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({
                                       'name': 'testmedianame',
                                       'medium': 'audio',
                                       'consumed_state': 'started'
                                   }),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'audio',
            'consumed_state': 'started'
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'audio')
        self.assertEqual(media.consumed_state, 'started')

    def test_update_media_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed_state='not started')
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': media.id, 'consumed_state': 'started'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'started'
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].consumed_state, 'started')

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': media.id, 'consumed_state': 'finished'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'finished'
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].consumed_state, 'finished')

    def test_update_media_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='film')
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': media.id, 'medium': 'literature'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'literature',
            'consumed_state': 'not started'
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].medium, 'literature')

    def test_update_media_consumed_state_and_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({
                                       'id': media.id,
                                       'medium': 'audio',
                                       'consumed_state': 'finished'
                                   }),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'audio',
            'consumed_state': 'finished'
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].consumed_state, 'finished')
        self.assertEqual(media_list[0].medium, 'audio')

    def test_update_media_nonexistant_id(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': 1}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'logged in user doesn\'t have media with given id')

    def test_update_media_other_users_media_id(self):
        user1 = User('testname1', 'P@ssw0rd')
        user2 = User('testname2', 'pass123')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        media = Media('testmedianame', user1.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname2/media',
                                   data=json.dumps({'id': 1}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'logged in user doesn\'t have media with given id')

    def test_get_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, medium='film', consumed_state='started')
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        response = self.client.get('/user/testname/media')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertListEqual(sorted(body['data'], key=lambda media: media['name']),
                             [{'id': media1.id, 'name': 'testmedianame1', 'medium': 'film', 'consumed_state': 'started'},
                              {'id': media2.id, 'name': 'testmedianame2', 'medium': 'other', 'consumed_state': 'not started'}])

    def test_get_media_with_specific_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed_state='started', medium='film')
        media2 = Media('testmedianame2', user.id, consumed_state='started')
        media3 = Media('testmedianame3', user.id, consumed_state='not started', medium='other')
        media4 = Media('testmedianame4', user.id, consumed_state='finished')
        media5 = Media('testmedianame5', user.id, consumed_state='not started', medium='audio')
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed-state=not-started')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertListEqual(sorted(body['data'], key=lambda media: media['name']),
                             [{'id': media3.id, 'name': 'testmedianame3', 'medium': 'other', 'consumed_state': 'not started'},
                              {'id': media5.id, 'name': 'testmedianame5', 'medium': 'audio', 'consumed_state': 'not started'}])

    def test_get_media_with_specific_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed_state='started', medium='film')
        media2 = Media('testmedianame2', user.id, medium='other')
        media3 = Media('testmedianame3', user.id, consumed_state='finished', medium='film')
        media4 = Media('testmedianame4', user.id, medium='film')
        media5 = Media('testmedianame5', user.id, consumed_state='not started')
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
                         [{'id': media1.id, 'name': 'testmedianame1', 'medium': 'film', 'consumed_state': 'started'},
                          {'id': media3.id, 'name': 'testmedianame3', 'medium': 'film', 'consumed_state': 'finished'},
                          {'id': media4.id, 'name': 'testmedianame4', 'medium': 'film', 'consumed_state': 'not started'}])

    def test_get_media_with_specific_medium_and_specific_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed_state='finished', medium='film')
        media2 = Media('testmedianame2', user.id, medium='other')
        media3 = Media('testmedianame3', user.id, consumed_state='not started', medium='film')
        media4 = Media('testmedianame4', user.id, medium='film')
        media5 = Media('testmedianame5', user.id, consumed_state='started')
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed-state=not-started&medium=film')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [{'id': media3.id, 'name': 'testmedianame3', 'medium': 'film', 'consumed_state': 'not started'},
                          {'id': media4.id, 'name': 'testmedianame4', 'medium': 'film', 'consumed_state': 'not started'}])

    def test_get_media_with_malformed_consumed_state_url_parameter(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed-state=true')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'consumed-state url parameter must be \'not-started\', \'started\',  or \'finished\'')

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
                                      data=json.dumps({'id': media.id}),
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
        self.assertEqual(body['message'], 'missing parameter \'id\'')

    def test_delete_media_mistyped_request_body_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'id': '12'}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'id parameter must be type integer')

    def test_delete_unexisting_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'id': 3}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
