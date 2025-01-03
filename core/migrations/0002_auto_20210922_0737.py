# Generated by Django 3.2.6 on 2021-09-22 07:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="principal",
            options={"ordering": ["-title__start_year", "-title__end_year"]},
        ),
        migrations.AddField(
            model_name="person",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="person",
            name="image",
            field=models.ImageField(blank=True, upload_to="person"),
        ),
        migrations.AddField(
            model_name="title",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="title",
            name="image",
            field=models.ImageField(blank=True, upload_to="title"),
        ),
        migrations.AlterField(
            model_name="principal",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="principals",
                to="core.person",
            ),
        ),
        migrations.AlterField(
            model_name="principal",
            name="title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="principals",
                to="core.title",
            ),
        ),
        migrations.AlterField(
            model_name="rating",
            name="title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ratings",
                to="core.title",
            ),
        ),
        migrations.AlterField(
            model_name="rating",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ratings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="core.title",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Crew",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "directors",
                    models.ManyToManyField(
                        blank=True, related_name="directors", to="core.Person"
                    ),
                ),
                (
                    "title",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crew",
                        to="core.title",
                    ),
                ),
                (
                    "writers",
                    models.ManyToManyField(
                        blank=True, related_name="writers", to="core.Person"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "crew",
            },
        ),
    ]
