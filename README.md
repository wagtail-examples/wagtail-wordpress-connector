# Experimental Wagtail Wordess Importer

This is a importer for WordPress XML files into Wagtail. It is a work in progress and is not yet ready for production use.

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
