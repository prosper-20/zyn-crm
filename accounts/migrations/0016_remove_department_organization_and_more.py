# Generated by Django 4.2.13 on 2024-07-16 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_otptoken_otp_code_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='organization',
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='3346', max_length=4),
        ),
    ]
