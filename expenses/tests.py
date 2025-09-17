from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Category,Expense,RecurringExpense
from .tasks import creating_recurring_costs
from datetime import date
import uuid 
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
            uuid="94455398-9df8-4973-9403-25ac7e4d4b2e",
            name='fun',
            user=self.user
        )

        response = self.client.patch('/expenses/category_details/94455398-9df8-4973-9403-25ac7e4d4b2e/',{
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
            uuid="94355398-9df8-4973-9403-25ac7e4d4b2e",
            name="fun",
            user=self.user,
            is_default=False
        )

        response = self.client.post('/expenses/expenses/',{
        "amount":250000.00,
        "category": "94355398-9df8-4973-9403-25ac7e4d4b2e",
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
            uuid="94455398-9df8-4973-9403-25ac7e4d4b2f",
            amount=250000.00,
            category=cat,
            description="Going out with frends",
            date="2025-01-02",
            user=self.user
        )

        response = self.client.patch("/expenses/expenses_details/94455398-9df8-4973-9403-25ac7e4d4b2f/",{
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
        self.cat_food = Category.objects.create(uuid="94455398-9df8-4973-9403-25ac7e4d4b4d",name="Food", user=self.user)
        self.cat_fun = Category.objects.create(uuid="94455398-9df8-4973-9403-25ac7e4d4b1c",name="Fun", user=self.user)
        self.cat_travel = Category.objects.create(uuid="21455398-9df8-4973-9403-25ac7e4d4b2e",name="Travel", user=self.user)

        # ساخت expense های مختلف
        Expense.objects.create(amount=100000, category=self.cat_food, description="Lunch", date="2025-05-01", user=self.user)
        Expense.objects.create(amount=500000, category=self.cat_fun, description="Cinema", date="2025-05-10", user=self.user)
        Expense.objects.create(amount=2000000, category=self.cat_travel, description="Trip to city", date="2025-05-20", user=self.user)
        Expense.objects.create(amount=250000, category=self.cat_food, description="Dinner", date="2025-05-15", user=self.user)
        Expense.objects.create(amount=750000, category=self.cat_fun, description="Concert", date="2025-05-25", user=self.user)

    def test_filter_by_category(self):
        response = self.client.get("/expenses/expenses/?category__uuid={}".format(self.cat_fun.uuid))
        self.assertEqual(response.status_code, 200)
        for exp in response.data:
            self.assertEqual(exp['category'], uuid.UUID(self.cat_fun.uuid))

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
        response = self.client.get(
            f"/expenses/expenses/?category__uuid={self.cat_fun.uuid}&min_amount=400000&max_amount=800000"
        )
        self.assertEqual(response.status_code, 200)
        for exp in response.data:
            self.assertEqual(exp['category'], uuid.UUID(self.cat_fun.uuid))
            self.assertGreaterEqual(float(exp['amount']), 400000)
            self.assertLessEqual(float(exp['amount']), 800000)

class ExpensesRecurring(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            id=1,
            uuid="24455378-9df8-4973-9403-25ac7e4d4b2e",
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
            uuid="94455378-9df8-4973-9403-25ac7e4d4b2e",
            name="Home",
            user=self.user,
            is_default=False
        )

        response = self.client.post('/expenses/recurring_expenses/',{
            "amount": 2500000.00,
            "category": "94455378-9df8-4973-9403-25ac7e4d4b2e",
            "description": "home rent",
            "frequency": "monthly",
            "anchor_date": "2025-09-16",
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['description'], "home rent")
    
    def test_updating_recurring_expenses(self):
        cat = Category.objects.create(
            id=1,
            uuid="94455398-9df8-4973-9403-25ac7e4d3b2e",
            name="home",
            user=self.user,
            is_default=False
        )

        RecurringExpense.objects.create(
            id=1,
            uuid="94455398-9df8-4973-9403-25ac7e4d4b3e",
            amount=2500000.00,
            description="به اقای محمودی اجاره خانه",
            frequency="monthly",
            anchor_date= "2025-09-04",
            next_run_at="2025-09-05",
            active=True,
            end_date="2026-09-04",
            created_at="2025-09-05T09:27:14.296468Z",
            updated_at="2025-09-05T09:27:14.296514Z",
            user=self.user,
            category=cat
        )  

        response = self.client.patch('/expenses/recurring_expenses_details/94455398-9df8-4973-9403-25ac7e4d4b3e/',{
            "description": "home rent"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], "home rent")

    def test_creating_expense_from_recurring(self):
        category = Category.objects.create(
            name="Rent",
            user=self.user,
            is_default=False
        )

        recurring = RecurringExpense.objects.create(
            user=self.user,
            category=category,
            amount=1000000,
            description="Monthly Rent",
            frequency="monthly",
            anchor_date=date.today(),
            next_run_at=date.today(),
            active=True
        )

        creating_recurring_costs()

        expenses = Expense.objects.filter(recurring=recurring)
        self.assertEqual(expenses.count(), 1)
        self.assertEqual(expenses.first().amount, recurring.amount)
        self.assertEqual(expenses.first().description, "Monthly Rent")

        recurring.refresh_from_db()
        self.assertGreater(recurring.next_run_at, date.today())

class Budget(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            id=1,
            uuid="24455378-9df8-4973-9403-25ac7e4d4b2e",
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        self.category = Category.objects.create(
            id=1,
            uuid="32455378-9df8-4973-9403-25ac7e4d4b2e",
            name="fun",
            is_default=False
        )

        response = self.client.post("/account/login/token/", {
            "email": "test@example.com",
            "password": "password123"
        }, format="json")

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
    

    def test_create_budget(self):
        response = self.client.post('/expenses/budget/',{
            "category": "32455378-9df8-4973-9403-25ac7e4d4b2e",
            "amount": 2000000.00,
            "user": self.user,
            "period": "monthly"
        })

        self.assertEqual(response.status_code,201)

