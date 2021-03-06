import json

from django.test import TestCase
from django.urls import reverse

from courses.models import Course, Hero


class MainPageTests(TestCase):
    def test_get_heroes(self):
        for index in range(1, 4):
            Hero.objects.create(
                image='fake/path/image' + str(index) + '.png',
                caption='c' + str(index)
            )

        response = self.client.get(reverse('api:courses:forestage:get-heroes'))
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'count': 3,
                'content': [
                    {
                        'image': 'fake/path/image1.png',
                        'hero_id': response_json_data['content'][0]['hero_id'],
                        'caption': 'c1'
                    },
                    {
                        'image': 'fake/path/image2.png',
                        'hero_id': response_json_data['content'][1]['hero_id'],
                        'caption': 'c2'
                    },
                    {
                        'image': 'fake/path/image3.png',
                        'hero_id': response_json_data['content'][2]['hero_id'],
                        'caption': 'c3'
                    }
                ]
            }
        )

    def test_get_recent_courses(self):
        Course.objects.create(
            title='t1',
            description='d1',
            codename='c1'
        )
        Course.objects.create(
            title='t2',
            description='d2',
            codename='c2',
            price='200.00'
        )
        Course.objects.create(
            title='t3',
            description='d3',
            codename='c3'
        )
        Course.objects.create(
            title='t4',
            description='d4',
            codename='c4'
        )
        Course.objects.create(
            title='t5',
            description='d5',
            codename='c5',
            price='500.00'
        )

        response = self.client.get(reverse('api:courses:forestage:get-recent-courses'))
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['free_courses'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['free_courses'][0]['title'], 't4')
        self.assertEqual(response_json_data['free_courses'][0]['description'], 'd4')
        self.assertEqual(response_json_data['free_courses'][1]['thumbnail'], '')
        self.assertEqual(response_json_data['free_courses'][1]['title'], 't3')
        self.assertEqual(response_json_data['free_courses'][1]['description'], 'd3')
        self.assertEqual(response_json_data['free_courses'][2]['thumbnail'], '')
        self.assertEqual(response_json_data['free_courses'][2]['title'], 't1')
        self.assertEqual(response_json_data['free_courses'][2]['description'], 'd1')
        self.assertEqual(response_json_data['paid_courses'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['paid_courses'][0]['title'], 't5')
        self.assertEqual(response_json_data['paid_courses'][0]['description'], 'd5')
        self.assertEqual(response_json_data['paid_courses'][1]['thumbnail'], '')
        self.assertEqual(response_json_data['paid_courses'][1]['title'], 't2')
        self.assertEqual(response_json_data['paid_courses'][1]['description'], 'd2')
