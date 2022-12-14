# Generated by Django 3.2.14 on 2022-08-08 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_profile_dating_sex'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone',
            new_name='phonenum',
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_month',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_year',
            field=models.IntegerField(default=2000),
        ),
    ]
