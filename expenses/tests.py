from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Category
User = get_user_model()

class CategoryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="testname",
            last_name="testFname"
        )

        response = self.client.post("/account/login/token/", {
            "email": "test@example.com",
            "password": "password123"
        }, format="json")

        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_category(self):

        response = self.client.post('/expenses/category/',{
            "name":"fun"
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"],"fun")


class ExpensesTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="testname",
            last_name="testFname"
        )

        response = self.client.post("/account/login/token/", {
            "email": "test@example.com",
            "password": "password123"
        }, format="json")

        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_expense(self):
        Category.objects.create(
            id=1,
            name="fun",
            user=self.user,
            is_default=False
        )

        response = self.client.post('/expenses/expenses/',{
        "amount":250000.00,
        "category": 1,
        "description": "Going out with friends ",
        "date":"2025-05-12"
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["description"],"Going out with friends")