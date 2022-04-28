# Generated by Django 3.2.8 on 2021-11-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0007_auto_20211120_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomcharge',
            name='day_charge',
            field=models.BooleanField(default=False, verbose_name='ΧΡΕΩΣΗ ΑΝΑ ΗΜΕΡΑ'),
        ),
        migrations.AlterField(
            model_name='roomcharge',
            name='capacity',
            field=models.BooleanField(default=False, verbose_name='ΧΡΕΩΣΗ ΑΝΑ ΑΤΟΜΟ'),
        ),
        migrations.AlterField(
            model_name='roomcharge',
            name='room',
            field=models.ManyToManyField(blank=True, null=True, related_name='my_extras', to='rooms.Room', verbose_name='ΔΩΜΑΤΙΑ'),
        ),
        migrations.AlterField(
            model_name='roomcharge',
            name='title',
            field=models.CharField(max_length=230, unique=True, verbose_name='ΤΙΤΛΟΣ'),
        ),
        migrations.AlterField(
            model_name='roomcharge',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='ΑΞΙΑ'),
        ),
    ]