# Generated by Django 3.2.8 on 2021-11-12 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Ονομασια')),
                ('category', models.CharField(choices=[('a', 'Αντικαταβολή'), ('b', 'Τραπεζική ΚατάΘεση')], max_length=1, verbose_name='Κατηγορια')),
            ],
        ),
    ]
