# Generated by Django 3.2.9 on 2021-12-18 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0004_alter_workinghour_u_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workinghour',
            old_name='u_id',
            new_name='w_id',
        ),
    ]
