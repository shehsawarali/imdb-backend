# Generated by Django 3.2.6 on 2021-08-25 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="verified",
            field=models.BooleanField(default=0),
        ),
    ]
