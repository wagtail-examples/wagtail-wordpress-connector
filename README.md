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


### Importer

The importer is a sequence of django management commands. To run the importer:

```
make all
```

This will import the whole sample data set into the Wagtail instance.

The dataset includes:

- Authors
- Categories
- Comments
- Media
- Posts
- Pages
- Tags

You can browse the wordpress site to inspect the imported content.

The setup is now complete and ready for the wordpress content to be transfered to Wagtail. This is done using django-admin actions.

The django admin is at `http://localhost:8000/import-admin`
