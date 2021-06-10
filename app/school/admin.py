from django.contrib import admin

from import_export.admin import ImportMixin

from util.admin.decorators import short_description

from .models import Department, Group, Student, System
from .resources import StudentResources


@admin.register(Department, Group, System)
class DisplayNameAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Student)
class StudentAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('std_no', 'get_groups')
    filter_horizontal = ('groups', )
    resource_class = StudentResources

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('groups')

    @short_description('群組')
    def get_groups(self, obj):
        return ', '.join([g.name for g in obj.groups.all()])
