# Generated by Django 3.2.14 on 2022-08-14 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_user_vip_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='vip_id',
            field=models.IntegerField(default=1),
        ),
    ]