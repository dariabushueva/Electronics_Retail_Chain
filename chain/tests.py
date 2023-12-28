from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from chain.models import Supplier, Product
from users.models import User


class SupplierTestCase(APITestCase):
    """ Тесты CRUD для модели Поставщика """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

    def test_create_supplier(self):
        data = {
            "supplier_type": "FR",
            "name": "TestFactory",
            "email": "factory@mail.com",
            "country": "TestCountry",
            "city": "TestCity",
            "street": "TestStreet",
            "house_number": 33,
            "debt": 3300,
        }

        response = self.client.post(
            '/suppliers/',
            data=data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Supplier.objects.all().exists()
        )

    def test_list_supplier(self):
        Supplier.objects.create(
            supplier_type="FR",
            name="TestFactory",
            email="factory@mail.com",
            country="TestCountry",
            city="TestCity",
            street="TestStreet",
            house_number=33,
            debt=3300,
        )

        response = self.client.get(
            '/suppliers/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_detail_supplier(self):
        supplier = Supplier.objects.create(
            supplier_type="FR",
            name="TestFactory",
            email="factory@mail.com",
            country="TestCountry",
            city="TestCity",
            street="TestStreet",
            house_number=33,
            debt=3300,
        )

        response = self.client.get(
            f'/suppliers/{supplier.id}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_supplier(self):
        update_data = {
            "name": "test_update_name",
            "country": "test_update_country"
        }
        supplier = Supplier.objects.create(
            supplier_type="FR",
            name="TestFactory",
            email="factory@mail.com",
            country="TestCountry",
            city="TestCity",
            street="TestStreet",
            house_number=33,
            debt=3300,
        )

        response = self.client.patch(
            f'/suppliers/{supplier.id}/',
            data=update_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_destroy_supplier(self):
        supplier = Supplier.objects.create(
            supplier_type="FR",
            name="TestFactory",
            email="factory@mail.com",
            country="TestCountry",
            city="TestCity",
            street="TestStreet",
            house_number=33,
            debt=3300,
        )

        response = self.client.delete(
            f'/suppliers/{supplier.id}/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class ProductTestCase(APITestCase):
    """ Тесты CRUD для модели Продукта """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.supplier = Supplier.objects.create(
            supplier_type="FR",
            name="TestFactory",
            email="factory@mail.com",
            country="TestCountry",
            city="TestCity",
            street="TestStreet",
            house_number=33,
            debt=3300,
        )

        self.product = Product.objects.create(
            name="TestProduct",
            model="TestModel",
            launch_date="2023-12-12",
            supplier=self.supplier
        )

    def test_create_product(self):
        data = {
            "name": "TestProduct",
            "model": "TestModel",
            "launch_date": "2023-12-12",
            "supplier": self.supplier.id,
        }

        response = self.client.post(
            '/products/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.product.id + 1,
                'name': 'TestProduct',
                'model': 'TestModel',
                'launch_date': '2023-12-12',
                'supplier': self.supplier.id
            }
        )

        self.assertTrue(
            Supplier.objects.all().exists()
        )

    def test_list_product(self):

        response = self.client.get(
            '/products/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_product(self):
        update_data = {
            "name": "test_updated_name",
            "model": "test_updated_model"
        }
        response = self.client.patch(
            f'/products/{self.product.id}/',
            data=update_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'id': self.product.id,
                'name': 'test_updated_name',
                'model': 'test_updated_model',
                'launch_date': '2023-12-12',
                'supplier': self.supplier.id
            }
        )

    def test_destroy_supplier(self):

        response = self.client.delete(
            f'/products/{self.product.id}/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class ValidateDataTestCase(APITestCase):
    """ Валидация серриализуемых данных """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.supplier_rr = Supplier.objects.create(
            supplier_type="RR",
            name="TestRetailer",
            email="retailer@mail.com",
            country="AnotherCountry",
            city="AnotherCity",
            street="AnotherStreet",
            house_number=22,
            debt=2200,
        )

    def test_factory_cannot_have_parent(self):
        """ Проверка того, что завод не может иметь поставщика """

        data = {
            "supplier_type": "FR",
            "name": "NewFactory",
            "email": "new_factory@mail.com",
            "country": "NewCountry",
            "city": "NewCity",
            "street": "NewStreet",
            "house_number": 11,
            "debt": 0,
            "parent": self.supplier_rr.id
        }
        response = self.client.post(
            '/suppliers/',
            data=data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            'Завод не может иметь поставщика',
            str(response.data)
        )

    def test_update_debt_not_allowed(self):
        """ Проверка запрета обновления через API поля «Задолженность перед поставщиком» """

        data = {
            "debt": 3300
        }
        response = self.client.patch(
            f'/suppliers/{self.supplier_rr.id}/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            'Обновление поля "Задолженность перед поставщиком" запрещено.',
            str(response.data)
        )
