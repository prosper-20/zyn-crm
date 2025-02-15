# Generated by Django 4.2.13 on 2024-07-10 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customeraccount_shipping_post_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraccount',
            name='billing_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.city'),
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='shipping_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='shipping_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_shipping_city', to='accounts.city'),
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='shipping_post_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='shipping_state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='9882', max_length=4),
        ),
    ]
