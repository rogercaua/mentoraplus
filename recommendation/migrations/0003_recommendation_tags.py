# Generated by Django 5.2.1 on 2025-05-31 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0002_recommendation_url_alter_recommendation_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='tags',
            field=models.JSONField(default=list),
        ),
    ]
