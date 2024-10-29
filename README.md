# Experimental Wagtail Wordess Importer

This is an experimental project to import WordPress page and posts into Wagtail. It is a work in progress and is not yet ready for production use.

## Requirements

- Python 3.10+
- Poetry
- Docker
- WordPress CLI
- Wordpress Theme Test Data
- Wagtail
- Django
- Lots of patience :)

## Overall Plan

The plan is to create a WordPress importer that can import WordPress pages and posts into Wagtail.

The importer will be a Django management command that will import the data from a WordPress instance and provide a basic admin interface using the django-admin to select and export the data to Wagtail. (posts and pages only at this time, but linked data such as authors, categories, tags, etc. will alos be exported to Wagtail snippets and taggit tags)

A docker container will be used to run a test WordPress instance with a theme and test data. The WordPress CLI will be used to manage the WordPress instance.
The wordpress instance has it's JSON api enabled so the importer can access the data.

The action of transferring the data to Wagtail will done using Django admin actions that export the data to Wagtail. This way the Wagtail site will have no dependency on the WordPress instance and all code will be contained in the wp_connector module. Then once all data is transferred the wp_connector migrations can be rolled back and the module can be removed.

The only module that should be added to your final production site, for creating the page and posts ion Wagtail, is the `wp_connector` module, add some temporary configuration to Wagtail and run the importer against your own live WordPress instance, whcih will need it's JSON api enabled.

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

3. Initilase and start Wagtail and Django:

```
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

4. Start up the wordress instance:

```
wp build
wp up
wp load
```

This gives you a WordPress instance running at `http://localhost:8888` with test data loaded.

The wordpress admin is at `http://localhost:8888/wp-admin` with the username `admin` and password `password`.


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
2. Select the items you want to export to Wagtail. At this time only Posts and Pages are supported but any linked data such as authors, categories, tags ect. will be exported to Wagtail snippets and taggit tags.

### Exporting Posts

1. Select the posts you want to export (you can select all by clicking the checkbox in the header)
2. Select the action `Create Wagtail Blog Pages`
3. Click `Go`
4. The posts will be exported to Wagtail as blog pages

### Exporting Pages

1. Select the pages you want to export (you can select all by clicking the checkbox in the header)
2. Select the action `Create Wagtail Pages`
3. Click `Go`
4. The pages will be exported to Wagtail as pages
