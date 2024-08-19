# Generated by Django 5.0.8 on 2024-08-17 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_tests_red_line'),
    ]

    operations = [
        migrations.AddField(
            model_name='tests',
            name='count_questions',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tests',
            name='for_who',
            field=models.CharField(choices=[('workers', 'workers'), ('specialists', 'specialists')], max_length=20),
        ),
    ]
