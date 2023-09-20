# Generated by Django 4.2.4 on 2023-09-19 13:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=250)),
                ('time', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('ip', models.CharField(max_length=250)),
            ],
        ),
    ]
