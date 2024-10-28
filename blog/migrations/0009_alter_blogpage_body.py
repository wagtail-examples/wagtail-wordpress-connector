# Generated by Django 5.1.2 on 2024-10-28 17:36

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0008_alter_blogpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.StreamField(
                [("paragraph", 0)],
                blank=True,
                block_lookup={0: ("wagtail.blocks.RichTextBlock", (), {})},
            ),
        ),
    ]
