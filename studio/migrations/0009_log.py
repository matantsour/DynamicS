# Generated by Django 3.2.9 on 2022-03-18 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0008_user_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=300)),
                ('time', models.DateField(auto_now_add=True)),
                ('creation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='studio.creation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='studio.user')),
            ],
        ),
    ]