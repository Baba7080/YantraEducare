# Generated by Django 3.0.6 on 2021-03-29 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210328_1444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='recomended_by',
            new_name='recommended_by',
        ),
    ]
