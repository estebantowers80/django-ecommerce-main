# Generated by Django 4.1 on 2022-08-30 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='identification',
            field=models.CharField(default='', max_length=14, unique=True),
        ),
    ]