# Generated by Django 3.2.14 on 2022-08-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_profile_dating_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(default='北京', max_length=32, verbose_name='目标城市'),
        ),
    ]