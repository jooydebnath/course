# Generated by Django 3.2.9 on 2021-11-23 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_payment_usercourse'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
