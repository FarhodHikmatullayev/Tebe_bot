# Generated by Django 5.0.8 on 2024-08-19 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_alter_results_created_at_alter_tests_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='tests',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
