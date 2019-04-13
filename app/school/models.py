from django.db import models


class Department(models.Model):
    name = models.CharField('科系', max_length=15, unique=True)

    def __str__(self):
        return self.name
