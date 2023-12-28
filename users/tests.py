from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserTestCase(APITestCase):
    """ Тесты CRUD для модели Сотрудника """

    def setUp(self):
        self.client = APIClient()
        self.data = {
            "email": "test@test.com",
            "password": "test_qwerty",
            "first_name": "Test",
            "last_name": "Tester"
        }
        self.update_data = {
            "first_name": "FirstTest",
            "last_name": "LastTest"
        }

    def test_create_user(self):
        response = self.client.post('/users/', data=self.data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_list_users(self):
        user = User.objects.create_user(email='test@test.com', password='test_qwerty', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)
        response = self.client.get('/users/')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_detail_for_stuff_user(self):
        user = User.objects.create_user(email='test@test.com', password='test_qwerty', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/users/{user.pk}/')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_detail_for_not_stuff_user(self):
        user = User.objects.create_user(email='test@test.com', password='test_qwerty')
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/users/{user.pk}/')
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_update_for_staff_user(self):
        user = User.objects.create_user(email='test@test.com', password='test_qwerty', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/users/{user.pk}/', data=self.update_data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        updated_user = User.objects.get(pk=user.pk)
        self.assertEquals(updated_user.email, user.email)
        self.assertEquals(updated_user.first_name, self.update_data['first_name'])
        self.assertEquals(updated_user.last_name, self.update_data['last_name'])

    def test_update_for_not_staff_user(self):
        user = User.objects.create_user(email='test@test.com', password='test_qwerty')
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/users/{user.pk}/', data=self.update_data)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_destroy_user(self):
        user = User.objects.create_user(email='test@test.com', password='test_qwerty', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/users/{user.pk}/')
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
