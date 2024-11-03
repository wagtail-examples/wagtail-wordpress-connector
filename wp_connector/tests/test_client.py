import responses
from django.test import TestCase

from wp_connector.client import Client


class TestClient(TestCase):
    @responses.activate
    def test_url(self):
        responses.add(responses.GET, "http://localhost:8888/wp-json", status=200)
        client = Client("http://localhost:8888/wp-json")
        self.assertEqual(client.url, "http://localhost:8888/wp-json")

    @responses.activate
    def test_headers(self):
        responses.add(
            responses.GET,
            "http://localhost:8888/wp-json",
            headers={"X-WP-TotalPages": "10", "X-WP-Total": "100"},
        )
        client = Client("http://localhost:8888/wp-json")
        self.assertTrue(client.is_paged)
        self.assertEqual(client.get_total_pages, 10)
        self.assertEqual(client.get_total_results, 100)
        self.assertEqual(
            client.paged_endpoints,
            [
                "http://localhost:8888/wp-json?page=1",
                "http://localhost:8888/wp-json?page=2",
                "http://localhost:8888/wp-json?page=3",
                "http://localhost:8888/wp-json?page=4",
                "http://localhost:8888/wp-json?page=5",
                "http://localhost:8888/wp-json?page=6",
                "http://localhost:8888/wp-json?page=7",
                "http://localhost:8888/wp-json?page=8",
                "http://localhost:8888/wp-json?page=9",
                "http://localhost:8888/wp-json?page=10",
            ],
        )

    @responses.activate
    def test_get(self):
        responses.add(
            responses.GET,
            "http://localhost:8888/wp-json",
            status=200,
            json={"key": "value"},
        )
        client = Client("http://localhost:8888/wp-json")

        self.assertEqual(client.get("http://localhost:8888/wp-json"), {"key": "value"})
