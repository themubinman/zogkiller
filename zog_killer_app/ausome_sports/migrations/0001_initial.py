# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 15:25
from __future__ import unicode_literals

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
            name='AusomeUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('sex', models.CharField(choices=[('M', 'Male'), ('W', 'Female')], max_length=6)),
                ('email', models.CharField(max_length=100)),
                ('picture', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(max_length=100)),
                ('bio', models.CharField(blank=True, max_length=500, null=True)),
                ('visible_in_directory', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('location', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('sport', models.CharField(choices=[('volleyball', 'Volleyball')], max_length=20)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=2)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reg_date', models.DateField()),
                ('day_of_week', models.CharField(max_length=100)),
                ('indoor_outdoor', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('location', models.TextField()),
                ('difficulty', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('team_max', models.IntegerField()),
                ('team_price', models.CharField(max_length=10)),
                ('individual_price', models.CharField(max_length=10)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.Game')),
            ],
        ),
        migrations.CreateModel(
            name='PendingTeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('team_type', models.CharField(choices=[('R', 'Random'), ('U', 'User generated')], max_length=15)),
                ('open_registration', models.BooleanField(default=False)),
                ('team_password', models.CharField(blank=True, max_length=50, null=True)),
                ('player_max', models.IntegerField()),
                ('payment_plan', models.CharField(choices=[('team whole', 'team whole'), ('team per person', 'team per person'), ('individual', 'individual')], max_length=20)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.AusomeUser')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.League')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_captain', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.AusomeUser')),
            ],
        ),
        migrations.CreateModel(
            name='Win',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.Game')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.Team')),
            ],
        ),
        migrations.AddField(
            model_name='pendingteammember',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.Team'),
        ),
        migrations.AddField(
            model_name='pendingteammember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.AusomeUser'),
        ),
        migrations.AddField(
            model_name='loss',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ausome_sports.League'),
        ),
        migrations.AddField(
            model_name='game',
            name='teams',
            field=models.ManyToManyField(to='ausome_sports.Team'),
        ),
    ]
