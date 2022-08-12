# Generated by Django 3.2.14 on 2022-08-12 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField(verbose_name='用户1的 UID')),
                ('uid2', models.IntegerField(verbose_name='用户2的 UID')),
            ],
        ),
        migrations.CreateModel(
            name='Swiperd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(verbose_name='滑动者的 UID')),
                ('sid', models.IntegerField(verbose_name='被滑动者的 UID')),
                ('status', models.CharField(choices=[('superlike', '超级喜欢'), ('like', '喜欢'), ('dislike', '不喜欢')], max_length=32)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
