# Generated by Django 5.0.6 on 2024-06-06 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0008_alter_address_alternative_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='alternative_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
