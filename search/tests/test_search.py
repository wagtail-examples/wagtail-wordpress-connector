from django.test import Client, TestCase


class TestSearch(TestCase):
    def test_search_view(self):
        client = Client()
        response = client.get("/search/")
        self.assertEqual(response.status_code, 200)

    def test_search_results_view(self):
        client = Client()
        response = client.get("/search/?query=hello")
        self.assertEqual(response.status_code, 200)

    def test_search_results_pagination(self):
        client = Client()
        response = client.get("/search/?query=hello&page=2")
        self.assertEqual(response.status_code, 200)

    def test_search_results_pagination_not_integer(self):
        client = Client()
        response = client.get("/search/?query=hello&page=not_integer")
        self.assertEqual(response.status_code, 200)

    def test_search_template(self):
        client = Client()
        response = client.get("/search/?query=hello")
        self.assertTemplateUsed(response, "search/search.html")
