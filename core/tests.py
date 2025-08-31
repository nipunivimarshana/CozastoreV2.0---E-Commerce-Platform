# core/tests.py
from django.test import TestCase
from django.urls import reverse

class CoreViewsTest(TestCase):
    def test_home_page_status_code(self):
        """
        Test that the homepage returns a 200 OK status code.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        print("Completed: test_home_page_status_code")

    def test_home_page_uses_correct_template(self):
        """
        Test that the homepage renders the correct template.
        """
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base.html')
        print("Completed: test_home_page_uses_correct_template")