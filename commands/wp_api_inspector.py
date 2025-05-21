import argparse
import pprint

import requests
from colorama import init
from commands.helpers import (
    BASE_ENDPOINT,
    ENDPOINTS,
    PERPAGE,
    display_colored_text,
    show_endpoints,
)

# Initialize colorama
init()


def inspect_endpoint(endpoint, all_records=False, perpage=PERPAGE, record=None):
    """Inspect a specific WordPress API endpoint."""
    # If the endpoint is not in the list, show an error message
    if endpoint not in ENDPOINTS:
        print(f"Endpoint {endpoint} not found")
        return

    endpoint_url = ENDPOINTS[endpoint]
    if record:
        endpoint_url = f"{endpoint_url}/{record}"

    try:
        response = requests.get(f"{BASE_ENDPOINT}{endpoint_url}?per_page={perpage}")

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return

        data = response.json()

        if all_records and isinstance(data, list):
            for i, record in enumerate(data):
                print(display_colored_text(f"Record {i}", "blue"))
                display_record(record)
            return

        # If not showing all records, display the first one or the single object
        if isinstance(data, list):
            data = data[0]

        display_record(data)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API")


def display_record(record):
    """Display a record with formatted output."""
    for key, value in record.items():
        if isinstance(value, dict):
            print(display_colored_text(f"{key}:", "yellow"))
            print(f"{pprint.pformat(value)}")
        else:
            k = display_colored_text(key, "yellow")
            v = display_colored_text(pprint.pformat(value), "green")
            print(f"{k}: {v}")


def main():
    """Main function to handle command line arguments and execute the inspector."""
    parser = argparse.ArgumentParser(
        description="Use this command to inspect the WordPress API."
    )

    parser.add_argument(
        "endpoint",
        nargs="?",
        help="Specify the endpoint you want to inspect. If not provided, an index of available endpoints will be shown.",
    )

    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Show all records, might need to use the -p option to increase the number of records per page",
    )

    parser.add_argument(
        "--perpage",
        "-p",
        type=int,
        default=PERPAGE,
        help=f"Request this number of records per page (default: {PERPAGE})",
    )

    parser.add_argument(
        "--record", "-r", help="Limit the returned record to its ID number"
    )

    args = parser.parse_args()

    if not args.endpoint:
        show_endpoints()
        return

    inspect_endpoint(args.endpoint, args.all, args.perpage, args.record)


if __name__ == "__main__":
    main()
