# Generated by Django 3.2.8 on 2021-11-12 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(choices=[('a', 'WebHotelier'), ('b', 'Social Media'), ('c', 'Email'), ('d', 'Τηλεφωνο'), ('e', 'Site'), ('f', 'Αλλο')], default='a', max_length=1)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('checkIn', models.BooleanField(default=False)),
                ('isCancel', models.BooleanField(default=False)),
                ('isDone', models.BooleanField(default=False)),
                ('capacity', models.IntegerField(default=1, verbose_name='ΑΤΟΜΑ')),
                ('clean_value', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='ΣΥΝΟΛΙΚΗ ΑΞΙΑ ΔΩΜΑΤΙΟΥ')),
                ('extra_cost_per_person', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='ΣΥΝΟΛΙΚΗ ΑΞΙΑ ΕΠΙΠΛΕΟΝ ΑΤΟΜΩΝ')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Total Value')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='ΕΚΠΤΩΣΗ')),
                ('days', models.IntegerField(default=1)),
                ('final_value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='customers.customer')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='rooms.room')),
            ],
            options={
                'ordering': ['-check_in', 'checkIn'],
            },
        ),
    ]