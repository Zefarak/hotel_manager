# Generated by Django 3.2.8 on 2021-11-14 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20211114_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='extra_charges',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='ΕΠΙΠΛΕΟΝ ΤΙΜΗ'),
        ),
        migrations.AlterField(
            model_name='roomcharge',
            name='room',
            field=models.ManyToManyField(blank=True, null=True, related_name='my_extras', to='rooms.Room', verbose_name='ΔΩΜΑΤΙΟ'),
        ),
    ]
