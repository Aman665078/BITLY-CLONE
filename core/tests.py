from django.test import TestCase
from .models import ShortURL
from django.contrib.auth.models import User


class ShortURLTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.short_url = ShortURL.objects.create(user=self.user, original_url='https://example.com')
    def test_short_code_generation(self):
        self.assertIsNotNone(self.short_url.short_code)
    def test_url_redirection(self):
        response = self.client.get(f'/{self.short_url.short_code}/')
        self.assertEqual(response.status_code, 302)
    def test_click_tracking(self):
        initial_clicks = self.short_url.click_count
        self.client.get(f'/{self.short_url.short_code}/')
        self.short_url.refresh_from_db()
        self.assertEqual(self.short_url.click_count, initial_clicks + 1)