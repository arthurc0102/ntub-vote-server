# Generated by Django 2.1.7 on 2019-03-26 17:00

import app.candidates.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=app.candidates.models.candidate_image_path, verbose_name='照片')),
                ('first_name', models.CharField(max_length=20, verbose_name='名字')),
                ('last_name', models.CharField(max_length=20, verbose_name='姓氏')),
                ('politics', models.TextField(max_length=1000, verbose_name='政見')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.Department', verbose_name='科系')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.Grade', verbose_name='年級')),
                ('klass', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.Class', verbose_name='班級')),
            ],
        ),
    ]
