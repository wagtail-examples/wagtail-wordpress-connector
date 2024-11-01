from django.test import Client, TestCase


class TestStyleGuide(TestCase):
    def test_style_guide_view(self):
        client = Client()
        response = client.get("/style-guide/")
        self.assertEqual(response.status_code, 200)
