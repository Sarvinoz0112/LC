# Generated by Django 5.1.4 on 2025-03-16 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0003_remove_user_is_admin_alter_user_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='is_active',
        ),
    ]
