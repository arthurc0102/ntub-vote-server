import os
import time

from django.core.exceptions import ValidationError
from django.db import models

from app.elections.models import Pool, Vote
from app.school.services import get_student_info


def candidate_image_path(instance, filename):
    ext = os.path.splitext(filename)[-1]
    now = str(time.time()).replace('.', '')
    full_name = str(instance)
    return os.path.join('candidate', '{}-{}{}'.format(now, full_name, ext))


class Candidate(models.Model):
    image = models.ImageField('照片', upload_to=candidate_image_path)
    std_no = models.CharField('學號', max_length=15)
    name = models.CharField('姓名', max_length=30)
    klass = models.CharField('課程', max_length=30)
    politics = models.TextField('政見', max_length=1000, blank=True)
    pool = models.ForeignKey(
        Pool,
        models.PROTECT,
        'candidates',
        verbose_name='選舉類型',
    )

    class Meta:
        verbose_name = '候選人'
        verbose_name_plural = '候選人'
        unique_together = (
            ('std_no', 'pool'),
        )

    def __str__(self):
        return f'選舉 {self.pool_id}-{self.std_no}-{self.name}'

    def clean(self):
        if Vote.objects.filter(candidate__pool=self.pool).count() > 0:
            raise ValidationError('這個選舉已經開始投票，所以無法更新或新增候選人。')

        try:
            info = get_student_info(self.std_no, ['std_name', 'class_name'])
        except Exception:
            raise ValidationError({'std_no': '這個學號不合法或不存在。'})

        self.name = info['std_name']
        self.klass = info['class_name']
