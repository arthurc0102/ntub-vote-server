from django.db import models


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
    std_no = models.CharField('學號', max_length=15, unique=True)
    groups = models.ManyToManyField(Group, verbose_name='群組')

    class Meta:
        verbose_name = '學生'
        verbose_name_plural = '學生'

    def __str__(self):
        return self.std_no
