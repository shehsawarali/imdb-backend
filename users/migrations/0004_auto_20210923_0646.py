# Generated by Django 3.2.6 on 2021-09-23 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("users", "0003_user_follows"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="favorites",
            field=models.ManyToManyField(
                blank=True, related_name="favorites_set", to="core.Title"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(blank=True, upload_to="user"),
        ),
        migrations.AddField(
            model_name="user",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True, related_name="watchlist_set", to="core.Title"
            ),
        ),
    ]
