# Generated by Django 3.2.9 on 2022-04-22 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0011_creationfile_fname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creation',
            name='profit',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='creation',
            name='supervisors',
            field=models.ManyToManyField(blank=True, null=True, related_name='creations', through='studio.Creations_Supervisors', to='studio.Employee'),
        ),
        migrations.AlterField(
            model_name='creationfile',
            name='fname',
            field=models.CharField(blank=True, editable=False, max_length=300, null=True),
        ),
    ]
