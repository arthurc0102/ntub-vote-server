from django.contrib import admin

from import_export.admin import ImportMixin

from .models import Department, Group, Student
from .resources import StudentResources


@admin.register(Department, Group)
class DisplayNameAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Student)
class StudentAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('std_no',)
    resource_class = StudentResources
