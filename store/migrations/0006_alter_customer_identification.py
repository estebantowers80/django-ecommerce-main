# Generated by Django 4.1 on 2022-08-30 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_customer_identification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='identification',
            field=models.CharField(default='', max_length=13, unique=True),
        ),
    ]