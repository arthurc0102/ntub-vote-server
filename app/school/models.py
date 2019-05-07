from django.core.validators import RegexValidator
from django.db import models


STD_NO_PATTERN = \
    '(?P<night>[N|n]?)' \
    '(?P<year>[0-9]{2,3})' \
    '(?P<system>[1-9])' \
    '(?P<department>[1-9A-Za-z])' \
    '(?P<class>[0-9]?)' \
    '(?P<no>[0-9]{2})'


class Department(models.Model):
    name = models.CharField('科系', max_length=15, unique=True)

    class Meta:
        verbose_name = '科系'
        verbose_name_plural = '科系'

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField('群組名稱', max_length=15, unique=True)

    class Meta:
        verbose_name = '群組'
        verbose_name_plural = '群組'

    def __str__(self):
        return self.name


class Student(models.Model):
    std_no = models.CharField(
        '學號',
        max_length=15,
        unique=True,
        validators=[RegexValidator(STD_NO_PATTERN, '不合法的學號')],
    )
    groups = models.ManyToManyField(Group, verbose_name='群組')

    class Meta:
        verbose_name = '學生'
        verbose_name_plural = '學生'

    def __str__(self):
        return self.std_no
