import requests
import rich_click as click
from bs4 import BeautifulSoup as bs

from .inspector import BASE_ENDPOINT, ENDPOINTS


@click.command()
@click.argument("endpoint", required=False)
def a(endpoint):
    """
    Use this command to inspect the wordpress API.

    Specifically look for anchor links in the response of the content field.
    Ths anchor links we are interested in are the ones that are not followed by an image tag
    and link to another page on the same site. e.g.
    <a href="http://localhost:8888/2021/08/09/hello-world/">Hello world!</a>
    External links are not of interest.
    """
    # If there's no endpoint, show all available endpoints
    if not endpoint:
        for key in ENDPOINTS:
            k = click.style(key, fg="yellow")
            v = click.style(ENDPOINTS[key], fg="green")
            click.echo(f"{k} : {v}")
        help_text = click.style("Use the --help option for more information", fg="red")
        click.echo(help_text)
        return

    # If the endpoint is not in the list, show an error message
    if endpoint not in ENDPOINTS:
        click.echo(f"Endpoint {endpoint} not found")
        return

    url = f"{BASE_ENDPOINT}{ENDPOINTS[endpoint]}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    for item in data:
        if "content" in item:
            content = item["content"]["rendered"]
            # if "<a" in content:
            soup = bs(content, "html.parser")
            for a in soup.find_all("a"):
                next_el = a.next_element
                if next_el and not next_el.name == "img":
                    href = a.get("href")
                    if href and href.startswith("http://localhost:8888"):
                        title = "no title"
                        if item.get("title"):
                            title = item["title"]
                        if item.get("name"):
                            title = item["name"]
                        click.echo(f"Title: {title} ID: {item['id']}")
                        click.echo(a)
                        click.echo("\n")
