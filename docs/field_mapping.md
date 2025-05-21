# Field Mapping Guide

This guide explains how to create custom field mappings between WordPress and Wagtail models.

## Basic Field Mapping

The `FIELD_MAPPING` attribute in WordPress models is used to map WordPress fields to Wagtail fields:

```python
FIELD_MAPPING = {
    "wp_field_name": "wagtail_field_name",
    "title": "title",
    "content": "body",
    # etc.
}
```

## StreamField Mapping

For WordPress content that should be converted to Wagtail StreamFields, you need to define a `get_streamfield_mapping` method:

```python
def get_streamfield_mapping(self):
    return {
        "content": "body",  # Map WP content to a Wagtail StreamField named "body"
        "excerpt": "intro",  # Map WP excerpt to a StreamField named "intro"
    }
```

## Custom Field Processing

The connector provides field processors for handling content transformations. You can customize these for your specific needs:

### RichText Fields

For processing RichText fields and converting links:

```python
from wp_connector.richtext_field_processor import FieldProcessor

# Use the field processor after transfer
field_processor = FieldProcessor(wordpress_instance)
field_processor.process_fields()
```

### StreamField Data

For converting HTML content to StreamField blocks:

```python
from wp_connector.streamfieldable import StreamFieldable

stream_data = StreamFieldable(
    obj=wordpress_object,
    content=wordpress_object.content
)
wagtail_page.body = stream_data.streamdata
```

## Common Field Mapping Patterns

### Posts to Blog Pages

```python
class WPPost(WordpressModel, ExportableMixin):
    SOURCE_URL = "/wp-json/wp/v2/posts"
    WAGTAIL_PAGE_MODEL = "blog.BlogPage"
    WAGTAIL_PAGE_MODEL_PARENT = "blog.BlogIndexPage"
    FIELD_MAPPING = {
        "title": "title",
        "content": "body",
        "excerpt": "intro",
        "date": "date",
        "slug": "slug",
    }
```

### Pages to Standard Pages

```python
class WPPage(WordpressModel, ExportableMixin):
    SOURCE_URL = "/wp-json/wp/v2/pages"
    WAGTAIL_PAGE_MODEL = "standardpages.StandardPage"
    WAGTAIL_PAGE_MODEL_PARENT = "home.HomePage"
    FIELD_MAPPING = {
        "title": "title",
        "content": "body",
        "slug": "slug",
    }
```

### Media to Images/Documents

```python
class WPMedia(WordpressModel):
    SOURCE_URL = "/wp-json/wp/v2/media"
    # Media handling usually requires custom processing
    # to download files and create Wagtail images/documents
```

## Advanced Configuration

### Handling Custom Fields from WordPress

If your WordPress instance has custom fields (from plugins like Advanced Custom Fields):

1. Ensure the field is exposed in the WordPress REST API
2. Add the field to your WordPress model
3. Include it in your field mapping to the corresponding Wagtail field

### Mapping to Wagtail Snippets

For WordPress data that should become Wagtail snippets:

```python
# When transferring content that relates to this data
def set_custom_relation(self, wagtail_page):
    if custom_data := self.obj.custom_data:
        # Get or create a Wagtail snippet
        custom_snippet, created = CustomSnippet.objects.get_or_create(
            name=custom_data.name,
        )
        # Set the relationship
        wagtail_page.custom_field = custom_snippet
```
