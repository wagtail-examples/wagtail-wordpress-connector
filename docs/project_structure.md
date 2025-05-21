# Project Structure Guide

This document provides an overview of the WordPress to Wagtail Connector project structure and its key components.

## Directory Structure

```
wagtail-wordpress-connector/
├── app/                   # Wagtail application code
│   ├── blog/              # Blog page models
│   ├── home/              # Home page models
│   ├── search/            # Search functionality
│   ├── settings/          # Django settings
│   ├── static_compiled/   # Compiled static files
│   ├── static_src/        # Source static files
│   ├── style_guide/       # Style guide app
│   └── templates/         # Global templates
├── commands/              # CLI commands and utilities
│   ├── find_anchor_links.py  # Tool to identify anchor links
│   └── wp_api_inspector.py   # Tool to inspect WordPress API
├── docs/                  # Documentation files
├── scripts/               # JavaScript build scripts
├── wordpress.docker/      # WordPress Docker setup
├── wordpress.testdata/    # Test data for WordPress
└── wp_connector/          # WordPress connector app
    ├── management/        # Django management commands
    ├── migrations/        # Database migrations
    ├── models/            # Django models for WordPress data
    ├── templates/         # Connector templates
    └── tests/             # Test suite
```

## Key Components

### wp_connector

The core of the connector is the `wp_connector` app which contains:

- **Models** (`models/`): Django models that represent WordPress content types
- **Importer** (`importer.py`): Handles importing data from WordPress API
- **Exporter** (`exporter.py`): Handles exporting WordPress data to Wagtail
- **Admin interface** (`admin.py`): Custom Django admin interface for managing imports
- **RichText Field Processor** (`richtext_field_processor.py`): Handles content conversion
- **StreamField Converter** (`streamfieldable.py`): Converts WordPress HTML to Wagtail StreamFields

### Commands

The `commands` directory contains utility scripts:

- **wp_api_inspector.py**: Tool to inspect WordPress API endpoints
- **find_anchor_links.py**: Tool to identify anchor links in WordPress content

### Wagtail App

The `app` directory contains the Wagtail application:

- **blog**: Blog page models that WordPress posts are mapped to
- **home**: Home page models that WordPress pages can be mapped to

## Flow of Data

The WordPress to Wagtail migration follows this general flow:

1. **Import**: Data is imported from WordPress API into Django models
   - WordPress content is saved in Django models in the `wp_connector` app
   - Foreign keys and relationships between content are preserved

2. **Transfer**: Data is transferred from Django models to Wagtail
   - WordPress content is mapped to Wagtail pages and snippets
   - Content is transformed as needed (HTML to StreamFields, etc.)
   - Relationships are re-established in Wagtail

3. **Post-processing**: Additional tasks are performed
   - Redirects are created from WordPress URLs to Wagtail URLs
   - Anchor links are converted to Wagtail internal links
   - Media files are processed and added to Wagtail media library

## Custom Extension Points

The connector is designed to be extended in several ways:

- **Model Mapping**: Define how WordPress models map to Wagtail models
- **Field Mapping**: Define how WordPress fields map to Wagtail fields
- **Content Processing**: Customize how content is processed during transfer
- **Streamfield Mapping**: Define how WordPress content is converted to StreamFields
