# Generated by Django 3.0 on 2020-01-09 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_blood_legion', '0013_add_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('body', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='member',
            name='rank',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Leader'), (2, 'Officer'), (3, 'Raider'), (4, 'Trial'), (5, 'Member'), (6, 'Friend')]),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.BooleanField()),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project_blood_legion.Member')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_blood_legion.Question')),
            ],
        ),
    ]
