from django.contrib import admin

from .models import Time, Pool, Vote


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'start_at', 'end_at')

    def get_name(self, _):
        return '選舉時間'

    get_name.short_description = '名稱'


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_departments')
    filter_horizontal = ('departments',)

    def get_departments(self, obj):
        return ', '.join([d.name for d in obj.departments.all()])

    get_departments.short_description = '可參與科系'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('email', 'pool')
