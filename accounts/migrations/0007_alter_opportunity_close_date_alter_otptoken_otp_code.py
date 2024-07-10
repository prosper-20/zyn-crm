# Generated by Django 4.2.13 on 2024-07-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customeraccount_account_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='close_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='3733', max_length=4),
        ),
    ]
