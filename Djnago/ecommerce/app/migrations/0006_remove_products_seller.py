# Generated by Django 4.2.10 on 2024-02-12 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_products_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='seller',
        ),
    ]
