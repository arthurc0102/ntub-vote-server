# Generated by Django 2.2 on 2019-04-26 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0009_auto_20190414_1435'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pool',
            options={'verbose_name': '選舉', 'verbose_name_plural': '選舉'},
        ),
        migrations.AlterModelOptions(
            name='time',
            options={'verbose_name': '選舉時間', 'verbose_name_plural': '選舉時間'},
        ),
        migrations.AlterModelOptions(
            name='vote',
            options={'verbose_name': '選票', 'verbose_name_plural': '選票'},
        ),
    ]