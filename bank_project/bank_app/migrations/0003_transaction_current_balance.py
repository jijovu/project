# Generated by Django 5.0 on 2024-01-23 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0002_alter_transaction_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='Current_Balance',
            field=models.IntegerField(blank=True, null=True, verbose_name='current_balance'),
        ),
    ]
