"""This module provides tests for Way model"""

import datetime

from django.test import TestCase
from django.db.models import signals

from notification.models import Notification
from notification.signals import create_notification_task, revoke_notification_task
from way.models import Way
from custom_user.models import CustomUser
from place.models import Place
from route.models import Route


class WayModelTestCase(TestCase):
    """TestCase for providing Way model testing"""

    def setUp(self):
        """Method that provides preparation before testing Way model's features."""
        signals.post_save.disconnect(create_notification_task, sender=Notification)
        signals.post_delete.disconnect(revoke_notification_task, sender=Notification)

        self.user = CustomUser.objects.create(id=100, email='mail@gmail.com', password='Password1234', is_active=True)
        start_place = Place.objects.create(id=100, longitude=111.123456, latitude=84.123456)
        end_place = Place.objects.create(id=200, longitude=120.123456, latitude=89.123456)

        self.way = Way.objects.create(
            id=100,
            name='test_name',
            user=self.user
        )
        self.route = Route.objects.create(
            id=100,
            time='23:58:59',
            transport_name='',
            position=0,
            way=self.way,
            start_place=start_place,
            end_place=end_place
        )
        self.notification = Notification.objects.create(
            id=100,
            way=self.way,
            start_time=datetime.date(2019, 10, 29),
            end_time=datetime.date(2019, 12, 29),
            week_day=6,
            time=datetime.time(23, 58, 59)
        )

    def test_get_by_id(self):
        """Provide tests for `get_by_id` method of certain Way instance."""
        expected_way = Way.objects.get(id=self.way.id)
        actual_way = Way.get_by_id(obj_id=self.way.id)
        self.assertEqual(expected_way, actual_way)

        unexisting_way = Way.get_by_id(obj_id=999)
        self.assertIsNone(unexisting_way)
        self.assertRaises(Way.DoesNotExist, Way.objects.get, id=999)

    def test_delete_by_id(self):
        """Provide tests for `delete_by_id` method of certain Way instance."""
        is_deleted = Way.delete_by_id(obj_id=self.way.id)
        self.assertTrue(is_deleted)
        self.assertRaises(Way.DoesNotExist, Way.objects.get, id=self.way.id)

        is_deleted = Way.delete_by_id(obj_id=999)
        self.assertFalse(is_deleted)

    def test_to_dict(self):
        """Provide tests for `to_dict` method of certain Way instance."""
        way = Way.objects.get(id=self.way.id)

        expected_dict = {
            'id': 100,
            'name': 'test_name',
            'user_id': 100
        }
        actual_dict = way.to_dict()
        self.assertDictEqual(expected_dict, actual_dict)

    def test_create(self):
        """Provide tests for `create` method of Way model."""
        way = Way.create(user=self.user, name='name')
        self.assertIsInstance(way, Way)
        self.assertIsNotNone(Way.objects.get(id=way.id))

        way = Way.create(user=CustomUser())
        self.assertIsNone(way)

    def test_update(self):
        """Provide tests for `update` method of certain Way instance."""
        new_name = 'new_test_name'
        is_updated = self.way.update(name=new_name)
        self.assertTrue(is_updated)

        way = Way.objects.get(id=self.way.id)
        self.assertEqual(way.name, new_name)

    def test_get_way_with_routes(self):
        """Provide tests for `get_way_with_routes` method of certain Way instance."""
        way = Way.objects.get(id=self.way.id)

        expected_dict = {
            'id': 100,
            'name': 'test_name',
            'user_id': 100,
            'routes': [
                {
                    'id': 100,
                    'time': datetime.time(23, 58, 59),
                    'transport_name': '',
                    'position': 0,
                    'way': 100,
                    'start_place': 100,
                    'end_place': 200
                }
            ]

        }

        actual_dict = way.get_way_with_routes()
        self.assertDictEqual(expected_dict, actual_dict)

    def test_str(self):
        """Provide tests for `__str__` method of certain Way instance."""
        expected_string = f'Way id: {self.way.id}, user id: {self.way.user.id}'
        actual_string = self.way.__str__()

        self.assertEqual(expected_string, actual_string)

    def test_get_route_by_position(self):
        """Provide tests for `get_route_by_position` method of certain Way instance."""
        expected_route = self.way.get_route_by_position(position=0)
        self.assertEqual(expected_route, self.route)

        way_without_routes = Way.objects.create(user=self.user)
        expected_route = way_without_routes.get_route_by_position(position=0)
        self.assertIsNone(expected_route)

    def test_get_by_notification(self):
        """Provide tests for `get_by_notification` method of certain Way instance."""
        expected_way = self.way.get_by_notification(notification_id=100)
        self.assertEqual(expected_way, self.way)
