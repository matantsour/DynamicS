# Generated by Django 3.2.9 on 2022-04-15 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0013_auto_20220405_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file_deletion_history',
            name='creation_id',
        ),
        migrations.AddField(
            model_name='creationfile',
            name='creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='studio.creation'),
        ),
        migrations.AddField(
            model_name='creationfile',
            name='file_creation_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='creationfile',
            name='audioFile',
            field=models.FileField(upload_to='audios/'),
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='File_Deletion_History',
        ),
    ]
