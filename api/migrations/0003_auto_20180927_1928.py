# Generated by Django 2.1.1 on 2018-09-27 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180925_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ccuser',
            old_name='friends',
            new_name='following',
        ),
    ]
