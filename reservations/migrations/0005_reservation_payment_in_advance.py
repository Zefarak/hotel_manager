# Generated by Django 3.2.10 on 2022-02-17 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_auto_20211120_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='payment_in_advance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]