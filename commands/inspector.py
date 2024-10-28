import pprint

import requests
import rich_click as click

BASE_ENDPOINT = "http://localhost:8888/wp-json"
ENDPOINTS = {
    "home": "/",
    "posts": "/wp/v2/posts",
    "pages": "/wp/v2/pages",
    "categories": "/wp/v2/categories",
    "tags": "/wp/v2/tags",
    "media": "/wp/v2/media",
    "users": "/wp/v2/users",
    "comments": "/wp/v2/comments",
}
PERPAGE = 100


@click.command()
@click.argument("endpoint", required=False)
@click.option(
    "--all",
    "-a",
    is_flag=True,
    help="Show all records, might need to use the -p option to increase the number of records per page",
)
@click.option(
    "--perpage", "-p", default=PERPAGE, help="Request this number of records per page"
)
@click.option(
    "--record", "-r", default=None, help="Limit the returned record to it's ID number"
)
def i(endpoint, all, perpage, record):
    """
    Use this command to inspect the wordpress API.

    You can use the endpoint argument to specify the endpoint you want to inspect.

    If you don't specify an endpoint, an index of available endpoints will be shown.

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

    if record:
        ENDPOINTS[endpoint] = f"{ENDPOINTS[endpoint]}/{record}"

    try:
        if response := requests.get(
            f"{BASE_ENDPOINT}{ENDPOINTS[endpoint]}?per_page={perpage}"
        ):
            if response.status_code != 200:
                click.echo(f"Error: {response.status_code}")
                return

            if all:
                data = response.json()
                for i, record in enumerate(data):
                    click.echo(click.style(f"Record {i}", fg="blue"))
                    for key, value in record.items():
                        if isinstance(value, dict):
                            click.echo(click.style(f"{key}:", fg="yellow"))
                            click.echo(f"{pprint.pformat(value)}")
                        else:
                            k = click.style(key, fg="yellow")
                            v = click.style(pprint.pformat(value), fg="green")
                            click.echo(f"{k}: {v}")
                return

            if isinstance(data := response.json(), list):
                data = data[0]
            else:
                data = data

            for key, value in data.items():
                if isinstance(value, dict):
                    click.echo(click.style(f"{key}:", fg="yellow"))
                    click.echo(f"{pprint.pformat(value)}")
                else:
                    k = click.style(key, fg="yellow")
                    v = click.style(pprint.pformat(value), fg="green")
                    click.echo(f"{k}: {v}")

    except requests.exceptions.ConnectionError:
        click.echo("Error: Could not connect to the API")
        return
