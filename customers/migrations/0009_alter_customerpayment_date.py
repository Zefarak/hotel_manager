# Generated by Django 3.2.8 on 2021-11-20 05:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_alter_customerpayment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerpayment',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 11, 20, 5, 43, 5, 743184, tzinfo=utc)),
        ),
    ]
