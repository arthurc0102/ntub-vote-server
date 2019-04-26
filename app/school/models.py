from django.db import models


class Department(models.Model):
    name = models.CharField('科系', max_length=15, unique=True)

    class Meta:
        verbose_name = '科系'
        verbose_name_plural = '科系'

    def __str__(self):
        return self.name
