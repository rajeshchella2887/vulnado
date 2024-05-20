from django.test import Client, TestCase
from django.urls import reverse


class HandleLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("accounts:login-user")

    def test_successful_login(self):
        response = self.client.post(self.url, {"username": "rahul", "password": "123"})
        self.assertEqual(response.status_code, 302)  # assert redirect status code
        self.assertEqual(response.url, "/dashboards")  # assert redirect target URL

    def test_failed_login(self):
        self.client.post(self.url, {"username": "rahul", "password": "123"})
        response = self.client.post(self.url, {"username": "ahul", "password": "923"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "invalid credentials")
