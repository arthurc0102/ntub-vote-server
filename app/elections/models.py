from django.core.exceptions import ValidationError
from django.db import models

from app.school.models import Department


class Time(models.Model):
    start_at = models.DateTimeField('開始時間')
    end_at = models.DateTimeField('結束時間')

    def __str__(self):
        return '{} - {}'.format(self.start_at, self.end_at)

    def clean(self):
        if self.start_at > self.end_at:
            raise ValidationError('Start should be smaller than end.')

        if Time.objects.exists() and not self.pk:
            raise ValidationError('Time should only have one record.')


class Pool(models.Model):
    name = models.CharField('選舉類型', max_length=50, unique=True)
    departments = models.ManyToManyField(Department, verbose_name='可參與科系')

    def __str__(self):
        return self.name


class Vote(models.Model):
    email = models.EmailField('電子郵件')
    pool = models.ForeignKey(Pool, models.CASCADE, verbose_name='投票類型')
    candidate = models.ForeignKey('candidates.Candidate',
                                  models.CASCADE,
                                  verbose_name='候選人')
    is_agree = models.BooleanField('同意票', default=True)
    create_at = models.DateTimeField('投票時間', auto_now_add=True)

    class Meta:
        unique_together = (
            ('email', 'pool'),
        )

    def __str__(self):
        return '{} vote at {}'.format(self.email, self.pool)

    def clean(self):
        if (not self.is_agree) and len(self.pool.candidates.all()) != 1:
            raise ValidationError({
                'is_agree': 'No disagree for more than one candidate.',
            })
