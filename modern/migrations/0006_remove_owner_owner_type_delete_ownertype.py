# Generated by Django 5.0.2 on 2024-03-25 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modern', '0005_alter_ownertype_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='owner_type',
        ),
        migrations.DeleteModel(
            name='OwnerType',
        ),
    ]
