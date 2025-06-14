# Generated by Django 5.1.6 on 2025-03-03 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AdminApp', '0005_sub_categorymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookRegistrationModel',
            fields=[
                ('Bid', models.AutoField(primary_key=True, serialize=False)),
                ('BookName', models.TextField(max_length=100, null=True, unique=True)),
                ('description', models.TextField(max_length=2000, null=True)),
                ('noofpages', models.IntegerField(null=True)),
                ('MRP', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('year', models.DateField(null=True)),
                ('isbn', models.TextField(null=True)),
                ('language', models.TextField(max_length=20, null=True)),
                ('Author', models.TextField(max_length=20, null=True)),
                ('Publisher', models.TextField(max_length=20, null=True)),
                ('Edition', models.TextField(max_length=20, null=True)),
                ('Bookimg', models.ImageField(null=True, upload_to='')),
                ('username', models.TextField(null=True)),
                ('Status', models.TextField(max_length=100, null=True)),
                ('Sub_Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.sub_categorymodel')),
                ('maincategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.categorymodel')),
            ],
        ),
    ]
