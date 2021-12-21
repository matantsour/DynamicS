# Generated by Django 3.2.9 on 2021-12-21 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('size', models.IntegerField(blank=True, editable=False, null=True)),
                ('length', models.FloatField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Creation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=200)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('profit', models.FloatField()),
                ('album_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='studio.album')),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('phase_id', models.CharField(blank=True, db_column='phase_id', editable=False, max_length=10, primary_key=True, serialize=False)),
                ('placement', models.IntegerField(blank=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('creation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.creation')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('unit_cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=12)),
                ('dob', models.DateField(blank=True, max_length=8, null=True)),
                ('dor', models.DateField(auto_now_add=True, max_length=8, null=True)),
                ('organization', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User_Type',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('u_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='studio.user')),
                ('title', models.CharField(max_length=100)),
                ('wage_method', models.CharField(choices=[('1', 'Hourly'), ('2', 'Monthly'), ('3', 'Flexible'), ('4', 'Per Project'), ('5', 'Unknown')], default='Hourly', max_length=1)),
                ('wage', models.FloatField()),
                ('date_of_start', models.DateField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Login_Details',
            fields=[
                ('u_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='studio.user')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.user_type'),
        ),
        migrations.CreateModel(
            name='Phase_Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_quantity', models.FloatField()),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.phase')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.resource')),
            ],
        ),
        migrations.AddField(
            model_name='phase',
            name='resources',
            field=models.ManyToManyField(blank=True, through='studio.Phase_Resources', to='studio.Resource'),
        ),
        migrations.AddField(
            model_name='phase',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='studio.status'),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('topic', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('attendees', models.ManyToManyField(to='studio.User')),
                ('phase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.phase')),
            ],
        ),
        migrations.CreateModel(
            name='File_Deletion_History',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField(blank=True, max_length=300)),
                ('deletion_date', models.DateField(auto_now=True)),
                ('creation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.creation')),
                ('phase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.phase')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=300)),
                ('file_creation_date', models.DateField(auto_now=True)),
                ('creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='studio.creation')),
            ],
        ),
        migrations.AddField(
            model_name='creation',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='studio.user'),
        ),
        migrations.CreateModel(
            name='WorkingHour',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('working_date', models.DateField()),
                ('stime', models.TimeField()),
                ('etime', models.TimeField()),
                ('e_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.employee')),
            ],
        ),
    ]
