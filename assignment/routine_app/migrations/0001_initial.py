# Generated by Django 4.0.6 on 2022-08-05 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='routine',
            fields=[
                ('routine_id', models.IntegerField(primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('MC', 'MIRACLE'), ('HW', 'HOMEWORK')], max_length=2)),
                ('goal', models.TextField(default='', null=True)),
                ('is_alarm', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='routine_result',
            fields=[
                ('routine_result_id', models.IntegerField(primary_key=True, serialize=False)),
                ('result', models.CharField(choices=[('N', 'NOT'), ('T', 'TRY'), ('D', 'DONE')], max_length=1)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('routine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routine', to='routine_app.routine')),
            ],
        ),
        migrations.CreateModel(
            name='routine_day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('routine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='routine_app.routine')),
            ],
        ),
    ]
