# Generated by Django 3.0 on 2019-12-19 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_blood_legion', '0008_rename_group_to_instance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='guid',
        ),
        migrations.RemoveField(
            model_name='character',
            name='user',
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project_blood_legion.Character')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]