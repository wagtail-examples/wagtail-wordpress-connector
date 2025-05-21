# Set Up & Usage Guide

You can run this example as a test site for your own WordPress to Wagtail migration.

This example has a WordPress instance with test data and a Wagtail instance with the WordPress connector installed so you can see how the importer works.

## Workflow Overview

The migration process follows these steps:

1. Set up the WordPress instance with test data
2. Set up the Wagtail instance
3. Import WordPress data into Django models
4. Inspect and manage the imported content using the Django admin
5. Transfer selected content to Wagtail using the admin actions
6. Manage the transferred content in Wagtail
7. Create redirects and update anchor links as needed

## Requirements

- Python 3.13+
- UV for dependency management
- Docker for WordPress
- Wagtail 7.0+
- Django 5.2+

## The CLI

The CLI is used to run the example. The CLI is a wrapper around all the parts required to run the example. It uses Docker to run the WordPress instance and Make commands to run the Wagtail/Django instance.

Once you have followed the virtual environment setup instructions below, you can run `make help` to see the available commands.

## WordPress CLI and test data

The WordPress CLI is used to setup and initialize the WordPress instance.

### Create a virtual environment and install the requirements

```bash
# Create a virtual environment using UV
uv venv

# Activate the virtual environment (Linux/macOS)
source .venv/bin/activate

# Activate the virtual environment (Windows)
.venv\Scripts\activate
```

### Start up the WordPress instance and load the test data

