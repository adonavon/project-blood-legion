# Generated by Django 3.0 on 2019-12-19 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_blood_legion', '0009_create_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project_blood_legion.Character')),
            ],
        ),
    ]