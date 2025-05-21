"""
Helper functions and constants for WordPress API inspection commands.
"""

import os
from colorama import Fore, Style

# Base endpoint for WordPress API
BASE_ENDPOINT = os.environ.get("WP_API_ENDPOINT", "http://localhost:8888/wp-json")

# Default number of records per page
PERPAGE = 100

# Endpoints available in the WordPress API
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


def display_colored_text(text, color):
    """Helper function to display colored text."""
    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
    }
    return f"{colors.get(color, '')}{text}{Style.RESET_ALL}"


def show_endpoints():
    """Display all available endpoints."""
    print("Available endpoints:")
    for key in ENDPOINTS:
        k = display_colored_text(key, "yellow")
        v = display_colored_text(ENDPOINTS[key], "green")
        print(f"{k} : {v}")
    help_text = display_colored_text(
        "Use the --help option for more information", "red"
    )
    print(help_text)
