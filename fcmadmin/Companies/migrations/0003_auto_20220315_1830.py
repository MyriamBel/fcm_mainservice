# Generated by Django 3.2 on 2022-03-15 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Companies', '0002_companyaccount_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
                ('director', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('isActive', models.BooleanField(default=True, verbose_name='is active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='joining date')),
                ('founder', models.ManyToManyField(blank=True, related_name='franchiseFounder', to=settings.AUTH_USER_MODEL)),
                ('franchiseOwner', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='franchiseOwner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'franchise',
                'verbose_name_plural': 'franchise',
            },
        ),
        migrations.DeleteModel(
            name='CompanyAccount',
        ),
        migrations.AddField(
            model_name='company',
            name='franchise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='companies', to='Companies.franchise'),
        ),
    ]
