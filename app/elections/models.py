from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from app.school.models import Department


class Time(models.Model):
    start_at = models.DateTimeField('開始時間')
    end_at = models.DateTimeField('結束時間')

    class Meta:
        verbose_name = '選舉時間'
        verbose_name_plural = '選舉時間'

    def __str__(self):
        return '{} - {}'.format(self.start_at, self.end_at)

    def clean(self):
        if self.start_at > self.end_at:
            raise ValidationError('開始時間必須小於結束時間。')

        if Time.objects.exists() and not self.pk:
            raise ValidationError('已經存在一筆投票時間紀錄了。')

    @property
    def is_vote_time(self):
        return self.start_at <= timezone.now() <= self.end_at


class Pool(models.Model):
    name = models.CharField('選舉類型', max_length=50, unique=True)
    departments = models.ManyToManyField(Department, verbose_name='可參與科系')

    class Meta:
        verbose_name = '選舉'
        verbose_name_plural = '選舉'

    def __str__(self):
        return self.name


class Vote(models.Model):
    std_no = models.CharField('學號', max_length=15)
    candidate = models.ForeignKey(
        'candidates.Candidate',
        models.CASCADE,
        verbose_name='候選人'
    )
    is_agree = models.BooleanField('同意票', default=True)
    create_at = models.DateTimeField('投票時間', auto_now_add=True)

    class Meta:
        verbose_name = '選票'
        verbose_name_plural = '選票'

    def __str__(self):
        return '{} vote for {}'.format(self.std_no, self.candidate)

    @property
    def pool(self):
        return self.candidate.pool

    def clean(self):
        try:  # No cross validation if fields validation not pass.
            self.clean_fields()
        except ValidationError:
            return

        errors = {}

        if not self.is_agree and self.pool.candidates.count() != 1:
            errors.setdefault('is_agree', []).append('此選舉不能投不同意票。')

        voted = Vote.objects \
            .filter(std_no=self.std_no, candidate__pool=self.pool) \
            .exclude(pk=self.pk) \
            .exists()

        if voted:
            errors.setdefault('candidate', []).append('你已經參與過這個選舉了。')

        if errors:
            raise ValidationError(errors)
