# Generated by Django 3.1.7 on 2021-04-07 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20210407_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdetails',
            name='Account_No',
            field=models.CharField(max_length=30, null=True),
        ),
    ]