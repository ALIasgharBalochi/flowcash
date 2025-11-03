from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Income,IncomeCategory
User = get_user_model()

class IncomeTestCase(APITestCase): 
    def setUp(self):
        self.user = User.objects.create_user(
            id=1,
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
    def test_create_income(self):
        IncomeCategory.objects.create(
            uuid='85a0675f-5408-46fa-aa11-904896670b2e',
            name='salary',
            color='#2f2f2f',
            icon='nothing'
        )
        response = self.client.post('/income/income/',{
            "category":'85a0675f-5408-46fa-aa11-904896670b2e',
            "amount": "7500000.00",
            "source": "get budget of my family"
        })

        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data['amount'],"7500000.00")
        


# Create your tests here.
