# Generated by Django 4.1.3 on 2023-05-25 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_customer_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
