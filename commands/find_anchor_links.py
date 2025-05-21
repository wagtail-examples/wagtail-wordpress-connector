import argparse
import requests
from bs4 import BeautifulSoup as bs
from colorama import init
from commands.helpers import (
    BASE_ENDPOINT,
    ENDPOINTS,
    display_colored_text,
    show_endpoints,
)

# Initialize colorama
init()


def find_anchor_links(endpoint):
    """
    Find anchor links in WordPress API content.

    Specifically look for anchor links in the response of the content field.
    The anchor links we are interested in are the ones that are not followed by an image tag
    and link to another page on the same site. e.g.
    <a href="http://localhost:8888/2021/08/09/hello-world/">Hello world!</a>
    External links are not of interest.
    """
    # If the endpoint is not in the list, show an error message
    if endpoint not in ENDPOINTS:
        print(f"Endpoint {display_colored_text(endpoint, 'red')} not found")
        return

    url = f"{BASE_ENDPOINT}{ENDPOINTS[endpoint]}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        found_links = False

        for item in data:
            if "content" in item:
                content = item["content"]["rendered"]
                soup = bs(content, "html.parser")

                for a in soup.find_all("a"):
                    next_el = a.next_element
                    if next_el and not next_el.name == "img":
                        href = a.get("href")
                        if href and href.startswith("http://localhost:8888"):
                            found_links = True
                            title = "no title"
                            if item.get("title"):
                                title = item["title"]
                                if isinstance(title, dict) and "rendered" in title:
                                    title = title["rendered"]
                            if item.get("name"):
                                title = item["name"]

                            print(
                                display_colored_text(
                                    f"Title: {title} ID: {item['id']}", "blue"
                                )
                            )
                            print(a)
                            print()

        if not found_links:
            print(display_colored_text("No relevant anchor links found", "yellow"))

    except requests.exceptions.RequestException as e:
        print(display_colored_text(f"Error accessing the API: {e}", "red"))


def main():
    """Main function to handle command line arguments and execute the script."""
    parser = argparse.ArgumentParser(
        description="Find anchor links in WordPress API content."
    )

    parser.add_argument(
        "endpoint",
        nargs="?",
        help="The WordPress API endpoint to inspect. If not provided, will list all available endpoints.",
    )

    args = parser.parse_args()

    if not args.endpoint:
        show_endpoints()
        return

    find_anchor_links(args.endpoint)


if __name__ == "__main__":
    main()
