# Generated by Django 3.1.4 on 2021-03-19 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20210317_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]