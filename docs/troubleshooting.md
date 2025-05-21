# Troubleshooting Guide

## Common Issues

### API Connection Problems

If you're having trouble connecting to the WordPress API:

1. Ensure your WordPress instance has the REST API enabled
2. Check that the API endpoint URLs are correct in your model definitions
3. Verify that authentication is configured properly if your API requires it

### Page Hierarchy Issues

If pages aren't appearing in the correct hierarchy:

1. Run `make wt-fixtree` to repair the Wagtail page tree
2. Ensure parent pages exist before transferring child pages
3. Check that parent-child relationships in WordPress are correctly mapped

### Missing Content After Transfer

If content appears to be missing after transfer:

1. Check the field mappings in your WordPress models
2. Verify that StreamField mappings are correctly configured
3. Look for any errors in the Django admin messages

### Anchor Link Conversion Issues

If anchor links aren't converting properly:

1. Use `find_anchor_links.py` to identify all anchor links in your content
2. Ensure all referenced pages have been transferred to Wagtail first
3. Run the `Update Anchor Links in content fields` action after all pages are transferred

## CLI Command Reference

The project includes several CLI commands to facilitate the migration process:

### WordPress Commands

- `make wp-build` - WordPress: initial setup
- `make wp-up` - WordPress: start the container
- `make wp-load` - WordPress: import the demo data
- `make wp-down` - WordPress: stop the container
- `make wp-destroy` - WordPress: destroy the container

### Wagtail Commands

- `make wt-migrate` - Wagtail: run migrations
- `make wt-superuser` - Wagtail: create superuser
- `make wt-run` - Wagtail: run the server
- `make wt-fixtree` - Wagtail: fix the tree

### Import Commands

- `make import-all` - Django: import all data from WordPress
- `make import-authors` - Django: import authors from WordPress
- `make import-categories` - Django: import categories from WordPress
- `make import-tags` - Django: import tags from WordPress
- `make import-pages` - Django: import pages from WordPress
- `make import-posts` - Django: import posts from WordPress
- `make import-media` - Django: import media from WordPress
- `make import-comments` - Django: import comments from WordPress

### Convenience Commands

- `make start` - Run all commands to set up and start the development environment
- `make stop` - Stop all running services
- `make destroy` - Destroy and cleanup WordPress and Wagtail

### Node.js Commands

- `make node-setup` - Install Node.js dependencies
- `make node-build` - Build all frontend assets for production
- `make node-start` - Start the frontend development server
- `make node-styles` - Compile CSS styles
- `make node-styles-watch` - Watch and compile CSS styles
- `make node-scripts` - Compile JavaScript
- `make node-scripts-watch` - Watch and compile JavaScript
