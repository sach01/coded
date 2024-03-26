# Generated by Django 5.0.2 on 2024-03-25 21:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modern', '0006_remove_owner_owner_type_delete_ownertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='owner',
            name='owner_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='modern.ownertype'),
        ),
    ]
