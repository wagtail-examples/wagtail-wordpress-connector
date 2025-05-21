# WordPress to Wagtail Importer (Experimental)

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Wagtail 7.0+](https://img.shields.io/badge/wagtail-7.0+-green.svg)](https://wagtail.org/)
[![Django 5.2+](https://img.shields.io/badge/django-5.2+-orange.svg)](https://www.djangoproject.com/)

This is an experimental project to import WordPress content including pages and posts into Wagtail.

It's not yet ready for production use, but most of the core functionality is in place.

## Features

- Import WordPress pages and posts into a Django application
- Inspect WordPress API endpoints to understand available data
- Transfer selected WordPress content to Wagtail
- Preserve authors, categories, and tags as Wagtail snippets
- Create redirects from WordPress URLs to new Wagtail URLs
- Manage imported content through Wagtail's admin interface

## Requirements

- Python 3.13+
- UV & Docker
- WordPress CLI (installed via Docker)
- WordPress instance with REST API enabled
- Wagtail 7.0+
- Django 5.2+

## Workflow Overview

The migration process follows these steps:

1. Import WordPress data into Django models
2. Manage and curate the imported data using the Django admin
3. Transfer selected content to Wagtail from the Django admin
4. Manage the transferred content in the Wagtail admin
5. Remove the WordPress connector app from the project when finished

![Wagtail site with imported WordPress data](./docs/screen-wagtail.png "Wagtail site with imported WordPress data")

![Wagtail admin for managing imported data](./docs/screen-wagtail-admin.png "Wagtail admin for managing imported data")

### Importing WordPress Data

The importer uses a Django management command to import data from a WordPress instance. While this example imports data from a local WordPress instance, the importer can connect to any WordPress site with the REST API enabled.

To use this for your own site, you'll need to add the `wp_connector` package to your Wagtail project, configure it to point to your WordPress instance, and run the importer.

### WordPress API Inspection

The project includes API inspection tools (`wp_api_inspector.py` and `find_anchor_links.py`) to help you understand the structure of your WordPress data before importing.

### Transferring Data to Wagtail

The Django admin interface provides a way to select and transfer WordPress content to Wagtail:

- Pages and Posts are created as corresponding Wagtail page types
- Authors, Categories, and Tags are created as Wagtail snippets
- Tags integrate with Wagtail's taggit implementation
- Redirects are automatically created from WordPress URLs to Wagtail URLs

![Django Admin for transferring data](./docs/screen-django.png "Django Admin for transferring data")

### Media Handling (Coming Soon)

The transfer process will include handling images and documents:

- Media files will be transferred to the Wagtail media library
- Content references will be updated to point to new Wagtail media URLs
- *Note: This feature is not yet fully implemented*

### Completing the Transfer

Once you've transferred all your content to Wagtail, you can remove the WordPress connector module. Your Wagtail site will have no dependencies on the WordPress instance, allowing you to manage it like any other Wagtail site.

## Project Setup & Usage

For detailed setup instructions, see the [Setup & Usage Guide](./docs/setup.md).

## Todo Items

- Complete media import (images and documents)
- Add comment import functionality
- Improve error handling and reporting during imports
- Add more customization options for content mapping

## Issues & Roadmap

Issues and feature requests are tracked in the [GitHub issues](https://github.com/wagtail-examples/wagtail-wordpress-connector/issues) section.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the terms included in the LICENSE file.
