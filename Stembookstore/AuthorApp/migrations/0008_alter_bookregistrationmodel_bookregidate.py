# Generated by Django 5.1.6 on 2025-03-24 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthorApp', '0007_alter_bookregistrationmodel_bookregidate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookregistrationmodel',
            name='BookRegidate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
