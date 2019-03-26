from django.db import models


class System(models.Model):
    name = models.CharField('學制', max_length=15, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField('科系', max_length=15, unique=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField('年級', max_length=15, unique=True)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField('班級', max_length=15, unique=True)

    def __str__(self):
        return self.name
