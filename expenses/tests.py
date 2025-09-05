from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Category,Expense
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

    def test_update_category(self):
        Category.objects.create(
            id=1,
            name='fun',
            user=self.user
        )

        response = self.client.patch('/expenses/category_details/1/',{
            "name": "Fun and entertainment"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Fun and entertainment")


class ExpensesTestCase(APITestCase):
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

    def test_update_expense(self):
        cat = Category.objects.create(
            id=1,
            name="fun",
            user=self.user,
            is_default=False
        )
        Expense.objects.create(
            id=1,
            amount=250000.00,
            category=cat,
            description="Going out with frends",
            date="2025-01-02",
            user=self.user
        )

        response = self.client.patch("/expenses/expenses_details/1/",{
            "description": "Geting out with reza and abol"
        })

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['description'],"Geting out with reza and abol")

class ExpensesFilterTestCase(APITestCase):
    def setUp(self):
        # ساخت یوزر و لاگین
        self.user = User.objects.create_user(
            id=1,
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        response = self.client.post("/account/login/token/", {
            "email": "test@example.com",
            "password": "password123"
        }, format="json")

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # ساخت category های مختلف
        self.cat_food = Category.objects.create(name="Food", user=self.user)
        self.cat_fun = Category.objects.create(name="Fun", user=self.user)
        self.cat_travel = Category.objects.create(name="Travel", user=self.user)

        # ساخت expense های مختلف
        Expense.objects.create(amount=100000, category=self.cat_food, description="Lunch", date="2025-05-01", user=self.user)
        Expense.objects.create(amount=500000, category=self.cat_fun, description="Cinema", date="2025-05-10", user=self.user)
        Expense.objects.create(amount=2000000, category=self.cat_travel, description="Trip to city", date="2025-05-20", user=self.user)
        Expense.objects.create(amount=250000, category=self.cat_food, description="Dinner", date="2025-05-15", user=self.user)
        Expense.objects.create(amount=750000, category=self.cat_fun, description="Concert", date="2025-05-25", user=self.user)

    def test_filter_by_category(self):
        response = self.client.get("/expenses/expenses/?category__id={}".format(self.cat_fun.id))
        self.assertEqual(response.status_code, 200)
        # باید فقط expense های Fun بیاد
        for exp in response.data:
            self.assertEqual(exp['category'], self.cat_fun.id)

    def test_filter_by_date_range(self):
        response = self.client.get("/expenses/expenses/?date__gte=2025-05-10&date__lte=2025-05-20")
        self.assertEqual(response.status_code, 200)
        for exp in response.data:
            self.assertGreaterEqual(exp['date'], "2025-05-10")
            self.assertLessEqual(exp['date'], "2025-05-20")

    def test_filter_by_amount_range(self):
        response = self.client.get("/expenses/expenses/?min_amount=200000&max_amount=800000")
        self.assertEqual(response.status_code, 200)
        for exp in response.data:
            self.assertGreaterEqual(float(exp['amount']), 200000)
            self.assertLessEqual(float(exp['amount']), 800000)

    def test_combined_filters(self):
        # مثال ترکیبی: category Fun و amount بین 400000 تا 800000
        response = self.client.get(
            f"/expenses/expenses/?category__id={self.cat_fun.id}&min_amount=400000&max_amount=800000"
        )
        self.assertEqual(response.status_code, 200)
        for exp in response.data:
            self.assertEqual(exp['category'], self.cat_fun.id)
            self.assertGreaterEqual(float(exp['amount']), 400000)
            self.assertLessEqual(float(exp['amount']), 800000)

class ExpensesRecurring(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            id=1,
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        response = self.client.post("/account/login/token/", {
            "email": "test@example.com",
            "password": "password123"
        }, format="json")

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_recurring(self):
        cat = Category.objects.create(
            id=1,
            name="fun",
            user=self.user,
            is_default=False
        )

        response = self.client.post('/expenses/recurring_expenses/',{
            "amount": 2500000.00,
            "category": 1,
            "description": "اجاره خانه",
            "frequency": "monthly",
            "anchor_date": "2025-09-04",
            "end_date": "2026-09-04",
            "active": True
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['description'], 'اجاره خانه')


