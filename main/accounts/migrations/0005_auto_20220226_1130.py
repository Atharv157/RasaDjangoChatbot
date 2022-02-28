# Generated by Django 3.2.7 on 2022-02-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220220_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='address',
            field=models.CharField(default='111, Vivan Heights, Near Jari Mari Temple, Kalyan', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default='15206712273534', max_length=14, primary_key=True, serialize=False),
        ),
    ]