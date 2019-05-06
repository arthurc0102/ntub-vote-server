from django.contrib import admin

from config.components.common import VOTE_ADMIN

from util.admin.decorators import short_description

from .models import Time, Pool, Vote
from .forms import VoteForm


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'start_at', 'end_at')

    def get_name(self, _):
        return '選舉時間'

    get_name.short_description = '名稱'


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_groups', 'get_departments')
    filter_horizontal = ('departments', 'groups')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('departments', 'groups')

    @short_description('可參與科系')
    def get_departments(self, obj):
        return ', '.join([d.name for d in obj.departments.all()])

    @short_description('可參與群組')
    def get_groups(self, obj):
        return ', '.join([g.name for g in obj.groups.all()])


class VoteAdmin(admin.ModelAdmin):
    list_display = ('std_no', 'candidate')
    form = VoteForm


if VOTE_ADMIN:
    admin.site.register(Vote, VoteAdmin)
