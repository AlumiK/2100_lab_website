import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from courses.models import Course


class CourseListTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='14412345678', password='123456')
        admin = get_user_model().objects.create_user(phone_number='13312345678', password='123456')
        permission = Permission.objects.get(codename='view_course')
        admin_group = Group.objects.create(name='course_admin')
        admin_group.permissions.add(permission)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()
        Course.objects.create(
            title='t1',
            description='d1',
            codename='SOFT1'
        )
        Course.objects.create(
            title='t2',
            description='d2',
            codename='SCIENCE2',
            price='100.00'
        )
        Course.objects.create(
            title='t3',
            description='d3',
            codename='SOFT3'
        )

    def test_course_list_access_denied(self):
        self.client.login(phone_number='14412345678', password='123456')

        response = self.client.get(
            reverse('api:courses:backstage:get-course-list'),
            {
                'codename': '',
                'title': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_course_list_no_filter(self):
        self.client.login(phone_number='13312345678', password='123456')
        course = Course.objects.get(codename='SCIENCE2')

        response = self.client.get(
            reverse('api:courses:backstage:get-course-list'),
            {
                'codename': '',
                'title': '',
                'page': 2,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'codename': '',
                'title': '',
                'count': 3,
                'page': 2,
                'num_pages': 3,
                'content': [
                    {
                        'codename': 'SCIENCE2',
                        'title': 't2',
                        'price': '100.00',
                        'updated_at': response_json_data['content'][0]['updated_at']
                    }
                ]
            }
        )

    def test_course_list_one_filter(self):
        self.client.login(phone_number='13312345678', password='123456')
        course = Course.objects.get(codename='SOFT1')

        response = self.client.get(
            reverse('api:courses:backstage:get-course-list'),
            {
                'codename': 'SOFT',
                'title': '',
                'page': 2,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'codename': 'SOFT',
                'title': '',
                'count': 2,
                'page': 2,
                'num_pages': 2,
                'content': [
                    {
                        'codename': 'SOFT1',
                        'title': 't1',
                        'price': '0.00',
                        'updated_at': response_json_data['content'][0]['updated_at']
                    }
                ]
            }
        )

    def test_course_list_two_filter(self):
        self.maxDiff = None
        self.client.login(phone_number='13312345678', password='123456')
        course = Course.objects.get(codename='SOFT1')

        response = self.client.get(
            reverse('api:courses:backstage:get-course-list'),
            {
                'codename': 'SOFT',
                'title': '1',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'codename': 'SOFT',
                'title': '1',
                'count': 1,
                'page': 1,
                'num_pages': 1,
                'content': [
                    {
                        'codename': 'SOFT1',
                        'title': 't1',
                        'price': '0.00',
                        'updated_at': response_json_data['content'][0]['updated_at']
                    }
                ]
            }
        )