# Generated by Django 4.2.6 on 2023-10-11 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEL4C', '0002_user_academic_user_discipline_alter_user_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='act4',
            name='retro',
        ),
        migrations.RemoveField(
            model_name='actfinal',
            name='pitch',
        ),
        migrations.AddField(
            model_name='act4',
            name='link',
            field=models.CharField(blank=True, max_length=510, null=True),
        ),
        migrations.AddField(
            model_name='actfinal',
            name='link',
            field=models.CharField(blank=True, max_length=510, null=True),
        ),
    ]