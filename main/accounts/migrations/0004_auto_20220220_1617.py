# Generated by Django 3.2.7 on 2022-02-20 10:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220206_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default='26439829720619', max_length=14, primary_key=True, serialize=False),
        ),
    ]
