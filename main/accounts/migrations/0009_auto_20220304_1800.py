# Generated by Django 3.2.7 on 2022-03-04 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20220304_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_ref',
            field=models.CharField(default='26634003', max_length=8),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default='22275894460720', max_length=14, primary_key=True, serialize=False),
        ),
    ]