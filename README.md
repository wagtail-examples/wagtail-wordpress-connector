# Experimental Wagtail Wordess Importer

This is an experimental project to import WordPress page and posts into Wagtail. It is a work in progress and is not yet ready for production use.

## Requirements

- Python 3.10+ (earlier versions may work)
- Poetry & Docker
- WordPress CLI
- Wordpress Data (currently using a test data set used for building themes)
- Wagtail v6.3 (earlier versions may work)
- Django v5.1 (earlier versions may work)
- Lots of patience :)

## Overall Plan

- To demostrate importing WordPress content into a Django admin instance.
- Be able to alter the imported data if required using the django-admin.
- Be able to export the imported data over to a Wagtail site.
- Exporting crates Pages and Posts that mirror the content from wordpress.

The importer will be a Django management command that will import the data from a WordPress instance and provide a basic admin interface using the django-admin to select and export the data to Wagtail. (posts and pages only at this time, but linked data such as authors, categories, tags, etc. will alos be exported to Wagtail snippets and taggit tags)

A docker container will be used to run a test WordPress instance with a theme and test data. The WordPress CLI will be used to manage the WordPress instance.
The wordpress instance has it's JSON api enabled so the importer can access the data.

The action of transferring the data to Wagtail will done using Django admin actions that export the data to Wagtail. This way the Wagtail site will have no dependency on the WordPress instance and all code will be contained in the wp_connector module. Then once all data is transferred the wp_connector migrations can be rolled back and the module can be removed.

The only module that should be added to your final production site, for creating the page and posts on Wagtail, is the `wp_connector` module, add some temporary configuration to Wagtail and run the importer against your own live WordPress instance, which will need it's JSON api enabled.

## Set Up

### Wagtail and CLI

1. Create a virtual environment and install the requirements:

```
poetry install
```

2. Activate the virtual environment:

```
poetry shell
```

3. Start up the wordress instance and load the test data:

```
wp build
wp up
wp load
```

This gives you a WordPress instance running at `http://localhost:8888` with test data loaded.

The wordpress admin is at `http://localhost:8888/wp-admin` with the username `admin` and password `password`.

4. Initilase and start Wagtail and Django:

```
wt migrate
wt superuser
wt runserver
```

This gives you a Wagtail instance running at `http://localhost:8000` with the Wagtail admin at `http://localhost:8000/admin`

The username and passowrd you added above can be used to log into the Wagtail admin.

#### Importer

The importer is a sequence of django management commands. To run the importer and import all the data from the wordpress instance, run:

```
dj all
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

You can browse the django admin site to inspect the imported content.

The setup is now complete and ready for the wordpress content to be transfered to Wagtail. This is done using django-admin actions.

The django admin is at `http://localhost:8000/import-admin`

## Exporting the data to Wagtail

Exporting data to Wagtail is done using the Django admin.

1. Go to the Django admin at `http://localhost:8000/import-admin`
2. At this time only Posts and Pages are supported but any linked data such as authors, categories, tags ect. will be exported to Wagtail snippets and taggit tags.

### Exporting Posts

From this page <http://localhost:8000/import-admin/wp_connector/wppost/>

1. Select the posts you want to export (you can select all by clicking the checkbox in the header)
2. Select the action `Create new Wagtail from selected`
3. Click `Go`
4. The posts will be exported to Wagtail as blog pages

### Exporting Pages

1. Select the pages you want to export (you can select all by clicking the checkbox in the header)
2. Select the action `Create new Wagtail from selected`
3. Click `Go`
4. The pages will be exported to Wagtail as pages

#### Cateogries and Tags

If a wordpress page has foriegn keys to categories and/or tags, the importer will create Wagtail snippets and taggit tags to hold the data and add the appropriate relationships to the Wagtail pages.

### Further actions

#### Redirects

Pages and posts exported to Wagtail could have slightly different urls/slugs to the original WordPress urls. To handle this, a redirect can be created from the old WordPress url to the new Wagtail url.

You can create the redirects using the `Create Wagtail Redirects from selected` action.

#### Content anchor links

Richtext fields in Wagtail do not support regular anchor links. To handle this you can use the action `Update Anchor Links in content fields` to convert the anchor links to Wagtail internal links.

This works for both single richtext fields and richtext fields within StreamFields.

## Still to do

- Images are not yet imported
- Comments are not yet imported
- and probably lots more I've not yet thought of 😆
