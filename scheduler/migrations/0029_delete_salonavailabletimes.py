# Generated by Django 5.1.4 on 2025-02-16 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0028_alter_salon_owner'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SalonAvailableTimes',
        ),
    ]
