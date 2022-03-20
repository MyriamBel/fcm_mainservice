# Generated by Django 3.2 on 2022-03-20 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Companies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceplace',
            name='servicePlaceDirector',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='seat',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Companies.table'),
        ),
        migrations.AddField(
            model_name='saleplace',
            name='cookingPlace',
            field=models.ManyToManyField(blank=True, to='Companies.CookingPlace'),
        ),
        migrations.AddField(
            model_name='saleplace',
            name='servicePlace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Companies.serviceplace'),
        ),
        migrations.AddField(
            model_name='room',
            name='servicePlace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Companies.serviceplace'),
        ),
        migrations.AddField(
            model_name='franchise',
            name='franchiseFounder',
            field=models.ManyToManyField(blank=True, related_name='franchises', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='franchise',
            name='franchiseOwner',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cookingplace',
            name='servicePlace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Companies.serviceplace'),
        ),
        migrations.AddField(
            model_name='cookingplace',
            name='storeHouse',
            field=models.ManyToManyField(blank=True, to='Companies.StoreHouse'),
        ),
        migrations.AddField(
            model_name='company',
            name='companyDirector',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='companyFounder',
            field=models.ManyToManyField(blank=True, related_name='companies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='franchise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Companies.franchise'),
        ),
    ]