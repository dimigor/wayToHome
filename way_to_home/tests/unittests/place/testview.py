"""
Place view tests
===============
"""
import json
from unittest import mock

from django.urls import reverse

from custom_user.models import CustomUser
from django.test import TestCase, Client

from place.models import Place


class PlaceViewTest(TestCase):
    """TestCase for providing Place view testing"""

    def setUp(self):
        """Method that provides preparation before testing Place view`s features."""
        custom_user = CustomUser.objects.create(id=2, email='mymail@icloud.com', is_active=True)
        custom_user.set_password('qwerty12345')
        custom_user.save()

        self.client = Client()
        self.client.login(email='mymail@icloud.com', password='qwerty12345')

        self.place = Place.objects.create(
            id=11,
            longitude=49.842601,
            latitude=23.968448,
            address='Широка 34, 79052',
            name='Дім',
            stop_id=None,
            user=custom_user
        )

        self.place2 = Place.objects.create(
            id=12,
            longitude=48.842601,
            latitude=21.968423,
            address='Сяйво 24, 79052',
            name='Робота',
            stop_id=None,
            user=custom_user
        )

    def test_get_one_success(self):
        """Method that tests the successful request to the certain place"""

        expected_data = {
            'id': 11,
            'longitude': "49.842601",
            'latitude': "23.968448",
            'name': 'Дім',
            'address': 'Широка 34, 79052',
            'stop_id': None,
            'user_id': 2
        }

        url = reverse('place', kwargs={'place_id': self.place.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(expected_data), json.loads(response.content))

    def test_get_all_success(self):
        """Method that tests the successful request to all user places"""
        expected_data = [
        {
            'id': 12,
            'longitude': "48.842601",
            'latitude': "21.968423",
            'name': 'Робота',
            'address': 'Сяйво 24, 79052',
            'stop_id': None,
            'user_id': 2
        },
        {
            'id': 11,
            'longitude': "49.842601",
            'latitude': "23.968448",
            'name': 'Дім',
            'address': 'Широка 34, 79052',
            'stop_id': None,
            'user_id': 2
        }]

        url = reverse('place', args=[])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(expected_data), json.loads(response.content))

    def test_get_failed_wrong_id(self):
        """Method that tests request to retrieve non existent object."""
        url = reverse('place', args=[1501])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)

    def test_get_non_owner(self):
        """Method that tests for request to retrieve non owner Place instance."""
        another_user = CustomUser(id=101, email='another_user@mail.com', is_active=True)
        another_user.set_password('qwerty12345')
        another_user.save()
        self.client.login(email='another_user@mail.com', password='qwerty12345')

        url = reverse('place', kwargs={'place_id': self.place.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_post_success(self):
        """Method that tests the success post request for creating place."""

        data = {
            'longitude': 12.842601,
            'latitude': 23.968448,
            'name': 'Дім',
            'address': 'Суха 3, 79052',
            'stop_id': None
        }

        expected_data = {
            'longitude': 12.842601,
            'latitude': 23.968448,
            'name': 'Дім',
            'address': 'Суха 3, 79052',
            'stop_id': None,
            'user_id': 2
        }

        url = reverse('place', args=[])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        response_dict = json.loads(response.content)
        response_dict.pop('id')

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response_dict, expected_data)

    def test_post_create_fail(self):
        """Method that tests when place was not created"""

        data = {
            'longitude': 12.842601,
            'latitude': 23.968448,
            'name': 'Дім',
            'address': 'Суха 3, 79052',
            'stop_id': None
        }
        url = reverse('place')

        with mock.patch('place.views.Place.create') as mock_place:
            mock_place.return_value = False
            response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_post_invalid_data(self):
        """Method that tests unsuccessful post request with invalid post data."""

        data = {
            'longitude': "fw",
            'latitude': 123.123,
            'address': "Lviv"
        }
        url = reverse('place', args=[])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_empty_json(self):
        """Method that tests unsuccessful post request with empty JSON data."""

        data = {}
        url = reverse('place', args=[])
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_put_success(self):
        """Method that test success put request for the updating the certain task."""

        data = {
            'name': 'Work'
        }

        url = reverse('place', kwargs={'place_id': self.place.id})
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_non_owner(self):
        """Method that tests for request to update non owner Place instance."""
        another_user = CustomUser(id=102, email='another_user1@mail.com', is_active=True)
        another_user.set_password('qwerty12345')
        another_user.save()
        self.client.login(email='another_user1@mail.com', password='qwerty12345')

        data = {
            'longitude': 12.842601
        }
        url = reverse('place', kwargs={'place_id': self.place.id})
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_put_empty_json(self):
        """Method that tests unsuccessful put request with empty JSON data."""
        data = {}
        url = reverse('place', kwargs={'place_id': 11})
        response = self.client.put(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_put_failed_wrong_id(self):
        """Method that tests request to update non existent object."""

        data = {
            'stop_id': 15,
        }

        url = reverse('place', kwargs={'place_id': 1100})
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_non_id(self):
        """Method that tests request to update object without id."""

        data = {
            'stop_id': 15,
        }

        url = reverse('place')
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_invalid_data(self):
        """Method that tests unsuccessful put request with invalid data."""

        data = {
            'stop_id': "asd",
        }
        url = reverse('place', kwargs={'place_id': self.place.id})
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_fail_update(self):
        """Method that tests when place was not updated"""
        data = {
            'stop_id': 15,
        }
        url = reverse('place', kwargs={'place_id': self.place.id})

        with mock.patch('place.views.Place.update') as mock_place:
            mock_place.return_value = False
            response = self.client.put(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_delete_success(self):
        """Method that tests successful delete request"""

        url = reverse('place', kwargs={'place_id': self.place.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)

    def test_delete_failed_wrong_id(self):
        """Method that tests request to delete non existent object."""

        url = reverse('place', kwargs={'place_id': 111})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 400)

    def test_delete_non_owner(self):
        """Method that tests for request to delete non owner Place instance."""
        another_user = CustomUser(id=102, email='another_user2@mail.com', is_active=True)
        another_user.set_password('qwerty12345')
        another_user.save()
        self.client.login(email='another_user2@mail.com', password='qwerty12345')

        url = reverse('place', kwargs={'place_id': self.place.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)

    def test_delete_non_id(self):
        """Method that tests request to delete object without id."""

        url = reverse('place')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

    def test_delete_fail_delete(self):
        """Method that tests when place was not deleted"""
        url = reverse('place', kwargs={'place_id': self.place.id})

        with mock.patch('place.views.Place.delete_by_id') as mock_place:
            mock_place.return_value = False
            response = self.client.delete(url)

        self.assertEqual(response.status_code, 400)
