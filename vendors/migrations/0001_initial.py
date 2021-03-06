# Generated by Django 3.2.8 on 2021-11-12 13:53

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Ενεργό')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Εταιρία')),
                ('owner', models.CharField(blank=True, max_length=200, verbose_name='Ιδιοκτήτης')),
                ('afm', models.CharField(blank=True, max_length=150, verbose_name='ΑΦΜ')),
                ('doy', models.CharField(blank=True, max_length=150, verbose_name='ΔΟΥ')),
                ('phone', models.CharField(blank=True, max_length=200, verbose_name='Σταθερο Τηλεφωνο')),
                ('cellphone', models.CharField(blank=True, max_length=200, verbose_name='Κινητό')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('site', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Λεπτομεριες')),
                ('address', models.CharField(blank=True, max_length=240, null=True, verbose_name='Διευθυνση')),
                ('city', models.CharField(blank=True, max_length=240, null=True, verbose_name='Πολη')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=50, verbose_name='Υπόλοιπο')),
                ('paid_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
                ('taxes_modifier', models.CharField(choices=[('a', 0), ('b', 13), ('c', 24)], default='c', max_length=1)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='VendorBankingAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, verbose_name='Ονομα Δικαιούχου')),
                ('iban', models.CharField(blank=True, max_length=150)),
                ('code', models.CharField(blank=True, max_length=200, verbose_name='Αριθμός Λογαριασμού')),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banking_accounts', to='frontend.paymentmethod', verbose_name='Τροπος Πληρωμής')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bankings', to='vendors.vendor', verbose_name='Προμηθευτής')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Ημερομηνία')),
                ('title', models.CharField(max_length=150, verbose_name='Τίτλος')),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Αξία')),
                ('description', models.TextField(blank=True, verbose_name='Περιγραφή')),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='frontend.paymentmethod', verbose_name='Τροπος Πληρωμής')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='vendors.vendor', verbose_name='Προμηθευτής')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Κατάσταση')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('text', tinymce.models.HTMLField(blank=True)),
                ('vendor_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='vendors.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Ημερομηνια')),
                ('title', models.CharField(max_length=150, verbose_name='Αριθμος Τιμολογιου')),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Καθαρή Αξια')),
                ('extra_value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Επιπλέον Αξία')),
                ('final_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Αξία')),
                ('description', models.TextField(blank=True, verbose_name='Λεπτομεριες')),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='frontend.paymentmethod', verbose_name='Τροπος Πληρωμης')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='vendors.vendor', verbose_name='Προμηθευτης')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=200, verbose_name='Ονομασια')),
                ('phone', models.CharField(blank=True, max_length=10, verbose_name='Τηλεφωνο')),
                ('cellphone', models.CharField(blank=True, max_length=10, verbose_name='Κινητο')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='vendors.vendor', verbose_name='Προμηθευτης')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
