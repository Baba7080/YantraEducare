# Generated by Django 3.1.7 on 2021-04-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210407_0720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountdetails',
            old_name='Account_No',
            new_name='Account_Number',
        ),
        migrations.RenameField(
            model_name='accountdetails',
            old_name='Google_Pay',
            new_name='Bank_Name',
        ),
        migrations.RemoveField(
            model_name='accountdetails',
            name='Name_of_Bank',
        ),
        migrations.RemoveField(
            model_name='accountdetails',
            name='Paytm_No',
        ),
        migrations.RemoveField(
            model_name='accountdetails',
            name='Phonepe_No',
        ),
        migrations.RemoveField(
            model_name='accountdetails',
            name='Re_Account_No',
        ),
        migrations.AddField(
            model_name='accountdetails',
            name='Google_Pay_Number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='accountdetails',
            name='Paytm_Number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='accountdetails',
            name='Phonepe_Number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='accountdetails',
            name='Re_Enter_Account_Number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='accountdetails',
            name='UPI_ID',
            field=models.EmailField(max_length=30, null=True),
        ),
    ]