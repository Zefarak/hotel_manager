# Generated by Django 3.0.1 on 2022-02-18 05:20

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_reservation_payment_in_advance'),
        ('customers', '0012_alter_customerpayment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpayment',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservations.Reservation'),
        ),
        migrations.AlterField(
            model_name='customerpayment',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 2, 18, 5, 20, 29, 757734, tzinfo=utc)),
        ),
    ]