Docker is used to run an example WordPress instance with a theme and test data installed. This test data is available for [WordPress Theme Design](https://raw.githubusercontent.com/WPTT/theme-unit-test/master/themeunittestdata.wordpress.xml) and has a lot of content and layouts that may not be appropriate for all use cases for transferring data across to Wagtail but it's a good test bed to get started.

The example has its JSON API enabled so the importer can access the data.

#### Build and initializes the WordPress instance

```bash
make wp-build
```

#### Start the WordPress docker container

```bash
make wp-up
```

#### Load the test data

```bash
make wp-load
```

You can access the WordPress site at `http://localhost:8888` with test data loaded.

You can login to the WordPress admin at `http://localhost:8888/wp-admin` with the username `admin` and password `password`.

## Wagtail and Django

Wagtail and Django are not run in Docker but are run in a virtual environment using UV.

### Initialize and start Wagtail and Django

```bash
make wt-migrate
make wt-superuser
make wt-run
```

You can access the Wagtail site at `http://localhost:8000` with the Wagtail admin at `http://localhost:8000/admin`

The username and password you added above can be used to log into the Wagtail admin.

At this point there is no data in the Wagtail instance. You should see the Wagtail welcome page.

**Important** Go to the Wagtail admin and create a page, under the Home Page, called `Blog` and publish it. This is the parent page for all blog pages and is required by the transfer process. *You can name the page anything you like.*

### Importing the data from WordPress into Django

The importer is a sequence of Django management commands. To run the importer and import all the data from the WordPress instance, run:

```bash
make import-all
```

This will import the whole sample data set into the Django instance.

The dataset includes:

- Authors
- Categories
- Comments
- Media
- Posts
- Pages
- Tags

You can browse the Django admin site to inspect the imported content.

The setup is now complete and ready for the WordPress content to be transferred to Wagtail. This is done using Django-admin actions.

The Django admin for transferring data is at `http://localhost:8000/import-admin`

## Transferring data to Wagtail

Transferring data to Wagtail is done using the Django admin. You can transfer posts and pages.

1. Go to the Django admin at `http://localhost:8000/import-admin`
2. At this time only Posts and Pages are intentionally supported but any linked data such as authors, categories, tags etc. will be transferred to Wagtail snippets and taggit tags.

### Transferring Posts

Posts will need a parent page to be transferred to. First create a page in the Wagtail admin using the BlogIndexPage type. This will be the parent page for all the blog posts.

From this page <http://localhost:8000/import-admin/wp_connector/wppost/>

1. Select the posts you want to transfer (you can select all by clicking the checkbox in the header)
2. Select the action `Create new Wagtail Pages from selected`
3. Click `Go`
4. The posts will be transferred to Wagtail as blog pages

*The list display is limited to 100 items at a time so you may need to use the `Select all` link next to the Go button to select all the posts.*

### Transferring Pages

1. Select the pages you want to transfer (you can select all by clicking the checkbox in the header)
2. Select the action `Create new Wagtail Pages from selected`
3. Click `Go`
4. The pages will be transferred to Wagtail as pages

#### Authors, Categories and Tags

If a WordPress page has foreign keys to data such as authors, categories or tags, the transfer process will create [Wagtail Snippets](https://docs.wagtail.org/en/stable/topics/snippets/index.html) and [taggit tags](https://docs.wagtail.org/en/stable/reference/pages/model_recipes.html#managing-tags-as-snippets) to hold the data and add the appropriate relationships to the Wagtail pages.

### Further actions

These actions are not required but recommended to make the transfer more complete.

#### Redirects

Pages and posts transferred to Wagtail could have slightly different urls/slugs to the original WordPress urls. To handle this, a redirect can be created from the old WordPress url to the new Wagtail url. This should help with SEO and user experience once the site is live.

You can create the redirects using the `Create Wagtail Redirects from selected` action for both posts and pages.

#### Anchor links to Wagtail internal pages

Richtext fields in Wagtail do not support regular anchor links. To handle this you can use the action `Update Anchor Links in content fields` to convert the anchor links to Wagtail internal links.

This works for both single richtext fields and richtext fields within StreamFields.

## Advanced Admin Actions

The import admin interface provides additional actions that can be useful during the WordPress to Wagtail migration process:

### Updating Existing Wagtail Pages

If you've already transferred content to Wagtail but need to update it with changes from WordPress:

1. Select the WordPress content that has already been transferred to Wagtail
2. Choose the action `Update Existing Wagtail Pages`
3. Click `Go`

This will update the corresponding Wagtail pages with any changes from the WordPress content while preserving the Wagtail page IDs.

### Deleting Wagtail Pages

If you need to remove Wagtail pages that were created from WordPress content:

1. Select the WordPress content whose Wagtail pages you want to delete
2. Choose the action `Delete Existing Wagtail Pages from selected`
3. Click `Go`

This will delete the Wagtail pages but keep the WordPress content in Django, allowing you to transfer it again if needed.

### Deleting WordPress Records

To remove WordPress content from the Django database:

1. Select the WordPress content you want to delete
2. Choose the action `Delete WordPress Records from selected`
3. Click `Go`

Note that this action does not delete any corresponding Wagtail pages that might have been created.

## Media Handling

The connector includes support for media files:

- WordPress media items are imported into Django models
- When transferring content to Wagtail, media references can be processed
- Support for featured images and inline images is included
- Note: Media handling is a complex area, and you may need to customize the implementation for your specific needs

## Completion

Once you've transferred all your content to Wagtail, you can remove the WordPress connector module. Your Wagtail site will have no dependencies on the WordPress instance, allowing you to manage it like any other Wagtail site.

## Convenience Commands

The project includes several convenience commands to simplify common tasks:

```bash
# Set up and start everything in one command
make start

# Stop all running services
make stop

# Destroy and cleanup WordPress and Wagtail
make destroy
```

Using `make start` will execute the following commands in sequence:
- WordPress initial setup (wp-build)
- Start WordPress container (wp-up)
- Import WordPress demo data (wp-load)
- Run Wagtail migrations (wt-migrate)
- Create a Wagtail superuser (wt-superuser)
- Import all WordPress data (import-all)
- Start the Wagtail development server (wt-run)

## Frontend Asset Management

The project includes several commands for managing frontend assets:

```bash
# Install Node.js dependencies
make node-setup

# Build all frontend assets for production
make node-build

# Start the frontend development server
make node-start

# Compile CSS styles
make node-styles

# Watch and compile CSS styles
make node-styles-watch

# Compile JavaScript
make node-scripts

# Watch and compile JavaScript
make node-scripts-watch
```

These commands help you manage the frontend assets when customizing the appearance and behavior of your Wagtail site after the WordPress content has been imported.

## Additional Tools

The connector includes several utility tools to help with the migration process:

- `wp_api_inspector.py` - Helps inspect WordPress API endpoints
- `find_anchor_links.py` - Identifies anchor links in WordPress content for conversion
- Field processors for handling richtext content and StreamFields
- Admin views and actions for managing the transfer process

## Customizing the Connector

The connector is designed to be extensible. You may need to customize it for your specific WordPress setup and Wagtail models.

### Model Mapping

Each WordPress model (posts, pages, etc.) can be mapped to a corresponding Wagtail model through configuration attributes:

```python
class WPPost(WordpressModel, ExportableMixin):
    """Model definition for Posts."""

    SOURCE_URL = "/wp-json/wp/v2/posts"
    WAGTAIL_PAGE_MODEL = "blog.BlogPage"
    WAGTAIL_PAGE_MODEL_PARENT = "blog.BlogIndexPage"
    FIELD_MAPPING = {
        "title": "title",
        "content": "body",
        "excerpt": "intro",
        "date": "date",
    }
```

For detailed information on field mapping between WordPress and Wagtail, see the [Field Mapping Guide](./field_mapping.md).

### StreamField Mapping

For WordPress content that should be converted to Wagtail StreamFields:

```python
def get_streamfield_mapping(self):
    return {
        "content": "body",
        "excerpt": "intro",
    }
```

### Custom Field Processing

You can extend the `FieldProcessor` class to handle custom content conversion needs:

```python
from wp_connector.richtext_field_processor import FieldProcessor

class CustomFieldProcessor(FieldProcessor):
    def process_fields(self):
        # Custom processing logic here
        super().process_fields()
```

### Adding Support for Additional WordPress Content Types

To add support for additional WordPress content types:

1. Create a new model class extending `WordpressModel`
2. Define the required attributes (SOURCE_URL, etc.)
3. Register the model with the admin interface
4. Create or modify the corresponding Wagtail model

## Troubleshooting

For help with common issues and a complete command reference, see the [Troubleshooting Guide](./troubleshooting.md).

## Contributing

Contributions to the WordPress to Wagtail connector are welcome! See the [README.md](../README.md) file for details on how to contribute.

## License

This project is licensed under the terms included in the LICENSE file.
