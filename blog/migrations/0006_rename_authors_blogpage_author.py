# Generated by Django 5.1.2 on 2024-10-20 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_remove_blogpage_authors_blogpage_authors"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blogpage",
            old_name="authors",
            new_name="author",
        ),
    ]
