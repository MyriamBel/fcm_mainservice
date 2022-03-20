# Generated by Django 3.2 on 2022-03-20 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Regions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='CookingPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
            ],
            options={
                'verbose_name': 'place of sale',
                'verbose_name_plural': 'places of sale',
            },
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
            ],
            options={
                'verbose_name': 'franchise',
                'verbose_name_plural': 'franchise',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
            ],
            options={
                'verbose_name': 'room',
                'verbose_name_plural': 'rooms',
            },
        ),
        migrations.CreateModel(
            name='SalePlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
            ],
            options={
                'verbose_name': 'place of sale',
                'verbose_name_plural': 'places of sale',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
            ],
            options={
                'verbose_name': 'seat',
                'verbose_name_plural': 'seats',
            },
        ),
        migrations.CreateModel(
            name='ServicePlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
                ('street', models.CharField(blank=True, max_length=100, verbose_name='street')),
                ('houseNumber', models.CharField(blank=True, max_length=10, verbose_name='house number')),
                ('roomNumber', models.CharField(blank=True, max_length=10, verbose_name='number room')),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, verbose_name='latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, verbose_name='longitude')),
                ('noteAddress', models.CharField(blank=True, max_length=100, verbose_name='notes to the address')),
                ('about', models.CharField(blank=True, max_length=300, verbose_name='about object')),
                ('city', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='Regions.city')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Companies.company')),
            ],
            options={
                'verbose_name': 'service point',
                'verbose_name_plural': 'service points',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
                ('shape', models.CharField(choices=[('cir', 'circle'), ('rec', 'rectangular')], default='rec', max_length=3, verbose_name='table shape')),
                ('minCapacity', models.IntegerField(verbose_name='minimum number of guests')),
                ('maxCapacity', models.IntegerField(verbose_name='maximum number of guests')),
                ('reservable', models.BooleanField(default=True, verbose_name='reservable')),
                ('isBusy', models.BooleanField(default=False, verbose_name='is busy')),
                ('reservationStart', models.DateTimeField(verbose_name='datetime of the start of the reservation')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Companies.room')),
            ],
            options={
                'verbose_name': 'table',
                'verbose_name_plural': 'tables',
            },
        ),
        migrations.CreateModel(
            name='StoreHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
                ('description', models.CharField(blank=True, max_length=300)),
                ('servicePlace', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Companies.serviceplace')),
            ],
            options={
                'verbose_name': 'storehouse',
                'verbose_name_plural': 'storehouse',
            },
        ),
    ]
