# Generated by Django 3.0 on 2019-12-04 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_blood_legion', '0002_boss_uniqueness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boss',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
