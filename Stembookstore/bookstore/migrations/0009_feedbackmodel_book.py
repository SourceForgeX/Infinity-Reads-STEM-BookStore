# Generated by Django 5.1.6 on 2025-03-31 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0008_remove_feedbackmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackmodel',
            name='book',
            field=models.TextField(default=None, max_length=500, null=True),
        ),
    ]
