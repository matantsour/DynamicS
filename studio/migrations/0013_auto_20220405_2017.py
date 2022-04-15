# Generated by Django 3.2.9 on 2022-04-05 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0012_creationfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creationfile',
            name='image',
        ),
        migrations.AddField(
            model_name='creationfile',
            name='audioFile',
            field=models.FileField(default='null', upload_to='musics/'),
            preserve_default=False,
        ),
    ]