# Generated by Django 5.2.3 on 2025-07-02 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_messageboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageboard',
            name='name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
