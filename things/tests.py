from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .models import Thing


# Create your tests here.
class ThingTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username='testuser1', password='password'
        )
        testuser1.save()

        test_thing = Thing.objects.create(
            name='john',
            owner=testuser1,
            desc='testing',
        )

    def test_things_model(self):
        thing = Thing.objects.get(id=1)
        actual_owner = str(thing.owner)
        actual_name = str(thing.name)
        actual_desc = str(thing.desc)

        self.assertEqual(actual_owner, 'testuser1')
        self.assertEqual(actual_name, 'john')
        self.assertEqual(actual_desc, 'testing')

    def test_get_thing_list(self):
        url = reverse('thing_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        things = response.data
        self.assertEqual(len(things), 1)
        self.assertEqual(things[0]['name'], 'john')

    def test_get_thing_by_id(self):
        url = reverse('thing_detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        thing = response.data
        self.assertEqual(thing['name'], 'john')

    def test_create_thing(self):
        url = reverse('thing_list')
        data = {'owner': 1, 'name': 'spoon', 'desc': 'spoon'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        things = Thing.objects.all()
        self.assertEqual(len(things), 2)
        self.assertEqual(Thing.objects.get(id=2).name, 'spoon')

    def test_update_thing(self):
        url = reverse('thing_detail', args=(1,))
        data = {'owner': '1', 'name': 'john', 'desc': 'test'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        thing = Thing.objects.get(id=1)
        self.assertEqual(thing.name, data['name'])
        self.assertEqual(str(thing.owner.id), data['owner'])
        self.assertEqual(thing.desc, data['desc'])

    def test_delete_thing(self):
        url = reverse('thing_detail', args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        things = Thing.objects.all()
        self.assertEqual(len(things), 0)