# Generated by Django 5.0.2 on 2024-04-20 21:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modern', '0005_bank'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='received_by',
        ),
        migrations.AddField(
            model_name='bank',
            name='banked_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='banker', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bank',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receive', to=settings.AUTH_USER_MODEL),
        ),
    ]
