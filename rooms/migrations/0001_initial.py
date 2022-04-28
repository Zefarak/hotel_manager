# Generated by Django 3.2.8 on 2021-11-12 13:53

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='ΚΑΤΑΣΤΑΣΗ')),
                ('used', models.BooleanField(default=False, verbose_name='ΧΡΗΣΙΜΟΠΟΙΕΙΤΑΙ')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='ΤΙΤΛΟΣ')),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='ΒΑΣΙΚΗ ΤΙΜΗ')),
                ('notes', tinymce.models.HTMLField(blank=True)),
                ('capacity', models.IntegerField(default=2)),
                ('extra_value_per_person', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='RoomPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='ΤΙΤΛΟΣ')),
                ('active', models.BooleanField(default=True, verbose_name='ΚΑΤΑΣΤΑΣΗ')),
                ('value_type', models.CharField(choices=[('a', 'Έκπτωση σε %'), ('b', '+/- Προσθήκη στην Βασική τιμή'), ('c', 'Καρφωτή Τιμή')], default='a', max_length=1, verbose_name='ΕΙΔΟΣ ΔΙΑΦΟΡΟΠΟΙΗΣΗΣ ΤΙΜΗΣ')),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='ΑΞΙΑ')),
                ('minimum_days', models.IntegerField(default=0, verbose_name='ΕΛΑΧΙΣΤΕΣ ΜΕΡΕΣ')),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='ΤΙΜΗ ΔΩΜΑΤΙΟΥ')),
                ('extra_value_per_person', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('room', models.ManyToManyField(related_name='extra_prices', to='rooms.Room', verbose_name='ΔΩΜΑΤΙΟ')),
            ],
            options={
                'ordering': ['date_start'],
            },
        ),
    ]
