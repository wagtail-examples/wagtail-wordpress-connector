import requests

from wp_connector.messages import ClientExitException, ClientMessage


class Client:
    """A client for the WordPress REST API.
    On been instantiated, the client will fetch the first page of the endpoint.

    It will set the following class properties that can be used to determine:
    - is_paged: True if the endpoint is paged, False otherwise.
    - total_pages: The total number of pages.
    - total_results: The total number of results.
    - paged_endpoints: A list of URLs that can be fetched.

    Calling the get() method will return the JSON response from the endpoint.
    """

    def __init__(self, url):
        self.client_exception = ClientExitException()
        self.client_message = ClientMessage()
        self.url = url

        # Test that the _session can be created
        # e.g. the server is alive
        self._session = requests.Session()
        try:
            self._session.get(self.url)
        except requests.exceptions.ConnectionError:
            self.client_exception.error_message(f"Could not connect to {self.url}")

        # Fetch the first page of the endpoint and
        # set the data for the class properties
        try:
            self.response = self._session.get(self.url)
            if self.response.status_code != 200:
                self.client_exception.error_message(
                    f"Could not connect to {self.url} the status code is {self.response.status_code}"
                )
            self.client_message.success_message(f"Connected to {self.url}")
        except ClientExitException as e:
            self.client_exception.error_message(
                f"Could not connect to {self.url} the error is {e}"
            )

    def get(self, url):
        try:
            response = self._session.get(url)
            if response.status_code != 200:
                self.client_exception.error_message(
                    f"Could not connect to {url} the status code is {response.status_code}"
                )
            return response.json()
        except ClientExitException as e:
            self.client_exception.error_message(
                f"Could not connect to {url} the error is {e}"
            )

    @property
    def is_paged(self):
        """Return True if the endpoint is paged, False otherwise."""
        return "X-WP-TotalPages" in self.response.headers

    @property
    def get_total_pages(self):
        """Return the total number of pages."""
        return int(self.response.headers["X-WP-TotalPages"])

    @property
    def get_total_results(self):
        """Return the total number of results."""
        return int(self.response.headers["X-WP-Total"])

    @property
    def paged_endpoints(self):
        """Generate a list of URLs that can be fetched.
        The 'page' parameter is always appended to the URL.
        Returns:
            A list of URLs.
        Example:
            [
                "https://foo.com/endpoint/bar/baz?page=1",
                "https://foo.com/endpoint/bar/baz?page=2",
            ]
        """

        total_pages = self.get_total_pages

        return [f"{self.url}?page={index}" for index in range(1, total_pages + 1)]
