from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import OTPToken
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class UserRegisterTest(APITestCase):

    def test_register_user_success(self):
        url = reverse("register")  
        data = {
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "first_name": "Ali",
            "last_name": "Developer"
        }
        
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data["message"], "User registered Successfully")

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "testuser@example.com")

class UserLoginTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("token_obtain_pair")  
        self.email = "test@example.com"
        self.password = "testpassword123"
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name="Ali",
            last_name="Test"
        )
    def test_login_user_success(self):

        url = reverse('token_obtain_pair')
        data = {
            "email":self.email,
            "password": self.password
        }

        response = self.client.post(url,data,format="json")

        self.assertEqual(response.status_code, 200)

        self.assertIn("access",response.data)
        self.assertIn("refresh", response.data)
        self.assertTrue(response.data["access"])
        self.assertIsInstance(response.data["access"], str)

class ProfileUpdateTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="Old",
            last_name="Name"
        )

        response = self.client.post("/account/login/token/", {
            "email": "test@example.com",
            "password": "password123"
        }, format="json")

        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_update_profile(self):
        response = self.client.patch("/account/profile/", {
            "first_name": "NewName"
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "NewName")

class ChangePasswordTest(APITestCase):
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

    def test_change_password(self):
        url = reverse('ch_password')
        data = {
            "old_password": "password123",
            "new_password": "passwordNew"
        }

        response = self.client.post(url,data,format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"],"Password changed successfully.")

class VerifyEmailTest(APITestCase):
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

    def test_verify_email_success(self):
        otp_token = OTPToken.objects.create(
            user=self.user,
            otp_code="123456",
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        response = self.client.post("/account/email_verified/", {
            "code": "123456"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(id=self.user.id).is_verified)

    def test_verify_email_invalid_code(self):
        response = self.client.post("/account/email_verified/", {
            "code": "999999"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid or expired OTP", response.data["message"])