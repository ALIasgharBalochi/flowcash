from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterTest(APITestCase):

    def test_register_user_success(self):
        url = reverse("register")  # همون نامی که برای url ثبت نام دادی
        data = {
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "first_name": "Ali",
            "last_name": "Developer"
        }
        
        response = self.client.post(url, data, format="json")

        # چک کردن status code
        self.assertEqual(response.status_code, 201)

        # چک کردن پیام
        self.assertEqual(response.data["message"], "User registered Successfully")

        # چک کردن اینکه یوزر واقعا ساخته شده
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "testuser@example.com")
