# Generated by Django 5.0.2 on 2024-03-25 18:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modern', '0003_ownertype_alter_owner_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='owner_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='modern.ownertype'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='created_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]