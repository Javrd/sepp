# Generated by Django 2.0.3 on 2018-04-16 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='paypalId',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
