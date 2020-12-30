# Generated by Django 3.1.4 on 2020-12-14 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_blood_legion', '0018_fix_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boss',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bosses', to='project_blood_legion.zone'),
        ),
    ]