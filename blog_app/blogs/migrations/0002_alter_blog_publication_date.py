# Generated by Django 5.1 on 2024-08-30 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='publication_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
