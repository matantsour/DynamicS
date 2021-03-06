# Generated by Django 3.2.9 on 2022-02-18 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0003_auto_20211228_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='creation',
            name='album_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creations', to='studio.album'),
        ),
        migrations.AlterField(
            model_name='creation',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creations', to='studio.user'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='u_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='employee', serialize=False, to='studio.user'),
        ),
        migrations.AlterField(
            model_name='file',
            name='creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='studio.creation'),
        ),
        migrations.AlterField(
            model_name='file_deletion_history',
            name='creation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deleted_files', to='studio.creation'),
        ),
        migrations.AlterField(
            model_name='login_details',
            name='u_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='login_details', serialize=False, to='studio.user'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='phase_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='studio.phase'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='creation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phases', to='studio.creation'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='phases', to='studio.status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='studio.user_type'),
        ),
        migrations.AlterField(
            model_name='user_type',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='workinghour',
            name='e_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_hours', to='studio.employee'),
        ),
    ]
