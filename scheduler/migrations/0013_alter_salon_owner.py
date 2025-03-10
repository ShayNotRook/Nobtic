# Generated by Django 5.1.3 on 2024-12-21 14:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0012_alter_salon_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='salon',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='salon', to=settings.AUTH_USER_MODEL),
        ),
    ]
