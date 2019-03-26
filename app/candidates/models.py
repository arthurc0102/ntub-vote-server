import os
import time

from django.db import models

from app.elections.models import Pool
from app.school.models import System, Department, Grade, Class


def candidate_image_path(instance, filename):
    ext = os.path.splitext(filename)[-1]
    now = str(time.time()).replace('.', '')
    full_name = instance.full_name()
    return os.path.join('candidate', '{}-{}{}'.format(now, full_name, ext))


class Candidate(models.Model):
    image = models.ImageField('照片', upload_to=candidate_image_path)
    first_name = models.CharField('名字', max_length=20)
    last_name = models.CharField('姓氏', max_length=20)
    system = models.ForeignKey(System, models.PROTECT, verbose_name='學制')
    department = models.ForeignKey(Department, models.PROTECT, verbose_name='科系')  # NOQA
    grade = models.ForeignKey(Grade, models.PROTECT, verbose_name='年級')
    klass = models.ForeignKey(Class, models.PROTECT, verbose_name='班級')
    politics = models.TextField('政見', max_length=1000)
    pool = models.ForeignKey(Pool, models.PROTECT, verbose_name='選舉類型')

    def __str__(self):
        return self.full_name()

    def full_name(self, swap=False, between=''):
        first_name = self.first_name
        last_name = self.last_name

        if swap:
            first_name, last_name = last_name, first_name
            between = ' '

        return '{}{}{}'.format(last_name, between, first_name)
