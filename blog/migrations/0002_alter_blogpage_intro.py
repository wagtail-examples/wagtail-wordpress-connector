# Generated by Django 5.1.2 on 2024-10-20 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='intro',
            field=models.TextField(max_length=750),
        ),
    ]
