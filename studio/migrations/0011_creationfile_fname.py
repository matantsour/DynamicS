# Generated by Django 3.2.9 on 2022-04-15 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0010_auto_20220415_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='creationfile',
            name='fname',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
